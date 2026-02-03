import type {Message} from "../../types/message.ts";

export type ClientEvent =
    | { type: 'chat:start'; topic: string}
    | { type: 'message:send'; chatId: string; text: string}
    | { type: 'chat:close'; chatId: string}

export type OperatorEvent =
    | {type: 'chat:accept'; chatId: string}
    | {type: 'chat:accept'; chatId: string}

export type ServerEvent =
    | { type: 'chat:queued'; chatId: string; position: number }
    | { type: 'chat:activated'; chatId: string; operatorId: number }
    | { type: 'message:new', message: Message}
    | { type: 'chat:closed', chatId: number}

