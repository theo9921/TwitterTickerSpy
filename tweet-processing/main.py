import pandas as pd
import itertools
import snscrape.modules.twitter as sntwitter

from analysis import tickers_in_tweet, ticker_ESG, ESG_avg_function
from extension_interface import get_twitter_handle


def twitter_scrape(handle, num_tweet):
    """
    Input:  1) handle: Twitter handle of a person without '@' (e.g. JoeBiden)
            2) num_tweet: The number of past tweets the analysis will be based on (e.g. 100)

    Outputs: 1) Dataframe containing scraped tweets
    """
    raw_tweet_df = pd.DataFrame(
        itertools.islice(sntwitter.TwitterSearchScraper('from: ' + handle).get_items(), num_tweet))

    return raw_tweet_df


def gather_tickers(tweet_df):
    """
    Input:   1) Dataframe of tweets to be analysed

    Outputs: 1) most_tweeted_company: The company this person has tweeted most times
             2) ESG_most_tweeted_company: The ESG score of the company mentioned above
             3) avg_esg: The average ESG score by all company this person has mentioned
               (weighted by number of mentions)
    """
    # gathers list of all tickers mentioned in all tweets
    tickers_list = []
    for i in range(len(tweet_df)):
        tickers_list += tickers_in_tweet(tweet_df['content'][i])

    # Create dict containing all companies mentioned (key), and the frequency (value)
    ticker_dict = {}
    for i in range(len(tickers_list)):
        try:
            ticker_dict[tickers_list[i]] += 1
        except KeyError:
            ticker_dict[tickers_list[i]] = 1

    return ticker_dict


def tweet_workflow():
    """Main function for the python backend"""
    # Get twitter handle from Chrome Extension
    handle = get_twitter_handle()

    # Scrape for the user's most recent tweets
    raw_tweets = twitter_scrape(handle=handle, num_tweet=30)

    # Tweet processing


    # Extract stock tickers
    ticker_dict = gather_tickers(raw_tweets)

    # Stock ticker analysis
    if not ticker_dict:  # If no tickers were found in the tweets
        most_tweeted_company = "N/A"
        number_of_mentions = "N/A"
        ESG_most_tweeted_company = "N/A"
        ESG_avg = "N/A"
    else:
        # Most tweeted company and number of mentions
        most_tweeted_company = max(ticker_dict, key=ticker_dict.get)
        number_of_mentions = ticker_dict[most_tweeted_company]
        ESG_most_tweeted_company = ticker_ESG(most_tweeted_company)

        try:  # If no ESG ratings are available for all companies
            ESG_avg = ESG_avg_function(ticker_dict)
        except ZeroDivisionError:
            ESG_avg = "This person has not tweeted about any ESG-rated companies!"

    # Send to Chrome Extension


    return str(most_tweeted_company), str(number_of_mentions), str(ESG_most_tweeted_company), str(
        ESG_avg)  # , ticker_dict

    #return True


if __name__ == "__main__":
    print(tweet_workflow())
