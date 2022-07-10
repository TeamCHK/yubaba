const getArticleTitle = () : String => {
    const tag = document.querySelector('div.l-container h1.pg-headline') as HTMLHeadingElement;
    return tag?.innerText ?? "";
};

(() => {
    chrome.runtime.onMessage.addListener((msg, sender, callback) => {
        console.log('Message received from sender: ', sender.id, msg);
        const articleTitle : String = getArticleTitle();
        const displayText : String = articleTitle ? `The article title is ${articleTitle}` : "Not a CNN article page";
        callback(displayText);
    });
})();
