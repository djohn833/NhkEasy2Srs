# Image or video: figure.article-main__figure
# Headline: h1.article-main__title
# Body paragraphs: div.article-main__body p

import requests
import sys
from bs4 import BeautifulSoup
from bs4.element import NavigableString

# articleUrl = 'https://www3.nhk.or.jp/news/easy/k10012766351000/k10012766351000.html
articleUrl = sys.argv[1]

r = requests.get(articleUrl)
soup = BeautifulSoup(r.content, 'html.parser')

def get_text(soup):
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

  expression = expression.strip()
  reading = reading.strip()
  return expression, reading

def make_sentence_card(cards, sentenceSoup, headline=''):
  try:
    expression, reading = get_text(sentenceSoup)
    if not headline or len(headline) == 0:
      headline = expression
    cards.write("\t".join([expression, reading, headline, articleUrl]) + "\n")

    return expression, reading
  except:
    print(sentenceSoup)

with open('cards.tsv', 'a') as cards:
  title = soup.find('h1', class_='article-main__title')
  headline, _ = make_sentence_card(cards, title)

  for paragraph in soup.find(class_='article-main__body').find_all('p'):
    for sentenceBytes in paragraph.encode_contents().split(bytes('。', 'utf8')):
      if len(sentenceBytes) > 0:
        sentence = sentenceBytes.decode('utf8') + '。'
        sentenceSoup = BeautifulSoup(sentence, 'html.parser')
        make_sentence_card(cards, sentenceSoup, headline)