// content.js
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if(request.message === "clicked_browser_action" ) {
        //var firstHref = $("a[href^='http']").eq(3).attr("href");
        var current_url = window.location.href // Get current URL
        console.log(current_url);

        // Send URL to background.js
        chrome.runtime.sendMessage({"message": "open_new_tab", "url": current_url});
      }
    }
);