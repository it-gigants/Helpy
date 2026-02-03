import type { FC, ReactNode } from 'react';
import { Box } from '@mui/material';

interface SidebarProps {
    children: ReactNode;
    width?: number | string;
}

export const Sidebar: FC<SidebarProps> = ({
                                              children,
                                              width = 320,
                                          }) => {
    return (
        <Box
            component="aside"
            sx={{
                width,
                height: '100%',
                borderRight: '1px solid',
                borderColor: 'divider',
                backgroundColor: 'background.paper',
                display: 'flex',
                flexDirection: 'column',
            }}
        >
            {children}
        </Box>
    );
};
