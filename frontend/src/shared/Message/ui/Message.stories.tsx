import type {Meta, StoryObj} from "@storybook/react-vite";
import {Message} from "./Message.tsx";

const meta: Meta<typeof Message> = {
    title: "Компоненты/Chat/Message",
    component: Message,
    tags: ["autodocs"]
}

export default meta;

type Story = StoryObj<typeof Message>;


export const Elevation: Story = {
    args: {
        children: "Привет, чем могу помочь?",
        variant: "elevation",
        style: {
            padding: "15px 10px"
        }
    }
}

export const Outlined: Story = {
    args: {
        children: "Привет, чем могу помочь?",
        variant: "outlined",
        style: {
            padding: "15px 10px"
        }
    }
}

export const Square: Story = {
    args: {
        children: "Привет, чем могу помочь?",
        square: true,
        style: {
            padding: "15px 10px"
        }
    }
}



