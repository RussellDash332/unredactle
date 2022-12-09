import re, os
from collections import Counter

BLOCK = '█'

while True:
    try:
        mode = int(input('Search title only or whole article? (1 or 2)\n'))
        if mode in [1, 2]: break
    except:
        continue

if mode == 1:
    prompt = input('Input your Redactle regex prompt: ').replace(BLOCK, '\w')
    for fn in os.listdir('articles'):
        search_result = re.findall(prompt, fn.strip('.txt').replace('_', ' '))
        if search_result:
            print(search_result[0] if len(search_result) == 1 else search_result)
if mode == 2:
    prompt = '\w*' + input('Input your Redactle prompt: ').replace(BLOCK, '\w')
    for fn in os.listdir('articles'):
        search_result = re.findall(prompt, '\n'.join(map(lambda x: x.decode(), open(os.path.join('articles', fn), 'rb').readlines())))
        try:
            search_result_summary = re.findall(prompt, '\n'.join(map(lambda x: x.decode(), open(os.path.join('summaries', fn), 'rb').readlines())))
        except:
            search_result_summary = None
        for result in [search_result, search_result_summary]:
            if result:
                print(fn.strip('.txt').ljust(30), Counter(result))

input('Press enter to quit...')
