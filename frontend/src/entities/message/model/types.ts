import type {MessageSender} from "@/shared/types/message.ts";

export interface Message {
    id: number;
    chatId: number;
    sender: MessageSender;
    text: string;
    createdAt: string;
}