const getArticleTitle = () : String => {
    const tag = document.querySelector('div.l-container h1.pg-headline') as HTMLHeadingElement;
    return tag?.innerText ?? "";
};

// (() => {
//     chrome.runtime.onMessage.addListener((msg, sender, callback) => {
//         console.log('Message received from sender: ', sender.id, msg);
//         const articleTitle : String = getArticleTitle();
//         const displayText : String = articleTitle ? `The article title is ${articleTitle}` : "Not a CNN article page";
//         callback(displayText);
//     });
// })();



const body = document.body;
const bodyText = body.outerText.split("\n").filter(text => text);

console.log(bodyText);

const delay = (ms: number) : Promise<void> => {
    return new Promise( resolve => setTimeout(resolve, ms));
}

const sendContent = () => {
    const msg = {
        type: 'page-content',
        text: bodyText[10]
    };
    console.log('sending message to background');
    chrome.runtime.sendMessage(msg);
};

sendContent();
