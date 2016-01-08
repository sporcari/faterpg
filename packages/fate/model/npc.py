# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc',pkey='id',name_long='Non-player character',name_plural='NPCS',caption_field='name')
        self.sysFields(tbl,df=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Name')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game')
        tbl.column('image',name_long='Image',name_short='Image')
        tbl.column('npc_type_id',size='22',name_long='NPC Type',name_short='Type')
