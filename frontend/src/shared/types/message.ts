export type MessageSender = 'client' | 'operator' | 'system';

export interface Message {
    id: number;
    chatId: number;
    sender: MessageSender;
    text: string;
    createdAt: string;
}