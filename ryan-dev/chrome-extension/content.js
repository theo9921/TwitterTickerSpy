// content.js
chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      if(request.message === "clicked_browser_action" ) {
          //var firstHref = $("a[href^='http']").eq(3).attr("href");
          //var test = $("[dir~='ltr'] span.css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0").text();

          // Get URL of current website
          var current_url = window.location.href;
          //console.log(current_url);

          // Extract twitter username from URL
          const regex = /(?<=twitter\.com\/)\w*/;
          var username = current_url.match(regex);
          console.log('@'.concat(username[0]));

          // Send URL to background.js
          chrome.runtime.sendMessage({"message": "twitter_handle", "handle": username, "url": current_url});
      }
    }
);
