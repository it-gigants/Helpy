import { ThemeProvider as MuiThemeProvider, CssBaseline } from '@mui/material';
import {theme} from "../theme/components";
import type {FC} from "react";

interface ThemeProviderProps {
    children: React.ReactNode;
}

export const ThemeProvider: FC<ThemeProviderProps> = ({ children }) => (
    <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
    </MuiThemeProvider>
)

