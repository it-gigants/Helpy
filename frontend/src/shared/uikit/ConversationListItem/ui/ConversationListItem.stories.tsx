import type { Meta, StoryObj } from '@storybook/react-vite';
import { ConversationListItem } from './ConversationListItem';
import { List } from '@mui/material';

const meta: Meta<typeof ConversationListItem> = {
    title: 'Компоненты/Навигация/ConversationListItem',
    component: ConversationListItem,
    tags: ['autodocs'],
    decorators: [
        (Story) => (
            <List sx={{ width: 320, bgcolor: 'background.paper' }}>
                <Story />
            </List>
        ),
    ],
};

export default meta;
type Story = StoryObj<typeof ConversationListItem>;

export const Default: Story = {
    args: {
        title: 'Заказ #1234',
        subtitle: 'Последнее сообщение...',
    },
};

export const Active: Story = {
    args: {
        title: 'Поддержка',
        subtitle: 'Оператор подключился',
        isActive: true,
    },
};

export const WithoutSubtitle: Story = {
    args: {
        title: 'Новый диалог',
    },
};

export const Disabled: Story = {
    args: {
        title: 'Архивный чат',
        subtitle: 'Чат завершён',
        disabled: true,
    },
};

export const LongText: Story = {
    args: {
        title: 'Очень длинное название диалога которое не должно ломать layout',
        subtitle:
            'Очень длинный текст последнего сообщения который должен аккуратно обрезаться',
    },
};
