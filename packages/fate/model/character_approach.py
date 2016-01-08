# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('character_approach',pkey='id',name_long='Character Approach',name_plural='Character Approaches',caption_field='id')
        self.sysFields(tbl)
        tbl.column('approach_id',size='22',name_long='Approach',name_short='Approach')
        tbl.column('pc_id',size='22',name_long='Player character',name_short='PC')
        tbl.column('npc_id',size='22',name_long='NPC',name_short='NPC')
        tbl.column('rate',dtype='I',name_long='Rate',name_short='Rate')
