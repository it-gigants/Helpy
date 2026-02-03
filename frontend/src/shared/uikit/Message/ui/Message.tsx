import type { FC } from 'react';
import { Paper, type PaperProps } from '@mui/material';

export const Message: FC<PaperProps> = ({ children, ...props }) => {
    return <Paper {...props}>{children}</Paper>;
};
