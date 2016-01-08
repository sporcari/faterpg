#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='fate package',sqlschema='fate',sqlprefix=True,
                    name_short='Fate', name_long='Fate', name_full='Fate')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
