import type {FC} from "react";
import {Button, type ButtonProps} from "@mui/material";

export const ButtonActive:FC<ButtonProps> = ({
   children,
    sx,
    ...props
    }) => {
    return (
        <Button
            type="button"
            sx={{
                borderRadius: "10px",
                textTransform: 'none',
                ...sx,
            }}
            {...props}
        >
                {children}
        </Button>
    );
};

