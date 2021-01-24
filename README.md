## Twitter Ticker $PY
__Hack Cambridge 2021__

There's no shortage of people on twitter giving investment advice, how does a user have a chance to separate signal from noise? We have built a browser extension which allows users to query any twitter profile and gain useful insight on their stock-promoting behaviour. Simply type in a twitter handle (e.g. 'JoeBiden', 'MadsC007', 'WarlusTrades' etc, and the extension will give you the following insight about that user:

- The stock they have tweeted about the most, and its ESG-score.
- The average ESG score of all stocks tweeted about, weighted by the number of mentions.
- The average return of stocks tweeted by this person since the stock was mentioned.

## How we built it
Using snscraper we are able to scrape all tweets by any user on the platform. We trained an ML model to identify which tweets are about stocks, and then used simple string-formatting to extract all ticker-mentions. ML-driven sentiment analysis built & pre-trained by Google is used to identify bullish tweets about stocks, such that only these stock mentions are included in the 'average stock return'-metric. These metrics are then passed along to the browser extension which users are able to interact with.

We hope that this tool will enable twitter users to make more informed decisions on the Twitter users that they follow by allowing them to identify the performance track-record and ESG profile of the companies that are being tweeted about.

One challenge with the workflow which we came up with is that serving users with the information they request takes quite some time; next step for this project would be to solve these issues either by increasing efficiency of the code, or storing the outputs about frequently queried users to allow for near-instantaneous serving.

