from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import Mock

import pytest
from aiokafka import AIOKafkaProducer
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from redis.asyncio import ConnectionPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db.dependencies import get_db_session
from src.db.utils import create_database, drop_database
from src.services.kafka.dependencies import get_kafka_producer
from src.services.kafka.lifespan import init_kafka, shutdown_kafka
from src.services.redis.dependency import get_redis_pool
from src.core.config import settings
from src.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def _engine(anyio_backend: Any) -> AsyncGenerator[AsyncEngine]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from src.db.models.meta import meta
    from src.db.models import Base, Chat, Message, Topic, User, OperatorTopic, RefreshSession

    await create_database()

    engine = create_async_engine(str(settings.db.url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
async def test_kafka_producer() -> AsyncGenerator[AIOKafkaProducer]:
    """
    Creates kafka's producer.

    :yields: kafka's producer.
    """
    app_mock = Mock()
    await init_kafka(app_mock)
    yield app_mock.state.kafka_producer
    await shutdown_kafka(app_mock)


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool]:
    """
    Get instance of a fake redis.

    :yield: FakeRedis instance.
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
    fake_redis_pool: ConnectionPool,
    test_kafka_producer: AIOKafkaProducer,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    application.dependency_overrides[get_kafka_producer] = lambda: test_kafka_producer
    return application


@pytest.fixture
async def client(
    fastapi_app: FastAPI, anyio_backend: Any
) -> AsyncGenerator[AsyncClient]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(
        transport=ASGITransport(fastapi_app), base_url="http://test", timeout=2.0
    ) as ac:
        yield ac
