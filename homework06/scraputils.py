import bs4.element
import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    table = parser.findAll('table')[2].findAll('tr')

    for i in range(0, len(table)-3, 3):
        newstr = table[i:i+3]
        try:
            comments = newstr[1].findAll('a')[3].getText()
            comments = int(comments[:comments.find(' ')])
        except IndexError:
            comments = 0
        except ValueError:
            comments = 0
        try:
            points = newstr[1].findAll('span')[0].getText()
            points = int(points[:points.find(' ')])
        except IndexError:
            points = 0
        except ValueError:
            points = 0
        newsel = {'author': newstr[1].findAll('a')[0].getText(),
                  'comments': comments,
                  'points': points,
                  'title': newstr[0].findAll('a')[1].getText(),
                  'url': newstr[0].findAll('a')[1].get('href')}
        news_list.append(newsel)

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """

    return parser.findAll('table')[2].findAll('a')[-1].get('href')


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

