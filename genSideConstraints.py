# -*- coding: utf-8 -*-

from collections import defaultdict
import os.path
import random
import sys

def addTags(lines, t):
    olines = []
    for tag in t:
        for line in lines:
            myline = list(line)
            myline.append(tag)
            if myline in olines: continue ### avoid repetitions
            olines.append(myline)
    return olines

def getTag(tag):
    i = tag.find(':')
    name = tag[1:i]
    val = tag[i+1:-1]
    #print (tag,name,val)
    return name, val, val.islower()

def genTags(tags, snoun, sverb, sadj, mood, tense, ndiff, originals, verbose):
    lines = [[]]
    for tag in tags:
        name, val, is_lowercase = getTag(tag)

        if verbose: sys.stdout.write('curr tag is {} value is {} is_lowercase is {}\n'.format(name, val, is_lowercase))

        if name == 'noun':
            t = []
            t.append(tag)
            if val.lower() != 'x':
                if verbose: sys.stdout.write('generating noun {}\n'.format(val))
                for s in range(snoun):
                    if is_lowercase:
                        k = chr(ord('a') + s)
                    else:
                        k = chr(ord('A') + s)
                    t.append('<noun:'+k+'>')
            lines = addTags(lines, t)

        elif name == 'verb':
            t = []
            t.append(tag)
            if val.lower() != 'x':
                if verbose: sys.stdout.write('generating verb {}\n'.format(val))
                for s in range(sverb):
                    if is_lowercase:
                        k = chr(ord('a') + s)
                    else:
                        k = chr(ord('A') + s)
                    t.append('<verb:'+k+'>')
            lines = addTags(lines, t)

        elif name == 'adj':
            t = []
            t.append(tag)
            if val.lower() != 'x':
                if verbose: sys.stdout.write('generating adj {}\n'.format(val))
                for s in range(sadj):
                    if is_lowercase:
                        k = chr(ord('a') + s)
                    else:
                        k = chr(ord('A') + s)
                    t.append('<adj:'+k+'>')
            lines = addTags(lines, t)

        elif name == 'mood':
            t = []
            t.append(tag)
            if val.lower() != 'x':
                if verbose: sys.stdout.write('generating mood {}\n'.format(val))
                if is_lowercase:
                    t.append('<mood:i>')
                    t.append('<mood:s>')
                    t.append('<mood:m>')
                    t.append('<mood:p>')
                    t.append('<mood:g>')
                    t.append('<mood:n>')
                else:
                    t.append('<mood:I>')
                    t.append('<mood:S>')
                    t.append('<mood:M>')
                    t.append('<mood:P>')
                    t.append('<mood:G>')
                    t.append('<mood:N>')
            lines = addTags(lines, t)

        elif name == 'tense':
            if verbose: sys.stdout.write('generating tense {}\n'.format(val))
            t = []
            t.append(tag)
            if val.lower() != 'x':
                if is_lowercase:
                    t.append('<tense:p>')
                    t.append('<tense:i>')
                    t.append('<tense:f>')
                    t.append('<tense:s>')
                    t.append('<tense:c>')
                else:
                    t.append('<tense:P>')
                    t.append('<tense:I>')
                    t.append('<tense:F>')
                    t.append('<tense:S>')
                    t.append('<tense:C>')
            lines = addTags(lines, t)

        else:
            sys.stderr.write('warning: unkown tag {}\n'.format(tag))
           
    initial = lines.pop(0) ### get rid of the original sequence of tags
    if verbose: sys.stdout.write('#different tag-sets = {}\n'.format(len(lines)))

    list_tags = []
    for line in lines:
        list_tags.append(' '.join(line))

    if ndiff > 0 and len(list_tags) > ndiff: 
        random.shuffle(list_tags) ### shuffles list_tags
        list_tags = list_tags[:ndiff] ### get ndiff sequences of tags

    if originals:
        list_tags.insert(0,' '.join(initial)) #### if used the original is always in the first position
 
    return list_tags

