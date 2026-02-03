import type {ChatStatus} from "@/shared/types/chat.ts";

export interface Chat {
    id: number;
    topic: string;
    status: ChatStatus;
    createdAt: string;
}