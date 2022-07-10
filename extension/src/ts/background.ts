const delay = (ms: number) : Promise<void> => {
    return new Promise( resolve => setTimeout(resolve, ms));
}

try {
    // TODO: types of tabId, tab to be determined
    chrome.tabs.onUpdated.addListener(async (tabId, tab) => {
        if (tab.url && tab.url.includes("cnn.com/") && tab.url.includes("index.html") ) {
            console.log(tab.url);
            // TODO: replace delay with webpage load completion listener
            await delay(3000);
            chrome.tabs.sendMessage(tabId, {
                url: tab.url,
            })
            console.log("Message sent from background script")
        }
    })
  } catch (err) {
    const msg: String = (err instanceof Error) ? err.message : String(err);
    console.log(msg);
  }
