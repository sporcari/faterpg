# encoding: utf-8

import sys
from gnr.app.gnrapp import GnrApp
db = GnrApp('faterpg').db

for tname,tblobj in db.packages['fate'].tables.items():
    print tname
    t = tblobj.dbtable
    for m in dir(t):
        if m.startswith('sysRecord_') and m!='sysRecord_':
            print tname,m[10:]
            t.sysRecord(m[10:])
db.commit()
print 'fatto'

