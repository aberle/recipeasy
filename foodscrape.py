from bs4 import BeautifulSoup
import urllib2
from random import choice,randint

url = 'http://foodgawker.com/page/1/?s_exclude=drinks&cats_inc%5B0%5D=No+Desserts'
request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
site = urllib2.urlopen(request)
html = site.read()

parsed_html = BeautifulSoup(html)
maxpage = int(parsed_html.body.find('div', attrs={'class' : 'post-section'}).attrs['data-maxpage'])

new_page = str(randint(1, maxpage))

url = 'http://foodgawker.com/page/' + new_page + '/?s_exclude=drinks&cats_inc%5B0%5D=No+Desserts'
request = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'})
site = urllib2.urlopen(request)
html = site.read()

parsed_html = BeautifulSoup(html)

dishes = parsed_html.body.find_all('div', attrs={'class' : 'flipwrapper'})

chosen = choice(dishes)

'''print chosen.attrs['data-sharetitle']
print chosen.find('section', attrs={'class' : 'description'}).text'''
img = chosen.find('a', attrs={'class' : 'picture-link'})
'''print img.attrs['href']
print img.find('img').attrs['src']'''

recipe = { 'title' : chosen.attrs['data-sharetitle'],
		   'description' : chosen.find('section', attrs={'class' : 'description'}).text,
		   'link' : img.attrs['href'],
		   'image' : img.find('img').attrs['src']
		   }

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.recipeasy
collection = db.recipes

recipes = db.recipes
recipes.insert(recipe)