# -*- coding: utf-8 -*-

import sys

def getTags(T1, T2, do):
    T = []

    if do == 'intersection':
        for t in T1:
            if t in T2: T.append(t)

    if do == 'union':
        for t in T1:
            T.append(t)
        for t in T2:
            k = t.find(':')
            if k<1 or k>=len(t):
                sys.stderr.write('error: cannot recognize tag {}\n´'.format(t))
                sys.exit()
            name = t[1:k]
            val = t[k+1:k+2]
            T.append("<{}:{}>".format(name,val.lower()))

    return T


if __name__ == '__main__':

    name = sys.argv.pop(0)
    usage = '''{}  -do STRING < paste TAG1 TAG2
       -do STRING : 'intersection' use the intersection of both sets (TAG1 and TAG2)
                    'union' use the union of both sets (TAG1 and TAG2) lowercasing TAG2  values
'''.format(name)

    do = 'both'
    while len(sys.argv):
        tok = sys.argv.pop(0)
        if tok=="-do" and len(sys.argv): 
            do = sys.argv.pop(0)
        elif tok=="-h":
            sys.stderr.write("{}".format(usage))
            sys.exit()
        else:
            sys.stderr.write('error: unparsed {} option\n'.format(tok))
            sys.stderr.write("{}".format(usage))
            sys.exit()

    ############
    ### main ###
    ############

    for line in sys.stdin:
        line = line.rstrip()
        t1, t2 = line.split('\t')
        res = getTags(t1.split(' '), t2.split(' '), do)
        print(' '.join(res))

