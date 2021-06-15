from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier, clean


def back():
    if request.query.back == "classify":
        redirect("/classify")
    else:
        redirect("/news")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id = request.query.id
    s = session()
    s.query(News).filter(News.id == id).update({"label": label})
    s.commit()
    back()


@route("/update")
def update_news():
    news_recs = get_news("https://news.ycombinator.com/", 15)
    a = [News(title=i['title'],
              author=i['author'],
              url=i['url'],
              comments=i['comments'],
              points=i['points']) for i in news_recs]
    s = session()
    for i in a:
        if len(s.query(News).filter(News.author == i.author).filter(News.title == i.title).all()) == 0:
            s.add(i)
    s.commit()
    back()


@route("/classify")
def classify_news():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    model = NaiveBayesClassifier(1)
    model.fit([clean(i.title) for i in rows], [i.label for i in rows])
    rows = s.query(News).filter(News.label == None).all()
    p, a, n = [], [], []
    pf, af, nf = [], [], []
    for i in rows:
        c, f = model.predict(clean(i.title))
        if c == "good":
            p.append((i, f))
        elif c == "never":
            n.append((i, f))
        else:
            a.append((i, f))
    p.sort(key=lambda x: x[1])
    n.sort(key=lambda x: -x[1])
    s.commit()
    return template('news_recom', positive=p, active=a, negative=n)


if __name__ == "__main__":
    run(host="localhost", port=8080)
