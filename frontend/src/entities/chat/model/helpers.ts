import type {ChatStatus} from "@/shared/types/chat.ts";

export const chatStatusLabel: Record<ChatStatus, string> = {
    queued: 'В очереди',
    active: 'Активен',
    closed: 'Завершен'
}