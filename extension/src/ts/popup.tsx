import React, { useEffect, useState } from "react";
import { createRoot, Root } from "react-dom/client";
import { PopupToBackgroundMsg, BackgroundToPopupMsg, MsgType } from "./types";


const Popup = () => {
    const [content, setContent] = useState('');

    useEffect(() => {
        const msg : PopupToBackgroundMsg = {
            type: MsgType.PopUpInit
        };
        chrome.runtime.sendMessage(msg, function(response: BackgroundToPopupMsg) {
            setContent(response.summary);
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
