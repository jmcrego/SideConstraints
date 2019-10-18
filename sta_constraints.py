# -*- coding: utf-8 -*-

from collections import defaultdict
import random
import sys
import json

def progress(n):
    if n%10000 == 0:
        if n%100000 == 0:
            sys.stderr.write("{}".format(n))
        else:
            sys.stderr.write(".")    

class sta():
    def __init__(self, opts, verbose):
        self.verbose = verbose
        self.opts = opts
        if not 'mode' in self.opts:
            sys.stderr.write('error: missing \'mode\' option!\n')
            sys.exit()
        self.sep = '￨'
        self.N = defaultdict(int)

    def triplet(self, src, tgt, ali, nline):
        self.ok = True
        self.vs = src.split()
        self.vt = tgt.split()
        self.s2t = [set() for i in range(len(self.vs))]
        self.t2s = [set() for i in range(len(self.vt))]
        for a in ali.split(' '):
            if "-" not in a: 
                sys.stderr.write('warning: bad format alignment [{}] in line {}!\n'.format(a,nline))
                self.ok = False
                return
            (s,t) = map(int, a.split('-'))
            if s<0 or s>=len(self.vs) or t<0 or t>=len(self.vt):
                sys.stderr.write('warning: alignment [{},{}] out of bounds in line {}!\n'.format(s,t,nline))
                self.ok = False
                return
            self.s2t[s].add(t)
            self.t2s[t].add(s)
        return

    def valid_alignment(self, s):
        if s >= len(self.s2t):
            return -1
        if len(self.s2t[s]) != 1: ### a single link pointing to t
            return -1
        t = list(self.s2t[s])[0]
        if self.opts['many_to_one']:
            return t
        if len(self.t2s[t]) != 1: ### a single link pointing to s
            return -1
        return t

    def valid_pos(self, spos, tpos):
        if len(self.opts['tags'])==0: ### do not filter
            return True
        for p in self.opts['tags']:                
            if len(p)==2: ### check both src/tgt pos-tags
                if spos.startswith(p[0]) and tpos.startswith(p[1]):
                    return True
            elif len(p)==1: ### check src pos-tag
                if spos.startswith(p[0]):
                    return True
        return False

    def token_features(self, tok):
        features = tok.split(self.sep)
        wrd = features[0]
        pos = features[1]
        lem = features[2]
        return wrd, pos, lem

    def stats(self):
        total = 0
        for k, v in self.N.iteritems():
            total += v
        return json.dumps(self.N, indent=4)
        
    def run(self, nline):
        if self.opts['mode'] == 'append':
            return self.append(nline)
        elif self.opts['mode'] == 'person' or self.opts['mode'] == 'tense' or self.opts['mode'] == 'mood':
            return self.person_tense_mood(nline)

    ###############################################################################################
    ### append ####################################################################################
    ###############################################################################################
    def append(self, nline):
        vsrc = []

        if not self.ok:
            return vsrc

        if self.verbose:
            print("===== SRC: {}\n===== TGT: {}".format(' '.join(self.vs), ' '.join(self.vt)))

        for s in range(len(self.vs)):
            swrd, spos, slem = self.token_features(self.vs[s])
            t = self.valid_alignment(s)

            if t<0:
                vsrc.append(swrd + self.sep + 'S')
                self.N['S'] += 1
                continue

            twrd, tpos, tlem = self.token_features(self.vt[t])
            if not self.valid_pos(spos,tpos):
                vsrc.append(swrd + self.sep + 'S')
                self.N['S'] += 1
                continue

            vsrc.append(swrd + self.sep + 'R')
            self.N['R'] += 1

            if random.random() < self.opts['pLem']: ### generates random float [0.0, 1.0)
                vsrc.append(tlem + self.sep + 'L') ### tlem may be lexically equal to twrd
                self.N['L'] += 1
            else:
                vsrc.append(twrd + self.sep + 'W')
                self.N['W'] += 1

            if self.verbose:
                print("========== {}:{}\t{}:{}\t{}".format(s,self.vs[s],t,self.vt[t],vsrc[-1]))

        return vsrc

    ###############################################################################################
    ### person_tense_mood #########################################################################
    ###############################################################################################
    def person_tense_mood(self, nline):
        vsrc = []

        if not self.ok:
            return vsrc

        if self.verbose:
            print("===== SRC: {}\n===== TGT: {}".format(' '.join(self.vs), ' '.join(self.vt)))

        for s in range(len(self.vs)):
            swrd, spos, slem = self.token_features(self.vs[s])
            t = self.valid_alignment(s)

            if t<0:
                vsrc.append(swrd + self.sep + 'S')
                self.N['S'] += 1
                continue

            twrd, tpos, tlem = self.token_features(self.vt[t])
            if not self.valid_pos(spos,tpos):
                vsrc.append(swrd + self.sep + 'S')
                self.N['S'] += 1
                continue

            if not tpos.startswith('VM'):
                vsrc.append(swrd + self.sep + 'S')
                self.N['S'] += 1
                continue

            if self.opts['mode'] == 'person':
                if (tpos[4] == '1' or tpos[4] == '2' or tpos[4] == '3') and (tpos[5] == 'S' or tpos[5] == 'P'):
                    vsrc.append(swrd + self.sep + 'person:'+tpos[4:6])
                    self.N['person:'+tpos[4:6]] += 1
                else:
                    vsrc.append(swrd + self.sep + 'S')
                    self.N['S'] += 1
                    continue

            elif self.opts['mode'] == 'tense': #P:present; I:imperfect; F:future; S:past; C:conditional
                if tpos[3] == 'P':
                    vsrc.append(swrd + self.sep + 'tense:Pres')
                    self.N['tense:Pres'] += 1
                elif tpos[3] == 'I' or tpos[3] == 'S':
                    vsrc.append(swrd + self.sep + 'tense:Past')
                    self.N['tense:Past'] += 1
                elif tpos[3] == 'F':
                    vsrc.append(swrd + self.sep + 'tense:Future')
                    self.N['tense:Future'] += 1
                elif tpos[3] == 'C':
                    vsrc.append(swrd + self.sep + 'tense:Cond')
                    self.N['tense:Cond'] += 1
                else:
                    vsrc.append(swrd + self.sep + 'S')
                    self.N['S'] += 1
                    continue

            elif self.opts['mode'] == 'mood': #I:indicative; S:subjunctive; M:imperative; P:participle; G:gerund; N:infinitive
                if tpos[2] == 'I':
                    vsrc.append(swrd + self.sep + 'mood:Indic')
                    self.N['mood:Indic'] += 1
                elif tpos[2] == 'S':
                    vsrc.append(swrd + self.sep + 'mood:Subj')
                    self.N['mood:Subj'] += 1
                elif tpos[2] == 'M':
                    vsrc.append(swrd + self.sep + 'mood:Imper')
                    self.N['mood:Imper'] += 1
                elif tpos[2] == 'P':
                    vsrc.append(swrd + self.sep + 'mood:Participle')
                    self.N['mood:Participle'] += 1
                elif tpos[2] == 'G':
                    vsrc.append(swrd + self.sep + 'mood:Gerund')
                    self.N['mood:Gerund'] += 1
                elif tpos[2] == 'N':
                    vsrc.append(swrd + self.sep + 'mood:Infinitive')
                    self.N['mood:Infinitive'] += 1
                else:
                    vsrc.append(swrd + self.sep + 'S')
                    self.N['S'] += 1
                    continue

            if self.verbose:
                print("========== {}:{}\t{}:{}\t{}".format(s,self.vs[s],t,self.vt[t],vsrc[-1]))

        return vsrc

