import type { Meta, StoryObj } from '@storybook/react-vite';
import { Input } from './Input.tsx';

const meta: Meta<typeof Input> = {
    title: 'Компоненты/Input',
    component: Input,
    tags: ['autodocs'],

    argTypes: {
        variant: {
            control: 'select',
            options: ['outlined', 'standard', 'filled'],
            description: 'Визуальный вариант инпута',
        },

        error: {
            control: 'boolean',
            description: 'Состояние ошибки',
        },
        disabled: {
            control: 'boolean',
            description: 'Отключённое состояние',
        },
        required: {
            control: 'boolean',
        },

        label: {
            control: 'text',
        },
        helperText: {
            control: 'text',
        },
        placeholder: {
            control: 'text',
        },

        sx: {
            table: { disable: true },
        },
        onChange: {
            table: { disable: true },
        },
    },
}

export default meta;

type Story = StoryObj<typeof Input>;

export const Playground: Story = {
    args: {
        label: "Label",
        placeholder: "Placeholder",
    },
};

export const Error: Story = {
    args: {
        label: "Email",
        error: true,
        helperText: "Invalid email",
    },
};

export const Disabled: Story = {
    args: {
        label: "Disabled",
        disabled: true,
    },
};

export const Required: Story = {
    args: {
        label: "Required",
        required: true,
    },
};
