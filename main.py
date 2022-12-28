import re, os, asyncio, aiofiles, concurrent.futures, random, logging, math
from collections import Counter

# Constants
BLOCK = '█'
USE_SUMMARY = False

# Utility functions
def search_title(fn, prompt, results):
    search_result = re.findall(prompt, fn.strip('.txt').replace('_', ' '))
    if search_result:
        results.append(search_result[0] if len(search_result) == 1 else search_result)

async def search_body(fn, prompt, results):
    async with aiofiles.open(fn, 'rb') as f:
        contents = await f.readlines()
    result = re.findall(prompt, '\n'.join(map(lambda x: x.decode(), contents)))
    if result:
        print(fn.strip('.txt').split(os.sep)[1].ljust(30), Counter(result))

# Main
async def main():
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            mode = int(input('Search title only or whole article? (1 or 2)\n'))
            if mode in [1, 2]: break
        except:
            continue

    results = []
    if mode == 1:
        prompt = '^' + input('Input your Redactle regex prompt: ').replace(BLOCK, '[^ ]') + '$'
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(lambda x: search_title(x, prompt, results), os.listdir('articles'))
        for result in sorted(results):
            print(result)
    if mode == 2:
        prompt = '\w*' + input('Input your Redactle prompt: ').replace(BLOCK, '\w')
        # Might take a while :)
        dirs = ['articles']
        if USE_SUMMARY: dirs.append('summaries')
        for directory in dirs:
            articles = os.listdir(directory)
            random.shuffle(articles) # >:)
            # Too many files in a single asyncio.gather will result in an OSError? 1000 is a limit?
            N = len(articles)
            SPLIT = math.ceil(N/1000)
            N /= SPLIT

            splitted_articles = [articles[int(i*N):int((i+1)*N)] for i in range(SPLIT)]
            for i, split in enumerate(splitted_articles):
                logging.info(f'{directory}: Split {i+1}/{SPLIT}')
                tasks = [asyncio.ensure_future(search_body(os.path.join(directory, x), prompt, results)) for x in split]
                await asyncio.gather(*tasks)

    input('Press enter to quit...')

if __name__ == '__main__':
    asyncio.run(main())
