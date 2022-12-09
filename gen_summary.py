import requests, wikipedia, os, re

def gen_summary():
    os.makedirs('summaries', exist_ok=True)
    src = 'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/4'
    content = requests.get(src).content.decode()
    subtopics = re.findall('href="/wiki/Wikipedia:Vital_articles/Level/4/([^"]*)', content)
    for subtopic in sorted(set(subtopics)):
        subcontent = requests.get(src + '/' + subtopic).content.decode()
        articles = sorted(set(re.findall('href="/wiki/([^":]*)"', subcontent)))
        for article in articles:
            try:
                article = article.replace('/', '-')
                summary = wikipedia.summary(article)
                open(os.path.join('summaries', article + '.txt'), 'w+').write(summary)
            except:
                pass