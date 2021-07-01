import argparse
from pathlib import Path
import re
import requests
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser(description='Download amino blogs in markdown format')
    parser.add_argument('-u', '--url', type=str, help='amino blog url')
    parser.add_argument('-f', '--file', type=str, help='urls list file')
    args = parser.parse_args()

    s = Scraper()
    if args.url: s.scrap(args.url)
    elif args.file: s.multi_scrap(args.file)

class Scraper:
    def __init__(self):
        self.current_file = None
        self.count = 0

    def multi_scrap(self, filename):
        file = open(filename, 'r')
        for url in file.readlines():
            self.scrap(url)
        file.close()

    def scrap(self, url):
        self.count += 1
        print(f'{self.count}) ', end='')

        req = requests.get(url)

        if req.status_code == 200:
            _root = BeautifulSoup(req.content, 'html.parser')
            _article = _root.select_one('article.main-post')

            title = _article.select_one('h1.title').text
            _author = _article.select_one('a.nickname')
            author_name = _author.select_one('span').text
            author_url = _author['href']
            date = _article.select_one('span.pretty-date').text

            title = re.sub(r"^\s+|\s+$", "", title)
            print(f'{title}... ', end='')

            if not Path('blogs').exists():
                Path.mkdir(Path('blogs'))

            self.current_file = open(f'blogs/{title}.md', 'w')

            metadata = {
                'title': title,
                'author_name': author_name,
                'author_url': author_url,
                'date': date,
                'url': url
            }

            self.write(self.gen_metadata(metadata))
            self.write(f'# {title}\n')

            _content = _article.select_one('div.post-content-toggle')
            for _node in _content.children:
                self.add(_node)

            self.current_file.close()
            print('OK')

    def write(self, text):
        self.current_file.write(text)

    def add(self, _node):
        self.write('\n')

        if _node.name == 'p':
            if _node.has_attr('class'):
                center = 'center' in _node['class']
                bold = 'bolder' in _node['class']
                italic = 'italic' in _node['class'] or 'underline' in _node['class']

                if center: self.write('<center>\n')
                if italic: self.write('*')
                if bold: self.write('**')

                self.write(_node.text)

                if italic: self.write('*')
                if bold: self.write('**')
                if center: self.write('\n</center>')
            else:
                self.write(_node.text)

        elif _node.name == 'div':
            if _node.has_attr('class'):
                center = 'center' in _node['class']
                if 'image-container' in _node['class']:
                    _img = _node.select_one('img.post-img')

                    self.write('<center>\n')
                    self.write(f"![](https:{_img['src']})")
                    self.write('\n</center>')

    def gen_metadata(self, data):
        return f"""---
    title: {data['title']}
    author: {data['author_name']}
    date: {data['date']}
    url: {data['url']}
    author_url: {data['author_url']}
---\n"""

if __name__ == '__main__':
    main()
