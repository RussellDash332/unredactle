import requests, wikipedia, os, re, warnings, asyncio, logging, aiofiles

EXISTING_REWRITTEN = False

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def warn(*args, **kwargs):
    pass
warnings.warn = warn

async def fetch_save_summary(article, path):
    try:
        async with aiofiles.open(path, 'wb+') as f:
            await f.write(wikipedia.summary(article).encode())
    except OSError as e:                                    logging.warning(f'OSError: Skipping... {e}')
    except wikipedia.exceptions.DisambiguationError as e:   logging.warning(f'Ambiguity, skipping... {article}')
    except Exception as e:                                  pass


async def fetch_save_async_summary(loop, articles):
    tasks = []
    for article in articles:
        path = os.path.join('summaries', article.replace('/', '-') + '.txt')
        if not EXISTING_REWRITTEN and os.path.exists(path): continue
        task = asyncio.ensure_future(fetch_save_summary(article, path))
        tasks.append(task)
    await asyncio.gather(*tasks)

def gen_summary(level=4):
    os.makedirs('summaries', exist_ok=True)
    src = f'https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/{level}'
    content = requests.get(src).content.decode()
    subtopics = re.findall(f'href="/wiki/Wikipedia:Vital_articles/Level/{level}/([^"]*)', content)
    for subtopic in sorted(set(subtopics)):
        subcontent = requests.get(src + '/' + subtopic).content.decode()
        articles = sorted(set(re.findall('href="/wiki/([^":]*)"', subcontent)))
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fetch_save_async_summary(loop, articles))
        loop.run_until_complete(future)
        logging.info(f'Done importing summaries from {subtopic}, got {len(articles)} such summaries!')
