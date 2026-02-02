import {Loader} from "./Loader.tsx";
import type {Meta, StoryObj} from "@storybook/react-vite";

const meta: Meta<typeof Loader> = {
    title: "Компоненты/Loader",
    component: Loader,
    tags: ["autodocs"]
}

export default meta;

type Story = StoryObj<typeof Loader>;


export const Primary: Story = {
    args: {
        color: "primary"
    }
}

export const Secondary: Story = {
    args: {
        color: "secondary"
    }
}

