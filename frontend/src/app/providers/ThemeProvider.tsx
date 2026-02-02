import { ThemeProvider as MuiThemeProvider, CssBaseline } from "@mui/material";
import { theme } from "../theme/components";
import type {FC, ReactNode} from "react";

interface ThemeProviderProps {
    children: ReactNode;
}

export const ThemeProvider: FC<ThemeProviderProps> = ({ children }) => (
    <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
    </MuiThemeProvider>
);
