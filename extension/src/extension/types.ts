export enum MsgType {
    PageContent = 'page-content',
    PopUpInit = 'popup-init',
};

export type ContentToBackgroundMsg = {
    type: MsgType,
    text: string
};

export type PopupToBackgroundMsg = {
    type: MsgType
};

export type BackgroundToPopupMsg = {
    articleTitle: string,
    textToSummarize: string
};

export type MLISResponse = {
    text: string
};
