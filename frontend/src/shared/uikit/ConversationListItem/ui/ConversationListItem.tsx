import type { FC } from 'react';
import {
    ListItem,
    ListItemButton,
    ListItemText,
    type ListItemButtonProps,
} from '@mui/material';

export interface ConversationListItemProps {
    title: string;
    subtitle?: string;
    isActive?: boolean;
    disabled?: boolean;
    onClick?: ListItemButtonProps['onClick'];
}

export const ConversationListItem: FC<ConversationListItemProps> = ({
        title,
        subtitle,
        isActive = false,
        disabled = false,
        onClick,
    }) => {
    return (
        <ListItem disablePadding>
            <ListItemButton
                selected={isActive}
                disabled={disabled}
                onClick={onClick}
                sx={{
                    alignItems: 'flex-start',
                    py: 1.25,
                }}
            >
                <ListItemText
                    primary={title}
                    secondary={subtitle}
                    primaryTypographyProps={{
                        fontWeight: isActive ? 600 : 400,
                        noWrap: true,
                    }}
                    secondaryTypographyProps={{
                        noWrap: true,
                    }}
                />
            </ListItemButton>
        </ListItem>
    );
};
