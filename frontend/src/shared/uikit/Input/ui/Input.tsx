import {TextField, type TextFieldProps} from "@mui/material";
import type {FC} from "react";


export const Input: FC<TextFieldProps> = ({...props}) => {
    return (
        <TextField {...props} />
    );
};

