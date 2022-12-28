from gen_article import gen_article
from gen_summary import gen_summary

while True:
    try:
        print('Generating level 4 articles...')
        gen_article()
        print('Done generating level 4 articles!')

        #print('Generating level 4 summaries...')
        #gen_summary() # This is expected to have some false positives...
        #print('Done generating level 4 summaries!')

        # Redactle lied, some level 5 articles exist
        print('Generating level 5 articles...')
        gen_article(5)
        print('Done generating level 5 articles!')

        #print('Generating level 5 summaries...')
        #gen_summary(5)
        #print('Done generating level 5 summaries!')

        print('Proceed to main.py...')
        break
    except Exception as e:
        print(e, type(e))
        pass
