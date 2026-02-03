import type { Meta, StoryObj } from '@storybook/react-vite';
import { Footer } from './Footer.tsx';
import { TextField, Button, Typography } from '@mui/material';

const meta: Meta<typeof Footer> = {
    title: 'Компоненты/Layout/Footer',
    component: Footer,
    tags: ['autodocs'],
    argTypes: {
        sx: {
            table: { disable: true },
        },
    },
};

export default meta;
type Story = StoryObj<typeof Footer>;

export const Default: Story = {
    args: {
        children: (
            <Typography variant="body2">
                Footer content
            </Typography>
        ),
    },
};

export const ChatInput: Story = {
    args: {
        children: (
            <>
                <TextField
                    placeholder="Введите сообщение"
                    size="small"
                    fullWidth
                />
                <Button variant="contained">
                    Отправить
                </Button>
            </>
        ),
    },
};

export const OnlyActions: Story = {
    args: {
        children: (
            <>
                <Button color="inherit">Отмена</Button>
                <Button variant="contained">Сохранить</Button>
            </>
        ),
    },
};

export const Dense: Story = {
    args: {
        sx: {
            py: 0.5,
        },
        children: (
            <>
                <TextField
                    placeholder="Сообщение"
                    size="small"
                    fullWidth
                />
                <Button size="small" variant="contained">
                    OK
                </Button>
            </>
        ),
    },
};

