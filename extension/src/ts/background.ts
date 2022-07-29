import wretch from 'wretch';
import { MsgType } from './types';


var summarizedText: string | null;

// TODO: Issue #14: Change url and endpoint after MLIS is ready
const apiRoot: string = "http://localhost:8000";
const summarizationEndpoint: string = "/summary";

try {
    chrome.runtime.onMessage.addListener(
        function(request, _, sendResponse) {
            if (request.type === MsgType.PageContent) {
                wretch(apiRoot + summarizationEndpoint)
                .options({mode: "cors"})
                .post({text: request.text})
                .json(response => {
                    summarizedText = response.text;
                });
            }
            else if (request.type === MsgType.PopUpInit) {
                if (summarizedText != null) {
                    sendResponse({
                        summary: summarizedText
                    });
                }
            }
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
