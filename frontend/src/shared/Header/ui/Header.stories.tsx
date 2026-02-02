import type { Meta, StoryObj } from '@storybook/react-vite';
import { Header } from './Header';
import { Box, Typography, Button } from '@mui/material';

const meta: Meta<typeof Header> = {
    title: 'Компоненты/Layout/Header',
    component: Header,
    tags: ['autodocs'],
    argTypes: {
        position: {
            control: 'select',
            options: ['fixed', 'absolute', 'sticky', 'static', 'relative'],
        },
        color: {
            control: 'select',
            options: ['primary', 'secondary', 'transparent', 'default'],
        },
        sx: {
            table: { disable: true },
        },
    },
};

export default meta;
type Story = StoryObj<typeof Header>;


export const Default: Story = {
    args: {
        position: 'static',
        children: (
            <Box px={2} py={1}>
                <Typography variant="h6">Header</Typography>
            </Box>
        ),
    },
};

export const WithActions: Story = {
    args: {
        position: 'static',
        children: (
            <Box
                px={2}
                py={1}
                display="flex"
                alignItems="center"
                justifyContent="space-between"
            >
                <Typography variant="h6">Support Chat</Typography>
                <Button color="inherit">Выйти</Button>
            </Box>
        ),
    },
};

export const Sticky: Story = {
    args: {
        position: 'sticky',
        children: (
            <Box px={2} py={1}>
                <Typography variant="h6">Sticky Header</Typography>
            </Box>
        ),
    },
};

export const Transparent: Story = {
    args: {
        position: 'static',
        color: 'transparent',
        elevation: 0,
        children: (
            <Box px={2} py={1}>
                <Typography variant="h6">Transparent Header</Typography>
            </Box>
        ),
    },
};

