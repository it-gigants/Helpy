import type { Meta, StoryObj } from '@storybook/react-vite';
import { Sidebar } from './Sidebar.tsx';
import {
    Box,
    List,
    ListItem,
    ListItemText,
    Typography,
    Button, ListItemButton,
} from '@mui/material';

const meta: Meta<typeof Sidebar> = {
    title: 'Компоненты/Layout/Sidebar',
    component: Sidebar,
    tags: ['autodocs'],
    argTypes: {
        width: {
            control: 'number',
        },
    },
};

export default meta;
type Story = StoryObj<typeof Sidebar>;

export const Default: Story = {
    args: {
        children: (
            <Box p={2}>
                <Typography variant="h6">Sidebar</Typography>
            </Box>
        ),
    },
};

export const ConversationList: Story = {
    args: {
        children: (
            <>
                <Box p={2} borderBottom="1px solid" borderColor="divider">
                    <Typography variant="h6">Диалоги</Typography>
                </Box>

                <List disablePadding>
                    {['Иван', 'Анна', 'Поддержка', 'Заказ #1234'].map((name) => (
                        <ListItem disablePadding key={name}>
                            <ListItemButton>
                                <ListItemText
                                    primary={name}
                                    secondary="Последнее сообщение..."
                                />
                            </ListItemButton>
                        </ListItem>
                    ))}
                </List>
            </>
        ),
    },
};

export const WithFooter: Story = {
    args: {
        children: (
            <>
                <Box p={2}>
                    <Typography variant="h6">Диалоги</Typography>
                </Box>

                <Box flex={1} overflow="auto">
                    <List>
                        {['Чат 1', 'Чат 2', 'Чат 3'].map((item) => (
                            <ListItem disablePadding key={item}>
                                <ListItemButton>
                                    <ListItemText primary={item} />
                                </ListItemButton>
                            </ListItem>
                        ))}
                    </List>
                </Box>

                <Box p={2} borderTop="1px solid" borderColor="divider">
                    <Button fullWidth variant="contained">
                        Новый чат
                    </Button>
                </Box>
            </>
        ),
    },
};

export const Narrow: Story = {
    args: {
        width: 240,
        children: (
            <Box p={2}>
                <Typography variant="body1">
                    Узкий sidebar
                </Typography>
            </Box>
        ),
    },
};

