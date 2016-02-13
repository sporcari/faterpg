from gnr.core.gnrbag import Bag
import os
def color(color):
    for icn in os.listdir('icons'):
        if icn == '.DS_Store':
            continue
        print 'icn',icn,os.path.join('icons',icn)
        p = os.path.join(os.path.join('icons',icn))
        if os.path.isfile(p):
            b = Bag(p)
            print b
        #print b

if __name__ == '__main__':
    color('#FFFFFF')