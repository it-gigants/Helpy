import {ButtonActive} from "./ButtonActive.tsx";
import type { Meta, StoryObj } from "@storybook/react";


const meta: Meta<typeof ButtonActive> = {
    title: "Компоненты/Buttons",
    component: ButtonActive,
    tags: ['autodocs']
}

export default meta;
type Story = StoryObj<typeof ButtonActive>

export const Primary: Story = {
    args: {
        appearance: 'primary',
        children: 'Кнопка',
        isLoading: false,
    }
}