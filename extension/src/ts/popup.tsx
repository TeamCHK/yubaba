import React, { useEffect, useState } from "react";
import { createRoot, Root } from "react-dom/client";


export const Popup = () => {
    const [content, setContent] = useState('');

    useEffect(() => {
        chrome.tabs.query({currentWindow: true, active: true}, tabs => {
            const currentTabId: number = tabs.length === 0 ? 0 : tabs[0].id!;
            chrome.tabs.sendMessage(currentTabId, '', response => setContent(response));
        });
    }, []);

    return (
        <div>
            {content}
        </div>
    );
};

const rootElement: HTMLElement = document.getElementById("react-target")!;
const root: Root = createRoot(rootElement);

root.render(<Popup />);
