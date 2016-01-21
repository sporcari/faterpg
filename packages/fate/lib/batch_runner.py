# encoding: utf-8

from gnr.app.gnrapp import GnrApp
db = GnrApp('faterpg').db

stunt_tbl = db.table('fate.stunt').setStandardSet()
db.commit()
print 'fatto'

