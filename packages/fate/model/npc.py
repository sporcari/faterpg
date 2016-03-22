# encoding: utf-8

from gnr.core.gnrbag import Bag


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc',pkey='id',name_long='Non-player character',name_plural='NPCS',caption_field='name')
        self.sysFields(tbl,df=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('high_concept',name_long='High Concept',name_short='HC')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game')
        tbl.column('image_url',name_long='Image',name_short='Image')
        tbl.column('npc_type',size='3',name_long='NPC Type',name_short='Type').relation('fate.npc_type.code', mode='foreignkey',onDelete='raise')
        tbl.column('mob', dtype='B', name_long='Mob')
        tbl.column('dead', dtype='B', name_long='Dead')
        tbl.column('stress_tracks', dtype='X')
        tbl.column('consequences_slots', dtype='X')
        tbl.column('data', dtype='X', _sendback=True)
        tbl.formulaColumn('image_img', "image_url" ,dtype='P',name_long='!!Portrait',name_short='Portrait', cell_format='auto:.5')


