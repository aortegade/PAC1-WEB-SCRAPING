from datetime import datetime
from scraping import GetContent
from selenium.common.exceptions import WebDriverException

if __name__ == '__main__':
    begin = datetime.now().strftime("[%H:%M:%S]")
    print("{} Scraping cryptos".format(begin))
    try:
        GetContent()

        end = datetime.now().strftime("[%H:%M:%S]")
        print("{} Scraping ended successfully!".format(end))

    except WebDriverException as e:
        err_time = datetime.now().strftime("[%H:%M:%S]")
        print(err_time, e.__class__, "occurred!")