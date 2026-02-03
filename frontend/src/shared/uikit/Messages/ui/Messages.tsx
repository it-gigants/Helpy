import type {FC} from "react";
import {Stack} from "@mui/material";
import {MessageRow} from "../../MessageRow";
import {Message} from "../../Message";

interface MessagesProps {
    messages: {
        id: string;
        text: string;
        isOwn: boolean;
    }[]
}


export const Messages: FC<MessagesProps> = ({ messages }) => {
    return (
        <Stack spacing={1}>
            {messages.map((m) => (
                <MessageRow key={m.id} isOwn={m.isOwn}>
                    <Message>
                        {m.text}
                    </Message>
                </MessageRow>
            ))}
        </Stack>
    )
}