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

def genTags(word, tags, do, ndiff, verbose):
    lines = [[]]
    for tag in tags:
        if verbose: sys.stdout.write('curr tag is {}\n'.format(tag))

        if tag.startswith('<det:'):
            if verbose: sys.stdout.write('adding det\n')
            t = []
            t.append(tag)
            if "det" in do:
                t.append('<det:A>')
                t.append('<det:D>')
                t.append('<det:I>')
                t.append('<det:P>')
                #t.append('<det:E>')
                #t.append('<det:T>')
            lines = addTags(lines, t)

        if tag.startswith('<fadj:'):
            if verbose: sys.stdout.write('adding fadj\n')
            t = []
            t.append(tag)
            if "fadj" in do:
                t.append('<fadj:A>')
                t.append('<fadj:B>')
                t.append('<fadj:C>')
            lines = addTags(lines, t)

        if tag.startswith('<fnoun:'):
            if verbose: sys.stdout.write('adding fnoun\n')
            t = []
            t.append(tag)
            if "fnoun" in do:
                t.append('<fnoun:A>')
                t.append('<fnoun:B>')
                t.append('<fnoun:C>')
            lines = addTags(lines, t)

        if tag.startswith('<fverb:'):
            if verbose: sys.stdout.write('adding fverb\n')
            t = []
            t.append(tag)
            if "fverb" in do:
                t.append('<fverb:A>')
                t.append('<fverb:B>')
                t.append('<fverb:C>')
            lines = addTags(lines, t)

        if tag.startswith('<ladj:'):
            if verbose: sys.stdout.write('adding ladj\n')
            t = []
            t.append(tag)
            if "ladj" in do:
                t.append('<ladj:A>')
                t.append('<ladj:B>')
                t.append('<ladj:C>')
            lines = addTags(lines, t)

        if tag.startswith('<lnoun:'):
            if verbose: sys.stdout.write('adding lnoun\n')
            t = []
            t.append(tag)
            if "lnoun" in do:
                t.append('<lnoun:A>')
                t.append('<lnoun:B>')
                t.append('<lnoun:C>')
            lines = addTags(lines, t)

        if tag.startswith('<lverb:'):
            if verbose: sys.stdout.write('adding lverb\n')
            t = []
            t.append(tag)
            if "lverb" in do:
                t.append('<lverb:A>')
                t.append('<lverb:B>')
                t.append('<lverb:C>')
            lines = addTags(lines, t)

        if tag.startswith('<radj:'):
            if verbose: sys.stdout.write('adding radj\n')
            t = []
            t.append(tag)
            if "radj" in do:
                t.append('<radj:A>')
                t.append('<radj:B>')
                t.append('<radj:C>')
            lines = addTags(lines, t)

        if tag.startswith('<rnoun:'):
            if verbose: sys.stdout.write('adding rnoun\n')
            t = []
            t.append(tag)
            if "rnoun" in do:
                t.append('<rnoun:A>')
                t.append('<rnoun:B>')
                t.append('<rnoun:C>')
            lines = addTags(lines, t)

        if tag.startswith('<rverb:'):
            if verbose: sys.stdout.write('adding rverb\n')
            t = []
            t.append(tag)
            if "rverb" in do:
                t.append('<rverb:A>')
                t.append('<rverb:B>')
                t.append('<rverb:C>')
            lines = addTags(lines, t)

        if tag.startswith('<length:'):
            if verbose: sys.stdout.write('adding length\n')
            t = []
            t.append(tag)
            if "length" in do:
                t.append('<length:XL>')
                t.append('<length:L>')
                t.append('<length:M>')
                t.append('<length:S>')
                t.append('<length:XS>')
            lines = addTags(lines, t)

        if tag.startswith('<vmood:'):
            if verbose: sys.stdout.write('adding vmood\n')
            t = []
            t.append(tag)
            if "vmood" in do:
                t.append('<vmood:I>') #indicative
                t.append('<vmood:S>') #subjunctive
                t.append('<vmood:M>') #imperative
                #t.append('<vmood:P>') #participle
                #t.append('<vmood:G>') #gerund
                #t.append('<vmood:N>') #infinitive
            lines = addTags(lines, t)

        if tag.startswith('<vnumber:'):
            if verbose: sys.stdout.write('adding vnumber\n')
            t = []
            t.append(tag)
            if "vnumber" in do:
                t.append('<vnumber:S>')
                t.append('<vnumber:P>')
            lines = addTags(lines, t)

        if tag.startswith('<vperson:'):
            if verbose: sys.stdout.write('adding vperson\n')
            t = []
            t.append(tag)
            if "vperson" in do:
                t.append('<vperson:1>')
                t.append('<vperson:2>')
                t.append('<vperson:3>')
            lines = addTags(lines, t)

        if tag.startswith('<vtense:'):
            if verbose: sys.stdout.write('adding vtense\n')
            t = []
            t.append(tag)
            if "vtense" in do:
                t.append('<vtense:F>') #future
                t.append('<vtense:P>') #present
                t.append('<vtense:S>') #past
                #t.append('<vtense:C>') #conditional
                #t.append('<vtense:I>') #imperfect
            lines = addTags(lines, t)

    ### add sentence after tags
    t = []
    t.append(' '.join(word))
    lines = addTags(lines,t)
    if len(lines) == 1:
        return lines, True

    initial = lines.pop(0)
    random.shuffle(lines) ### shuffles lines
    if ndiff>0:
        lines = lines[:ndiff]

    return lines, False

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
    usage = '''usage: {} -do LIST -o FILE -n INT [-rep] [-v] < file_with_tags_and_words
   -do LIST : comma-separated list of features (Ex: det,fadj,fnoun,fverb,ladj,lnoun,lverb,radj,rnoun,rverb,length,vmood,vnumber,vperson,vtense)
   -o  FILE : output files will be FILE and FILE.i
   -n   INT : consider INT tag sets for each sentence (default 0:all)
   -rep     : allow repeated sentences (default False)
   -v       : verbose output (default False)
'''.format(name)
    
    rep = False
    do = []
    ofile = None
    verbose = False
    ndiff = 0
    while len(sys.argv):
        tok = sys.argv.pop(0)
        if tok=="-h":
            sys.stderr.write("{}".format(usage))
            sys.exit()
        elif tok=="-do" and len(sys.argv):
            do = sys.argv.pop(0).split(",")
        elif tok=="-o" and len(sys.argv):
            ofile = sys.argv.pop(0)
        elif tok=="-n" and len(sys.argv):
            ndiff = int(sys.argv.pop(0))
        elif tok=="-rep":
            rep = True
        elif tok=="-v":
            verbose = True
        else:
            sys.stderr.write('error: unparsed {} option\n'.format(tok))
            sys.stderr.write("{}".format(usage))
            sys.exit()

    if len(do) == 0:
        sys.stderr.write('error: -do option must be set\n')
        sys.stderr.write("{}".format(usage))
        sys.exit()

    if ofile == None:
        sys.stderr.write('error: -do option must be set\n')
        sys.stderr.write("{}".format(usage))
        sys.exit()

    if os.path.exists(ofile):
        sys.stderr.write('error: file already exist: {}\n'.format(ofile))
        sys.stderr.write("{}".format(usage))
        sys.exit()
    

    ff = open(ofile, "w")
    fi = open(ofile+".i", "w")
    N = defaultdict(int)
#    olines = defaultdict(int)
#    nrep = 0
    n_original = 0
    for nline, strline in enumerate(sys.stdin):
        if (nline+1)%10000 == 0:
            if (nline+1)%100000 == 0:
                sys.stderr.write("{}".format(nline+1))
            else:
                sys.stderr.write(".")

        strline = strline.rstrip()
        word, tags = splitline(strline, verbose)
        n = 0
        lines, is_original = genTags(word, tags, do, ndiff, verbose)
        if is_original: n_original += 1
        for line in lines:
            strline = ' '.join(line)
#            if not rep and strline in olines: 
#                nrep += 1
#                continue
#            olines[strline] += 1
            ff.write(strline+"\n")
            fi.write(str(nline+1)+"\n")
            ff.flush()
            fi.flush()
            n += 1
        N[n] += 1
    ff.close()
    fi.close()

    sys.stderr.write("({} sentences {} original)\n".format(nline+1, n_original))
    for n in sorted(N):
        sys.stderr.write("{}\t{}\n".format(n,N[n]))
