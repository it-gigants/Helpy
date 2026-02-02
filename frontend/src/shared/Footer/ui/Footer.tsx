import type { FC } from 'react';
import { Box, type BoxProps } from '@mui/material';

export const Footer: FC<BoxProps> = ({
                                         children,
                                         sx,
                                         ...props
                                     }) => {
    return (
        <Box
            component="footer"
            sx={{
                px: 2,
                py: 1,
                borderTop: '1px solid',
                borderColor: 'divider',
                display: 'flex',
                alignItems: 'center',
                gap: 1,
                backgroundColor: 'background.paper',
                ...sx,
            }}
            {...props}
        >
            {children}
        </Box>
    );
};
