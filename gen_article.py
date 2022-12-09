import requests, re, html2text, os

EXISTING_REWRITTEN = False

def gen_article():
    os.makedirs('articles', exist_ok=True)
    src = 'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4'
    content = requests.get(src).content.decode()
    subtopics = re.findall('href="/wiki/Wikipedia:Vital_articles/Level/4/([^"]*)', content)
    for subtopic in sorted(set(subtopics)):
        subcontent = requests.get(src + '/' + subtopic).content.decode()
        articles = sorted(set(re.findall('href="/wiki/([^":]*)"', subcontent)))
        for article in articles:
            path = os.path.join('articles', article.replace('/', '-') + '.txt')
            if not EXISTING_REWRITTEN and os.path.exists(path): continue
            html_text = html2text.html2text(requests.get('https://en.wikipedia.org/wiki/' + article).content.decode(), bodywidth=float('inf'))
            html_text = re.sub('\[([^\]]*)\]\([^\)]*\)', '\g<1>', html_text)
            html_text = re.sub('\[\d+\]', '', html_text)
            html_text = re.sub('\[[a-zA-Z]\]', '', html_text)
            html_text = re.sub('_([^_]*)_', '\g<1>', html_text)
            html_text = html_text.replace('\\(', '(').replace('\\)', ')').replace(')")', ')"')
            html_text = re.sub('!\[[^\]]*\]\([^\)]*\)', '', html_text)
            html_text = re.sub('\[edit\]', '', html_text)
            open(path, 'wb+').write(html_text.encode())
        print(f'Done importing articles from {subtopic}, got {len(articles)} such articles!')