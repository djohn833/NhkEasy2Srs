# Image or video: figure.article-main__figure
# Headline: h1.article-main__title
# Body paragraphs: div.article-main__body p

from contextlib import redirect_stdout
from dataclasses import dataclass
import requests
import sys
from bs4 import BeautifulSoup
from bs4.element import NavigableString


# articleUrl = 'https://www3.nhk.or.jp/news/easy/k10012766351000/k10012766351000.html'
articleUrl = sys.argv[1]


r = requests.get(articleUrl)
soup = BeautifulSoup(r.content, 'html.parser')


@dataclass
class Card:
  expression: str
  reading: str
  headline: str
  articleUrl: str

  def __str__(self):
    return "\t".join([self.expression, self.reading, self.headline, self.articleUrl])


def get_text(soup: BeautifulSoup):
  expression = ''
  reading = ''

  for node in soup.children:
    if node.name == 'ruby':
      expression += node.contents[0].string
      reading += ' ' + node.contents[0].string + '[' + node.rt.string + ']'
    elif node.name:
      expr, read = get_text(node)
      expression += expr
      reading += read
    else:
      expression += node.string
      reading += node.string

  return expression, reading


def make_sentence_card(sentenceSoup: BeautifulSoup, headline: str =''):
  expression, reading = get_text(sentenceSoup)
  expression = expression.strip()
  reading = reading.strip()
  if not headline or len(headline) == 0:
    headline = expression
  return Card(expression, reading, headline, articleUrl)


def sentencesFromParagraph(paragraphText: str):
  sentence = ''
  numQuotes = 0

  for c in paragraphText:
    sentence += c

    if c == '「':
      numQuotes += 1
    elif c == '」':
      numQuotes -= 1
    elif c == '。' and numQuotes == 0:
      yield sentence
      sentence = ''

  if len(sentence) > 0:
    yield sentence


def sentencesFromParagraphs(soup: BeautifulSoup):
  for p in soup.find(class_='article-main__body').find_all('p'):
    text = p.encode_contents().decode('utf8')
    for sentence in sentencesFromParagraph(text):
      yield sentence


def soupFromParagraphs(soup: BeautifulSoup):
  for sentence in sentencesFromParagraphs(soup):
    yield BeautifulSoup(sentence, 'html.parser')


def cardsFromParagraphs(soup: BeautifulSoup, headline: str):
  for sentenceSoup in soupFromParagraphs(soup):
    yield make_sentence_card(sentenceSoup, headline)


def cardFromTitle(soup: BeautifulSoup):
  title = soup.find('h1', class_='article-main__title')
  return make_sentence_card(title)


def cardsFromPage(soup: BeautifulSoup):
  headlineCard = cardFromTitle(soup)
  headline = headlineCard.expression
  yield headlineCard

  for card in cardsFromParagraphs(soup, headline):
    yield card


with open('cards.tsv', 'a') as f:
  with redirect_stdout(f):
    for card in cardsFromPage(soup):
      print(card)
