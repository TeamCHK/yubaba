(() => {
    chrome.runtime.onMessage.addListener((obj, sender, response) => {
        const { random, url } = obj;
        messageReceived(url, random);
    });

    const messageReceived = (url: any, random: any) => {
        console.log("Message received from content script");
        console.log(random);
        console.log(url);
    };
})();
