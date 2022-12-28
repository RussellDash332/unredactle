import requests, re, html2text, os, asyncio, logging, aiofiles
from aiohttp import ClientSession, ClientResponseError

EXISTING_REWRITTEN = False

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def clean_response(resp):
    html_text = html2text.html2text(resp.decode(), bodywidth=float('inf'))
    html_text = re.sub('\[([^\]]*)\]\([^\)]*\)', '\g<1>', html_text)
    html_text = re.sub('\[\d+\]', '', html_text)
    html_text = re.sub('\[[a-zA-Z]\]', '', html_text)
    html_text = re.sub('_([^_]*)_', '\g<1>', html_text)
    html_text = html_text.replace('\\(', '(').replace('\\)', ')').replace(')")', ')"')
    html_text = re.sub('!\[[^\]]*\]\([^\)]*\)', '', html_text)
    html_text = re.sub('\[edit\]', '', html_text)
    return html_text.encode()

async def fetch_save_article(session, url, path):
    try:
        async with session.get(url) as response:
            resp = await response.read()
            try:
                async with aiofiles.open(path, 'wb+') as f:
                    await f.write(clean_response(resp))
            except OSError as e:        print('Skipping...', e)
    except ClientResponseError as e:    logging.warning(e.code)
    except Exception as e:              logging.warning(e)
    else:                               return resp

async def fetch_save_async_article(loop, articles):
    tasks = []
    async with ClientSession() as session:
        for article in articles:
            path = os.path.join('articles', article.replace('/', '-') + '.txt')
            if not EXISTING_REWRITTEN and os.path.exists(path): continue
            task = asyncio.ensure_future(fetch_save_article(session, 'https://en.wikipedia.org/wiki/' + article, path))
            tasks.append(task)
        await asyncio.gather(*tasks)

def gen_article(level=4):
    os.makedirs('articles', exist_ok=True)
    src = f'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/{level}'
    content = requests.get(src).content.decode()
    subtopics = re.findall(f'href="/wiki/Wikipedia:Vital_articles/Level/{level}/([^"]*)', content)
    for subtopic in sorted(set(subtopics)):
        subcontent = requests.get(src + '/' + subtopic).content.decode()
        articles = sorted(set(re.findall('href="/wiki/([^":]*)"', subcontent)))
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fetch_save_async_article(loop, articles))
        loop.run_until_complete(future)
        logging.info(f'Done importing articles from {subtopic}, got {len(articles)} such articles!')
