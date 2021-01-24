import pandas as pd
import itertools
import snscrape.modules.twitter as sntwitter

from analysis import tickers_in_tweet, ticker_ESG, ESG_avg_function, stock_return_since_mention
from extension_interface import get_twitter_handle
from gcloud_api import stock_tweet_classifier


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
    date_df = tweet_df['date'].dt.date
    sum_stock_return = 0
    no_data_counter = 0
    for i in tweet_df.index:
        new_tickers = tickers_in_tweet(tweet_df['content'][i])
        tickers_list += new_tickers
        # If a tweet is added to the list calculate stock returns for this batch of stocks
        if new_tickers != []:
            date = str(date_df[i])
            for j in range(len(new_tickers)):
                ticker = new_tickers[j]
                try:
                    stock_return = stock_return_since_mention(ticker, date)
                except IndexError:
                    stock_return = 0
                    no_data_counter += 1
                sum_stock_return += stock_return

    # Create dict containing all companies mentioned (key), and the frequency (value)
    ticker_dict = {}
    for i in range(len(tickers_list)):
        try:
            ticker_dict[tickers_list[i]] += 1
        except KeyError:
            ticker_dict[tickers_list[i]] = 1

    return ticker_dict, sum_stock_return, no_data_counter


def tweet_workflow():
    """Main function for the python backend"""
    # Get twitter handle from Chrome Extension
    #handle = get_twitter_handle()
    handle = "MadsC007"

    # Scrape for the user's most recent tweets
    raw_tweets_df = twitter_scrape(handle=handle, num_tweet=30) # Returns dataframe

    # Tweet processing
    # Stock tweet filter
    stock_df_rows = []
    # for row, tweet in enumerate(raw_tweets_df['content']):
    #     is_stock = stock_tweet_classifier(tweet)
    #
    #     if is_stock:
    #         stock_df_rows.append(row)
    stock_tweets = raw_tweets_df.iloc[stock_df_rows]

    # Sentiment filter

    # Extract stock tickers
    ticker_dict, sum_stock_returns, no_data_counter = gather_tickers(raw_tweets_df)

    # Stock ticker analysis
    if not ticker_dict:  # If no tickers were found in the tweets
        most_tweeted_company = "N/A"
        number_of_mentions = "N/A"
        ESG_most_tweeted_company = "N/A"
        ESG_avg = "N/A"
        average_return = "N/A"
    else:
        # Most tweeted company and number of mentions
        most_tweeted_company = max(ticker_dict, key=ticker_dict.get)
        number_of_mentions = ticker_dict[most_tweeted_company]
        ESG_most_tweeted_company = ticker_ESG(most_tweeted_company)
        average_return = sum_stock_returns/(number_of_mentions - no_data_counter)

        try:  # If no ESG ratings are available for all companies
            ESG_avg = ESG_avg_function(ticker_dict)
        except ZeroDivisionError:
            ESG_avg = "This person has not tweeted about any ESG-rated companies!"

    # Send to Chrome Extension


    return str(most_tweeted_company), str(number_of_mentions), str(ESG_most_tweeted_company), str(
        ESG_avg), str(average_return)  # , ticker_dict

    #return True


if __name__ == "__main__":
    print(tweet_workflow())
