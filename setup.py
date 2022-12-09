from gen_article import gen_article
from gen_summary import gen_summary

print('Generating articles...')
gen_article()
print('Done generating articles!')
print('Generating summaries...')
gen_summary() # This is expected to have some false positives...
print('Done generating summaries! Proceed to main.py...')