def splitline(line, verbose):
    word = []
    tags = []
    for w in line.split():
        if w.startswith('<') and w.endswith('>'):
            tags.append(w)
        else:
            word.append(w)
    if verbose: sys.stdout.write("word: {} tags: {}\n".format(' '.join(word), ' '.join(tags)))
    return word, tags

#####################################################################
### MAIN ############################################################
#####################################################################

if __name__ == '__main__':

    name = sys.argv.pop(0)
    usage = '''usage: {} -snoun INT -sverb INT -sadj INT -o FILE [-v] < file_with_tags_and_words
   -snoun INT : number of noun sets (default 0)
   -sverb INT : number of verb sets (default 0)
   -sadj  INT : number of adjective sets (default 0)
   -mood      : generate mood values (default False)
   -tense     : generate tense values (default False)
   -ndiff INT : number of generated lists of tags per sentence (default 0:all)
                if tags can be generated returns [INT] random sequences of tags
                a tag cannot be generated if its original form is 'x' or 'X'
   -originals : include the tags of the original sentence (default False)
   -o  FILE : output files will be FILE.desc and FILE.i
   -v       : verbose output (default False)
'''.format(name)
    
    snoun = 0
    sverb = 0
    sadj = 0
    mood = False
    tense = False
    ofile = None
    ndiff = 0
    originals = False
    verbose = False
    while len(sys.argv):
        tok = sys.argv.pop(0)
        if tok=="-h":
            sys.stderr.write("{}".format(usage))
            sys.exit()
        elif tok=="-snoun" and len(sys.argv):
            snoun = int(sys.argv.pop(0))
        elif tok=="-sverb" and len(sys.argv):
            sverb = int(sys.argv.pop(0))
        elif tok=="-sadj" and len(sys.argv):
            sadj = int(sys.argv.pop(0))
        elif tok=="-o" and len(sys.argv):
            ofile = sys.argv.pop(0)
        elif tok=="-ndiff" and len(sys.argv):
            ndiff = int(sys.argv.pop(0))
        elif tok=="-mood":
            mood = True
        elif tok=="-tense":
            tense = True
        elif tok=="-originals":
            originals = True
        elif tok=="-v":
            verbose = True
        else:
            sys.stderr.write('error: unparsed {} option\n'.format(tok))
            sys.stderr.write("{}".format(usage))
            sys.exit()

    if ofile == None:
        sys.stderr.write('error: -o option must be set\n')
        sys.stderr.write("{}".format(usage))
        sys.exit()    

    if snoun: ofile = ofile + ".snoun{}".format(snoun)
    if sverb: ofile = ofile + ".sverb{}".format(sverb)
    if sadj: ofile = ofile + ".sadj{}".format(sadj)
    if mood: ofile = ofile + ".mood"
    if tense: ofile = ofile + ".tense"
    if originals: ofile = ofile + ".originals"
    ofile = ofile + ".ndiff{}".format(ndiff)

    if os.path.exists(ofile):
        sys.stderr.write('error: file already exists: {}\n'.format(ofile))
        sys.exit()

    ff = open(ofile, "w")
    fi = open(ofile+".i", "w")
    N = defaultdict(int)
    for nline, strline in enumerate(sys.stdin):
        if (nline+1)%10000 == 0:
            if (nline+1)%100000 == 0:
                sys.stderr.write("{}".format(nline+1))
            else:
                sys.stderr.write(".")

        strline = strline.rstrip()
        words, tags = splitline(strline, verbose)
        n = 0
        list_tags = genTags(tags, snoun, sverb, sadj, mood, tense, ndiff, originals, verbose)
        for tags in list_tags:
            ff.write(tags+' '+' '.join(words)+"\n")
            fi.write(str(nline+1)+"\n")
            ff.flush()
            fi.flush()
            n += 1
        N[n] += 1
    ff.close()
    fi.close()

    sys.stderr.write("(read {} sentences)\n".format(nline+1))
    for n in sorted(N):
        sys.stderr.write("{}\t{}\n".format(n,N[n]))
