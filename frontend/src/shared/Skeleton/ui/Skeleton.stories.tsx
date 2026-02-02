import type {Meta, StoryObj} from "@storybook/react-vite";
import {SkeletonBlock} from "./Skeleton.tsx";

const meta: Meta<typeof SkeletonBlock> = {
    title: "Компоненты/Skeleton",
    component: SkeletonBlock,
    tags: ["autodocs"]
}

export default meta;

type Story = StoryObj<typeof SkeletonBlock>;


export const Text: Story = {
    args: {
        variant: "text",
        width: 400,
        height: 50
    }
}

export const Circular: Story = {
    args: {
        variant: "circular",
        width: 50,
        height: 50
    }
}


export const Rectangular: Story = {
    args: {
        variant: "rectangular",
        width: 400,
        height: 50
    }
}


export const Rounded: Story = {
    args: {
        variant: "rounded",
        width: 400,
        height: 50
    }
}

