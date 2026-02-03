export type ChatStatus = 'queued' | 'active' | 'closed';

export interface Chat {
    id: number;
    status: ChatStatus;
    topic: string;
    clientId: number;
    operatorId?: number;
}