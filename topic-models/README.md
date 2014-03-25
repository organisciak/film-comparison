Topic Modelling Film Titles
----------------------------

This thread is exploring the co-occurance patterns of movie titles in film review.

## Extract Titles from Review

extract_title.py extracts likely film title matches by looking for:
 * strings of one or more capitalized words, allowing word characters or apostrophes,
 * not at the start of a sentence,
 * with lowercase articles or short conjunctions allowed, provided that they do not occur at the start or end of the phrase.

These initial matches are filtered against:
 * an English language stoplist
 * a list of common English first names
 * a custom film specific stoplist

Optionally, one word titles are filtered out, weeding out many false positives at the expense of some false negatives

```
usage: extract_title.py [-h] [--no-singles] [infile] [outfile]

positional arguments:
  infile        Input file of Amazon review. Default is stdin.
  outfile       Output file for found titles. Default is stdout.

optional arguments:
  -h, --help    show this help message and exit
  --no-singles  Option to ignore single word matches. This option increases
                precision while losing recall.
```

### Issues

Stdin input doesn't register the end of the piped input, so it will keep listening forever.

## Log

```
 > bzcat ../data/movies.bz2 | python extract_titles.py --no-singles >all_titles2_noSingles.txt
 > bin/mallet import-file --input ~/film-comparison/topic-models/all_titles2_noSingles.txt --output movierefs.mallet --keep-sequence --token-regex '[\p{L}\p{M}\p{P}]+'
 > bin/mallet train-topics --input movierefs.mallet --num-topics 40 --output-state film-topic-state.gz --output-topic-keys film_keys.txt --output-doc-topics film_topics.txt --optimize-interval 20
```
