'''
MALLET requires an ordered feature stream for baffling reason, so this script reads 
a file ordered in SVM-light format and similar writes out the features X number of times.

Bizarre, I know. Neater to just fix Mallet in the long term, but this hack will do for now.

'''

infile = open('tags_for_mallet.dat', 'r')

for line in infile.readlines():
    items = line.split(" ")
    out = items[0]
    for featurecount in items[1:]:
        f = featurecount.split(":")
        out += " " + " ".join([f[0]] * int(f[1]))
    print out