#####################################################################
### MAIN ############################################################
#####################################################################

if __name__ == '__main__':

    name = sys.argv.pop(0)
    usage = '''usage: {} -s FILE -t FILE -a FILE [-mode STRING] [-tags STRING] [-many-to-one] [-pLem FLOAT] [-maxl INT] [-v]
Mandatory:
   -s      FILE : source file
   -t      FILE : target file
   -a      FILE : src2tgt alignment file
Optional:
   -mode STRING : available modes are: append, person, tense, mood, rnd, frq (default append)
   -tags STRING : pairs of src/tgt valid tags (default: \'V-VM N-NC J-AQ\')
   -many-to-one : consider many-to-one alignments rather than one-to-one (default not used)
   -pLem  FLOAT : probability to use lemma rather than word form in append mode (default 0.5)
Other:
   -maxl    INT : consider the first INT lines (default 0: all)
   -v           : verbose output (default False)
   -h           : this help
'''.format(name)

    fsrc = None
    ftgt = None
    fali = None
    maxl = 0
    verbose = False

    opts = {}
    opts['mode'] = 'append'
    opts['tags'] = [['V','VM'], ['N','NC'], ['J','AQ']]
    opts['many_to_one'] = False
    opts['pLem'] = 0.5

    while len(sys.argv):
        tok = sys.argv.pop(0)
        if tok=="-h":
            sys.stderr.write("{}".format(usage))
            sys.exit()
        elif tok=="-v":
            verbose = True
        elif tok=="-s" and len(sys.argv):
            fsrc = sys.argv.pop(0)
        elif tok=="-t" and len(sys.argv):
            ftgt = sys.argv.pop(0)
        elif tok=="-a" and len(sys.argv):
            fali = sys.argv.pop(0)
        elif tok=="-maxl" and len(sys.argv):
            maxl = int(sys.argv.pop(0))
        elif tok=="-mode" and len(sys.argv):
            opts['mode'] = sys.argv.pop(0)
        elif tok=="-tags" and len(sys.argv):
            stags = sys.argv.pop(0)
            opts['tags'] = [tag.split('-') for tag in stags.split()]                
        elif tok=="-many-to-one":
            opts['many_to_one'] = True
        elif tok=="-pLem" and len(sys.argv):
            opts['pLem'] = float(sys.argv.pop(0))
        else:
            sys.stderr.write('error: unparsed {} option\n'.format(tok))
            sys.stderr.write("{}".format(usage))
            sys.exit()

    if fsrc is None:
        sys.stderr.write('error: missing -s option\n{}'.format(usage))
        sys.exit()

    if ftgt is None:
        sys.stderr.write('error: missing -t option\n{}'.format(usage))
        sys.exit()

    if fali is None:
        sys.stderr.write('error: missing -a option\n{}'.format(usage))
        sys.exit()

    fh_src = open (fsrc, "r")
    fh_tgt = open (ftgt, "r")
    fh_ali = open (fali, "r")

    nline = 0
    l = sta(opts,verbose)
    while True:
        nline += 1
        if maxl > 0 and nline > maxl:
            break
        progress(nline)
        lsrc = fh_src.readline()
        ltgt = fh_tgt.readline()
        lali = fh_ali.readline()
        if not lsrc or not ltgt or not lali: 
            break
        l.triplet(lsrc, ltgt, lali, nline)
        print(' '.join(l.run(nline)))

    fh_src.close()   
    fh_tgt.close()   
    fh_ali.close()   

    sys.stderr.write('Done {}\n'.format(l.stats()))



