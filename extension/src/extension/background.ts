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
                .res(res => {
                    res.json().then(body => {
                        console.log(`[Yubaba] (${res.status}) Received response:`)
                        console.log(body)
                        sendResponse({
                            ...body,
                            status: res.status,
                        })
                    })
                })
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
