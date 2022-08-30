import wretch from 'wretch';
import { MLISRequest, MLISResponse } from './types';

const apiRoot: string = "https://aacxuouv1m.execute-api.us-east-1.amazonaws.com/default";
const summarizationEndpoint: string = "/summarize";

try {
    chrome.runtime.onMessage.addListener(
        function (
            request: MLISRequest,
            _,
            sendResponse: (response: MLISResponse) => void
        ) {
            console.log("[Yubaba] Waiting for summarization process...")
            wretch(apiRoot + summarizationEndpoint)
                .options({ mode: "cors" })
                .post({ url: request.url })
                .error(500, error => {
                    // TODO: Implement error page (https://github.com/TeamCHK/yubaba/issues/24)
                })
                .res(res => {
                    res.json().then(body => {
                        console.log(`[Yubaba] (${res.status}) Received response:`, body)
                        sendResponse({
                            ...body,
                            status: res.status,
                        })
                    })
                })
            return true; // This allows message sender to wait for async sendResponse
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
