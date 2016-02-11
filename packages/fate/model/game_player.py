# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game_player',pkey='id',name_long='Game player',name_plural='Game players',caption_field='id')
        self.sysFields(tbl)
        tbl.column('game_id',name_long='game_id').relation('fate.game.id',relation_name='players', mode='foreignkey', onDelete='cascade',)
        tbl.column('player_id',name_long='player_id').relation('fate.player.id',relation_name='games', mode='foreignkey', onDelete='cascade')
        tbl.column('character_id',name_long='character_id').relation('fate.player_character.id',relation_name='player', mode='foreignkey', onDelete='setnull')
        
        tbl.formulaColumn('is_gm',"(@game_id.gm_id = #THIS.player_id)",dtype='B',name_long='Is GM')
        tbl.aliasColumn('username', relation_path='@player_id.username', name_long='Username')
        tbl.aliasColumn('nickname', relation_path='@player_id.nickname', name_long='Nickname')
        tbl.aliasColumn('fullname', relation_path='@player_id.fullname', name_long='Fullname')
    
