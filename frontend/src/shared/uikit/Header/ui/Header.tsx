import {AppBar, type AppBarProps} from "@mui/material";
import type {FC} from "react";

export const Header:FC<AppBarProps> = ({children, ...props}) => {
    return (
        <AppBar {...props}>{children}</AppBar>
    );
};

