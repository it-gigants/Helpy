import { ButtonActive } from "./ButtonActive.tsx";
import type { Meta, StoryObj } from "@storybook/react-vite";

const meta: Meta<typeof ButtonActive> = {
    title: "Компоненты/Button",
    component: ButtonActive,
    tags: ["autodocs"],
    argTypes: {
        variant: {
            control: "select",
            options: ["contained", "outlined", "text"],
        },
        color: {
            control: "select",
            options: ["primary", "secondary", "error", "info", "success", "warning"],
        },
        size: {
            control: "radio",
            options: ["small", "medium", "large"],
        },
        loading: {
            control: "boolean",
        },
        disabled: {
            control: "boolean",
        },
        children: {
            control: "text",
        },
    },
};

export default meta;
type Story = StoryObj<typeof ButtonActive>;

export const Primary: Story = {
    args: {
        size: "medium",
        color: "primary",
        variant: "contained",
        children: "Кнопка",
        loading: false,
    },
};

export const Outlined: Story = {
    args: {
        variant: "outlined",
        children: "Outlined",
    },
};

export const Text: Story = {
    args: {
        variant: "text",
        children: "Text",
    },
};

export const Loading: Story = {
    args: {
        loading: true,
        children: "Загрузка",
    },
};

export const Disabled: Story = {
    args: {
        disabled: true,
        children: "Disabled",
    },
};
