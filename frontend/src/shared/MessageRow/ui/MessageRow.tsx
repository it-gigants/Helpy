import type {FC, ReactNode} from "react";
import {Box} from "@mui/material";

interface MessageRowProps {
    isOwn?: boolean;
    children: ReactNode;
}

export const MessageRow: FC<MessageRowProps> = ({isOwn, children}) => {
    return (
        <Box
            display="flex"
            justifyContent={isOwn ? 'flex-end' : 'flex-start'}
        >
            {children}
        </Box>
    )
}