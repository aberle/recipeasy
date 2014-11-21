from bs4 import BeautifulSoup
import urllib2
from random import choice,randint
from pymongo import MongoClient

url = 'http://foodgawker.com/page/1/?s_exclude=drinks'
request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
site = urllib2.urlopen(request)
html = site.read()

parsed_html = BeautifulSoup(html)
maxpage = int(parsed_html.body.find('div', attrs={'class' : 'post-section'}).attrs['data-maxpage'])

for x in xrange(1, maxpage):

    url = 'http://foodgawker.com/page/' + str(x) + '/?s_exclude=drinks'
    request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
    site = urllib2.urlopen(request)
    html = site.read()

    parsed_html = BeautifulSoup(html)

    dishes = parsed_html.body.find_all('div', attrs={'class' : 'flipwrapper'})

    client = MongoClient('localhost', 27017)
    db = client.recipeasy
    collection = db.recipes
    recipes = db.recipes

    for dish in dishes:
        img = dish.find('a', attrs={'class' : 'picture-link'})

        recipe = { 'title' : dish.attrs['data-sharetitle'],
                   'description' : dish.find('section', attrs={'class' : 'description'}).text,
                   'link' : img.attrs['href'],
                   'image' : img.find('img').attrs['src'] }

        recipes.insert(recipe)

    amtDone = float(x)/float(maxpage)
    print("\rProgress: [{0:100s}] {1:.1f}% ({2}/{3})".format('#' * int(amtDone * 50), amtDone * 100, x, maxpage)),