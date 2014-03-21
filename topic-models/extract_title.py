import argparse
import sys
import re
from nltk.corpus import stopwords

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)

    args = parser.parse_args()

    current_film = None
    title_parser = TitleParser()

    for line in args.infile.readlines():
        line = line.rstrip()
        
        # Check if a new film has been added
        if line[0:18] == r"product/productId:":
            current_film = line[19:]
        # Find likely titles in review
        elif line[0:12] == r"review/text:":
            review = line[13:]
            titles = title_parser.parse(review)
            if len(titles) > 0:
                print titles


class TitleParser:
    # The Super-duper magic regex for matching titles:
    # strings of one or more capital-case words, not following
    # Another sentence, with up to 2 lowercase articles and inconjugates
    # allowed in the middle, but not beginning or end
    TITLE_MATCH = re.compile('''((?<!(\.|\!|\?) )(([A-Z][\w']+|I)(( (the|on|from|to|and|of|a)){0,2}( [A-Z][\w']+|I)+)*))(?=[\s\.\!\?$])''')
    
    def __init__(self):
        stoplist = stopwords.words('english')

        # add custom words to stoplist
        stoplist += ['it\'s', 'i\'ve', 'also']

        names_file = open('/data/datasets/reference/english-names.txt')
        names = [name.strip().lower() for name in names_file.readlines()]

        ## Add person names to stoplist
        stoplist += names
        self.stoplist = stoplist

    # Extra filtering of false positives, by heristics
    def filter(self, match):
        # Remove stoplist
        if match.lower() in self.stoplist:
            return None
        #Remove short words. 
        if len(match) <= 3:
            return None
        return match

    def parse(self, review):
        titles_raw = self.TITLE_MATCH.findall(review)
        titles = [title[0] for title in titles_raw]
        # Extra step for false positives
        titles = [self.filter(title) for title in titles]
        titles = [title for title in titles if title]
        return titles


if __name__=='__main__':
    main()
