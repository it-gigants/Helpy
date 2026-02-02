import type {Components} from "@mui/material";

export const button: Components['MuiButton'] = {
    defaultProps: {
        disableElevation: true
    },
    styleOverrides: {
        root: {
            borderRadius: 10
        }
    }
}