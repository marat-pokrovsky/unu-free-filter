document.getElementById("runScript1").addEventListener("click", () => {
  chrome.scripting.executeScript({
    target: {
      tabId: chrome.tabs.query({ active: true, currentWindow: true })[0].id,
    },
    files: ["script1.js"],
  });
});

document.getElementById("runScript2").addEventListener("click", () => {
  chrome.scripting.executeScript({
    target: {
      tabId: chrome.tabs.query({ active: true, currentWindow: true })[0].id,
    },
    files: ["script2.js"],
  });
});
