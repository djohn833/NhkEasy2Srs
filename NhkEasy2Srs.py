# Image or video: figure.article-main__figure
# Headline: h1.article-main__title
# Body paragraphs: div.article-main__body p

import requests
import sys
from bs4 import BeautifulSoup
from bs4.element import NavigableString

# articleUrl = 'https://www3.nhk.or.jp/news/easy/k10012766351000/k10012766351000.html'
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

  return expression, reading

def make_sentence_card(cards, sentenceSoup, headline=''):
  expression, reading = get_text(sentenceSoup)
  expression = expression.strip()
  reading = reading.strip()
  if not headline or len(headline) == 0:
    headline = expression
  cards.write("\t".join([expression, reading, headline, articleUrl]) + "\n")

  return expression, reading

def splitParagraphIntoSentences(paragraphText):
  sentences = []
  currSentence = ''
  numQuotes = 0

  for c in paragraphText:
    currSentence += c
    if c == '「':
      numQuotes += 1
    elif c == '」':
      numQuotes -= 1
    elif c == '。' and numQuotes == 0:
      sentences.append(currSentence)
      currSentence = ''

  if len(currSentence) > 0:
    sentences.append(currSentence)

  return sentences

with open('cards.tsv', 'a') as cards:
  title = soup.find('h1', class_='article-main__title')
  headline, _ = make_sentence_card(cards, title)

  for paragraph in soup.find(class_='article-main__body').find_all('p'):
    paragraphText = paragraph.encode_contents().decode('utf8')

    sentences = splitParagraphIntoSentences(paragraphText)

    for sentence in sentences:
      sentenceSoup = BeautifulSoup(sentence, 'html.parser')
      make_sentence_card(cards, sentenceSoup, headline)
