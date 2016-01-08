# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc_type',pkey='id',name_long='NPC Type',name_plural='NPC Types',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
