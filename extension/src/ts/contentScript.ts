import { ContentToBackgroundMsg, MsgType } from "./types";

const sendContent = (textToSend: string) => {
    const msg: ContentToBackgroundMsg = {
        type: MsgType.PageContent,
        text: textToSend
    };
    chrome.runtime.sendMessage(msg);
};
//TODO: Decide and change whether we'll serve all types of websites vs only certain websites
if (window.location.href.includes('cnn.com') && window.location.href.includes('index.html')) {
    const body: HTMLElement = document.body;
    const bodyText: Array<string> = body.outerText.split("\n").filter(text => text);

    sendContent(bodyText[15]);
}
