import React from "react";
import { createRoot, Root } from "react-dom/client";
import Popup from './Popup';

const root: Root = createRoot(
    document.getElementById("react-target") as HTMLElement
);

root.render(
    <React.StrictMode>
        <Popup />
    </React.StrictMode>
);
