import wikipedia, os

def gen_summary():
    os.makedirs('summaries', exist_ok=True)
    for fn in os.listdir('articles'):
        try:
            summary = wikipedia.summary(fn.strip('.txt'))
            open(os.path.join('summaries', fn), 'w+').write(summary)
        except:
            pass