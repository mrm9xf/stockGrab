import os
import urllib2
import pandas as pd
from datetime import datetime
from pyquery import PyQuery as pq

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

FILES_DIR = os.path.join(SCRIPT_DIR, '..', 'stockData')

CONFIGS_DIR = os.path.join(SCRIPT_DIR, '..', 'configs')

# function to format url
def generate_url(code):
    """
    function to format the url for the stock quote that is
    reqeusted by the user

    return: string in the format of a web url
    """

    url = 'https://finance.google.com/finance?q=OTCMKTS%3A{code}'.format(**{
        'code': code
    })

    return url


def load_config():
    """
    function to load the file with all of the stock symbols

    return: list of stock symbols
    """

    dataframe = pd.read_csv(os.path.join(CONFIGS_DIR, 'companylist.csv'))

    return list(dataframe['Symbol'])


# function to grab the web data
def get_url_data(code):
    """

    """

    # format the url
    url = generate_url(code=code)

    return pq(url)


# function to open file
def write_file(code, data):
    """
    function to open a file and write the line of data
    """

    # open the file
    f = open(os.path.join(FILES_DIR, '{code}.csv'.format(**{'code': code})), 'a')

    # write the data
    f.write(data)

    # write a blank row
    f.write('\n')

    # close the file
    f.close()


# function to find the stock quote
def pull_stock_quote(code):
    """

    """

    # get the stock weebpage data
    try:
        response = get_url_data(code=code)
    except urllib2.HTTPError:
        sleep(15)
        response = get_url_data(code=code)


    # create a pyquery object of the webpage data
    d = pq(response)

    # find the value wrapper
    panel = d('div#price-panel')
    span = pq(panel).find('span:first')
    quote_span = pq(span).find('span:first')

    return quote_span.text()


def write_stock_data(code):
    """

    """

    # pull the quote
    quote = pull_stock_quote(code=code)

    # get the date today
    date_today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # prepare data string
    data_string = '{code},{datetime},{quote}'.format(**{
        'code': code,
        'datetime': date_today,
        'quote': quote
    })

    # write file
    write_file(code, data_string)


def gather_quotes(code_list=[]):
    """
    function to take a list of codes and write stock quotes to
    their respective CSV file
    """

    if len(code_list):
        for code_index, code in enumerate(code_list):
            code = code.replace(' ', '')
            try:
                write_stock_data(code)
            except UnboundLocalError:
                print(code)

            if code_index % 25 == 0:
                print('wrote {0} stock quotes, {1} most recently'.format(
                    str(code_index),
                    code
                ))

if __name__ == '__main__':
    #write_stock_data('AAPL')
    code_list = load_config()

    # process the stock qutoes
    gather_quotes(code_list)
