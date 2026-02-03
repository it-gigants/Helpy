import type {MessageSender} from "@/shared/types/message.ts";
import type {Message} from "./types.ts";


export const senderLabel: Record<MessageSender, string> = {
    client: 'Клиент',
    operator: 'Оператор',
    system: 'Система',
}

export const isOwnMessage = (
    message: Message,
    currentRole: 'client' | 'operator'
) => message.sender === currentRole;
