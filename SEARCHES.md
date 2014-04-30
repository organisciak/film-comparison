# Search against a file that has movie names
## Add review/text to grep file, to match proper lines.
perl -pe "s:^:review\\\/text.*:" 200-films.txt >200-films-grep.txt
bzgrep --ignore-case --before-context=7 -f 200-films-grep.txt sample.bz2 >matched-sample.txt

# Replace all film matches with capital letters
## TO understand this, here's an example:
##   echo "THis is a test" | perl -pe "s:(Test):\U\1\E:gi"
## This matches case-insensitive (the 'i' at the end) 'Test', and replaces it will all uppercase \U...\E of the captured pattern 
films=`perl -pe "chomp if eof;s:\n:|:g" 200-films.txt`
perl -pe -i "s:($films):\*\*\*\U\1\E\*\*\*:gi" matched-sample.txt


# Grepping out lines that include most common names

## download a csv of popular names and pull out just the names
wget https://raw.github.com/hadley/data-baby-names/master/baby-names.csv
cat baby-names.csv | perl -pe "s:^.*?\"(.*?)\".*:\1:" | tail -n +2 | head -n 50 > baby-names.txt



#####################
For exploring:

p="(similar to|like|mix of) .{3,10} and .*? "; perl -ne "print if
 s/($p)/\*\*\*\U\1\E\*\*\*/g" <(bzcat data/movies.bz2 | tr "[:upper:]" "[:l
ower:]") | less 

# Pull out sentences

bzgrep -Po "(?<=(\.|\:|\!|\?) ).{0,120}?-esque.*?(\.|\!|\?)" x-ian_x-esque.txt.bz2 | bzip2 -c >esque-sentences.bz2 
