# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game_player',pkey='id',name_long='Game player',name_plural='Game players',caption_field='id')
        self.sysFields(tbl)
        tbl.column('game_id',name_long='game_id').relation('fate.game.id',relation_name='players', mode='foreignkey', onDelete='setnull',)
        tbl.column('player_id',name_long='player_id').relation('fate.player.id',relation_name='games', mode='foreignkey', onDelete='setnull')
        tbl.column('character_id',name_long='character_id').relation('fate.player_character.id',relation_name='player', mode='foreignkey', onDelete='setnull')
