import wretch from 'wretch';
import { MLISRequest, MLISResponse } from './types';

// TODO: Issue #14: Change url and endpoint after MLIS is ready
// const apiRoot: string = "http://localhost:8000";
const apiRoot: string = "https://jlgl3bu3n6.execute-api.us-east-1.amazonaws.com/test/pass-article-to-summarization-model";
const summarizationEndpoint: string = "/summary";

console.log("background")
try {
    chrome.runtime.onMessage.addListener(
        function (request: MLISRequest, _, sendResponse: (response: MLISResponse) => void) {
            console.log("Message received")
            wretch(apiRoot + summarizationEndpoint)
                .options({ mode: "cors" })
                .post({ text: request.url })
                .json((mlisResponse: MLISResponse) => {
                    console.log(mlisResponse)
                    sendResponse(mlisResponse)
                });
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
