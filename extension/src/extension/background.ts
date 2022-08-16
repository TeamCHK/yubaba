import wretch from 'wretch';
import { MLISRequest, MLISResponse } from './types';

// TODO: Issue #14: Change url and endpoint after MLIS is ready
const apiRoot: string = "http://localhost:8000";
const summarizationEndpoint: string = "/summary";


try {
    chrome.runtime.onMessage.addListener(
        function (request: MLISRequest, _, sendResponse: (response: MLISResponse) => void) {
            wretch(apiRoot + summarizationEndpoint)
                .options({ mode: "cors" })
                .post({ text: request.url })
                .json((mlisResponse: MLISResponse) => {
                    sendResponse(mlisResponse)
                });
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
