import React from "react";
import { createRoot } from "react-dom/client";

function Popup() {
    return (
        <div>
            <h1>Hello, World</h1>
            <p>This is a changed popup.</p>
            <p>Hello</p>
        </div>
    );
}

const rootElement: HTMLElement = document.getElementById("react-target")!;
const root = createRoot(rootElement);

root.render(
    <Popup />
);
