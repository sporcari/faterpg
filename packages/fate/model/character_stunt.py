# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('character_stunt',pkey='id',name_long='Character stunt',name_plural='Character stunts',caption_field='id')
        self.sysFields(tbl)
        tbl.column('stunt_id',size='22',name_long='Stunt',name_short='Stunt')
        tbl.column('pc_id',size='22',name_long='PC',name_short='PC')
        tbl.column('npc_id',size='22',name_long='NPC',name_short='NPC')
