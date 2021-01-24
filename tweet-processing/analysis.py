"""Contains functions related to scraping and analysis of tweets"""

import pandas as pd
import itertools
import snscrape.modules.twitter as sntwitter
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import yfinance as yf
import datetime


def tickers_in_tweet(tweet):
    """ Input: A single tweet as a string

        Output: A list of all the tickers mentioned

        Will return a ticker if there's 2, 3, or 4 capital
        letters preceeded by a '$' and not followed by a capital letter.
    """
    tickers = []
    for i in range(len(tweet) - 4):
        if tweet[i] == '$':
            if tweet[i + 1].isalpha():
                if tweet[i + 2].isalpha():
                    if not tweet[i + 3].isalpha():
                        tickers.append(tweet[i + 1] + tweet[i + 2])
                    if tweet[i + 3].isalpha():
                        if not tweet[i + 4].isalpha():
                            tickers.append(tweet[i + 1] + tweet[i + 2] + tweet[i + 3])
                        if tweet[i + 4].isalpha():
                            tickers.append(tweet[i + 1] + tweet[i + 2] + tweet[i + 3] + tweet[i + 4])
    return tickers


def ticker_ESG(ticker):
    """This function accepts a ticker input and outputs its Total ESG Risk Score"""
    # Generate URL
    working_url = 'https://uk.finance.yahoo.com/quote/' + str(ticker).upper() + '/sustainability?p=' + str(
        ticker).upper()
    total_ESG = _scrape_yahoo(working_url)
    return total_ESG


def _scrape_yahoo(url):
    """This function checks and accepts a Yahoo finance URL and outputs the Total ESG Risk Score as an int """

    # GET page and convert content to bs4 soup
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find class containing ESG risk score from 0-100, cast to string
    total_ESG = str(soup.findAll('div', {"class": "Fz(36px) Fw(600) D(ib) Mend(5px)"}))

    # Extract ESG score using regex, with error handling
    if total_ESG != '[]':
        total_ESG = int(re.search('data-reactid="20">(.+?)</div>', total_ESG).group(1))
    else:
        total_ESG = None

    return total_ESG


def ESG_avg_function(dictionary):
    """
    Input: dictionary with tickers as keys and number of mentions as values
    Output: average ESG score, weighted according to the number of mentions
    """
    # Numerator = sum(ESG-score * number of mentions)
    # The sum is over all companies which have an ESG score\

    numerator = 0
    total_mentions = 0

    keys_list = list(dictionary)

    for i in range(len(keys_list)):
        ESG_score = ticker_ESG(keys_list[i])
        if not ESG_score == None:
            numerator += ESG_score * dictionary[keys_list[i]]
            total_mentions += dictionary[keys_list[i]]

    ESG_avg = numerator / total_mentions

    return ESG_avg


def stock_price_today(ticker):
    """
    Input: ticker of a stock (as string)
    Returns the stock price of that stock today
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    stock = yf.Ticker(ticker)
    price = stock.history(start='2021-01-01', end=now)
    price_today = price['Close'][-1]

    return price_today


def stock_price_at_date(ticker, date):
    """
    Inputs: 1) ticker of a stock (as string)
            2) Date you want the stock price for (format: 'YYYY-MM-DD')
    Returns the stock price of that ticker for that day (or closest to)
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    stock = yf.Ticker(ticker)
    price = stock.history(start=date, end=now)
    price_date = price['Close'][0]

    return price_date


def stock_return_since_mention(ticker, date):
    """
    Input:  Ticker
            Date the stock was mentioned (format: 'YYYY-MM-DD')
    Output: Stock return since it was mentioned
    """
    price_today = stock_price_today(ticker)
    price_date = stock_price_at_date(ticker, date)


    stock_return = (price_today - price_date) / price_date
    return stock_return