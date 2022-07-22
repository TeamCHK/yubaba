import axios from 'axios';

// try {
//     chrome.tabs.onUpdated.addListener(
//         async (tabId: number, 
//                changeInfo: chrome.tabs.TabChangeInfo, 
//                tab: chrome.tabs.Tab) => {
//         if (changeInfo.status == 'complete') {
//             if (tab.url && tab.url.includes("cnn.com/") && tab.url.includes("index.html") ) {
//                 console.log(tab.url);
//                 chrome.tabs.sendMessage(tabId, {
//                     url: tab.url,
//                 })
//                 console.log("Message sent from background script")
//             }
//         }
//     })
//   } catch (err) {
//     const msg: String = (err instanceof Error) ? err.message : String(err);
//     console.log(msg);
//   }
// chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
//     if (changeInfo == 'complete') {
//         chrome.runtime.sendMessage('page-content', (response) => {
//             console.log('received page content', response);
//         });
//         console.log('message sent!');
//     }
// });


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        console.log(sender.tab ? 'from content script: ' + sender.tab.url :
        'from extension')

        if (request.type == 'page-content') {
            console.log(request.text);
            axios.post('http://localhost:8000/summary',{
                text: request.text
            }).then(response => {
                console.log(response);
            }, (error) => {
                console.log(error);
            });
        }
    }
);

