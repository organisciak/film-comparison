import argparse
import sys
import re
from nltk.corpus import stopwords

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="Input file of Amazon review. Default is stdin.")
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, 
                        help="Output file for found titles. Default is stdout.")
    parser.add_argument('--no-singles', action='store_true', 
                        help="Option to ignore single word matches. This option increases precision while losing recall.")

    args = parser.parse_args()

    current_film = None
    current_user = None
    title_parser = TitleParser()

    for line in args.infile:
        line = line.rstrip()
        
        # Check if a new film has been added
        if line[0:18] == r"product/productId:":
            current_film = line[19:]
        if line[0:14] == r"review/userId:":
            current_user = "%s/%s" % (current_film, line[15:])
        # Find likely titles in review
        elif line[0:12] == r"review/text:":
            review = line[13:]
            titles = title_parser.parse(review, args.no_singles)
            if len(titles) > 0:
                tokens = [re.sub(' ', '_', title) for title in titles]
                out = "%s\t%s\t%s\n" % (current_user, current_film, " ".join(tokens))
                args.outfile.write(out)


class TitleParser:
    # The Super-duper magic regex for matching titles:
    # strings of one or more capital-case words, not following
    # Another sentence, with up to 2 lowercase articles and inconjugates
    # allowed in the middle, but not beginning or end
    TITLE_MATCH = re.compile('''((?<!(\.|\!|\?) )(([A-Z][\w']+|I)(( (the|on|from|to|and|of|a)){0,2}( [A-Z][\w']+|I)+)*))(?=[\s\.\!\?$])''')
    TITLE_MATCH_LONGER = re.compile('''((?<!(\.|\!|\?) )(([A-Z][\w']+|I)(( (the|on|from|to|and|of|a)){0,2}( [A-Z][\w']+|I)+)+))(?=[\s\.\!\?$])''')
    
    def __init__(self):
        stoplist = stopwords.words('english')

        # add custom words to stoplist
        stoplist += ['it\'s', 'i\'ve', 'also', 'i\'ll', 'let\'s']
        film_stoplist = ['hd dvd', 'this dvd', 'the dvd', 'dolby digital']
        stoplist += film_stoplist

        names_file = open('/data/datasets/reference/english-names.txt')
        self.names = [name.strip().lower() for name in names_file.readlines()]

        ## Add person names to stoplist
        stoplist += self.names
        self.stoplist = stoplist

    # Extra filtering of false positives, by heristics
    def filter(self, match, min_length=4):
        # Remove stoplist
        if match.lower() in self.stoplist:
            return None
        #Remove short words. 
        if len(match) < min_length:
            return None

        return match

    def match_first_names(self, match):
        first_word = match.split(" ")[0]
        if first_word.lower() in self.names:
            return None
        else:
            return match

    def parse(self, review, no_singles=True):
        if no_singles is True:
            titles_raw = self.TITLE_MATCH_LONGER.findall(review)
        else:
            titles_raw = self.TITLE_MATCH.findall(review)
        titles = [title[0] for title in titles_raw]
        # Extra step for false positives
        titles = [self.filter(title) for title in titles]
        titles = [title for title in titles if title]
        # Strip out matches that have a proper first name
        titles = [self.match_first_names(title) for title in titles]
        titles = [title for title in titles if title]
        return titles


if __name__=='__main__':
    main()
