# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc_type',pkey='id',name_long='NPC Type',name_plural='NPC Types',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')

    def sysRecord_NL(self):
        return self.newrecord(name='Nameless',
                              description='Nameless NPC')

    def sysRecord_SU(self):
        return self.newrecord(name='Supporting NPC',
                              description='Supporting NPC')

    def sysRecord_MA(self):
        return self.newrecord(name='Main NPC',
                              description='Main NPC')
