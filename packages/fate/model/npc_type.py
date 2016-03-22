# encoding: utf-8
from gnr.core.gnrbag import Bag


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc_type',pkey='code', name_long='NPC Type',name_plural='NPC Types',caption_field='name')
        self.sysFields(tbl, id=None)
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='npc_types', mode='foreignkey', onDelete='raise')
        tbl.column('name', name_long='Name', name_short='Name',unique=True)
        tbl.column('code', size=':2', unique=True, long_name='Code')
        tbl.column('can_be_mob', dtype='B')
    
    def sysRecord_NL(self):
        return self.newrecord(ruleset='CORE',
                              name='Nameless',
                              can_be_mob=True,
                              code='NL')

    def sysRecord_SU(self):
        return self.newrecord(ruleset='CORE',
                              name='Supporting',
                              can_be_mob=False,
                              code='SU')

    def sysRecord_MA(self):
        return self.newrecord(ruleset='CORE',
                              name='Main',
                              can_be_mob=False,
                              code='MA')