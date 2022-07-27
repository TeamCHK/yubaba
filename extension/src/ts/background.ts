import wretch from 'wretch';
import { MsgType } from './types';


var textToSummarize: string | null;

try {
    chrome.runtime.onMessage.addListener(
        function(request, _, sendResponse) {
            if (request.type === MsgType.PageContent) {
                textToSummarize = request.text;
            }
            else if (request.type === MsgType.PopUpInit) {
                if (textToSummarize != null) {
                    sendResponse({
                        textToSummarize: textToSummarize,
                        articleTitle: "'Article Title Placeholder'"
                    });
                }
            }
        }
    );
} catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
};
