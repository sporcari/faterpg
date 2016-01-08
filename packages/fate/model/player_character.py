# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('player_character',pkey='id',name_long='Player Character',name_plural='Characters',caption_field='name')
        self.sysFields(tbl)
        tbl.column('player_id',size='22',name_long='Player',name_short='Player').relation('fate.player.id',relation_name='characters', mode='foreignkey', onDelete='setnull')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',relation_name='player_characters', mode='foreignkey')
        tbl.column('name',size=':40',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('refresh',dtype='I',name_long='Refresh',name_short='Refresh')
        tbl.column('high_concept_id',size='22',name_long='High concept',name_short='High concept').relation('fate.aspect.id',relation_name='defined_pc', mode='foreignkey', one_one=True)
        tbl.column('trouble_id',size='22',name_long='Trouble',name_short='Trouble').relation('fate.aspect.id',relation_name='troubled_pc', mode='foreignkey', one_one=True)
        tbl.column('fate_points',dtype='I',name_long='Fate Points',name_short='Fate Points')
        tbl.column('image',name_long='Image',name_short='Image')
