import os
from datetime import datetime
from pyquery import PyQuery as pq

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

FILES_DIR = os.path.join(SCRIPT_DIR, '..', 'stockData')

# function to format url
def generate_url(code):
    """
    function to format the url for the stock quote that is
    reqeusted by the user

    return: string in the format of a web url
    """

    url = 'https://www.google.com/search?q={code}'.format(**{
        'code': code
    })

    return url


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

    # get the stock webpage data
    response = get_url_data(code=code)

    # create a pyquery object of the webpage data
    d = pq(response)

    i = 0
    # find the value wrapper
    spans = d('span')
    for span in spans:
        if span.find('b') is not None and span.find('cite') is not None:
            if i == 0:
                stock_value = pq(span).find('b').eq(0).text()
                i += 1

    return stock_value


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

if __name__ == '__main__':
    write_stock_data('AAPL')
