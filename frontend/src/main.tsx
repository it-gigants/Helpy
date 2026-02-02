import { createRoot } from "react-dom/client";
import "./app/styles/index.scss";
import App from "./app/App.tsx";
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import {ThemeProvider} from "./app/providers/ThemeProvider.tsx";

createRoot(document.getElementById("root")!).render(
    <ThemeProvider>
        <App />
    </ThemeProvider>
);
