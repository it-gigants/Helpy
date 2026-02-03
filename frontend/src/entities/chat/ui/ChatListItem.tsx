import { chatStatusLabel } from '../model/helpers';
import type {Chat} from "../model/types.ts";
import {ConversationListItem} from "@/shared/uikit/ConversationListItem";

interface ChatListItemProps {
    chat: Chat;
    isActive: boolean;
    onClick: () => void;
}

export const ChatListItem = ({ chat, isActive, onClick }: ChatListItemProps) => (
    <ConversationListItem
        title={chat.topic}
        subtitle={chatStatusLabel[chat.status]}
        isActive={isActive}
        onClick={onClick}
    />
);
