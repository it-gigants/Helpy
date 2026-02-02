import {createTheme} from "@mui/material";
import {typography} from "../typography.ts";
import {palette} from "../palette.ts";
import {shape} from "../shape.ts";
import {components} from "../index.ts";

export const theme = createTheme({
    palette,
    typography,
    shape,
    components,
});