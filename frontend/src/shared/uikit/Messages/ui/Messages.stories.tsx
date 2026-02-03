import type { Meta, StoryObj } from '@storybook/react-vite';
import { Messages } from './Messages.tsx';

const meta: Meta<typeof Messages> = {
    title: 'Компоненты/Chat/Messages',
    component: Messages,
    tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Messages>;

export const Default: Story = {
    args: {
        messages: [
            {
                id: '1',
                text: 'Здравствуйте! Чем могу помочь?',
                isOwn: false,
            },
            {
                id: '2',
                text: 'У меня проблема с заказом',
                isOwn: true,
            },
        ],
    },
};

export const OnlySupport: Story = {
    args: {
        messages: [
            {
                id: '1',
                text: 'Мы уже проверяем ваш запрос',
                isOwn: false,
            },
            {
                id: '2',
                text: 'Подскажите номер заказа',
                isOwn: false,
            },
        ],
    },
};

export const OnlyUser: Story = {
    args: {
        messages: [
            {
                id: '1',
                text: 'Привет',
                isOwn: true,
            },
            {
                id: '2',
                text: 'Есть кто-нибудь?',
                isOwn: true,
            },
        ],
    },
};

export const LongConversation: Story = {
    args: {
        messages: [
            {
                id: '1',
                text: 'Здравствуйте! Чем могу помочь?',
                isOwn: false,
            },
            {
                id: '2',
                text: 'Не могу войти в аккаунт',
                isOwn: true,
            },
            {
                id: '3',
                text: 'Появляется ошибка при авторизации?',
                isOwn: false,
            },
            {
                id: '4',
                text: 'Да, пишет что пароль неверный',
                isOwn: true,
            },
            {
                id: '5',
                text: 'Попробуйте восстановление пароля',
                isOwn: false,
            },
        ],
    },
};
