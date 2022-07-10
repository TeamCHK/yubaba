try {
    chrome.tabs.onUpdated.addListener((tabId, tab) => {
        if (tab.url && tab.url.includes("youtube.com/watch") ) {
            console.log(tab.url);

            chrome.tabs.sendMessage(tabId, {
                random: "Hello Jun",
                url: tab.url,
            })
            console.log("Message sent from background")
        }
    })
  } catch (err) {
    console.log(err);
  }

