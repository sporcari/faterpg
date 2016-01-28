# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game_player',pkey='id',name_long='Game player',name_plural='Game players',caption_field='id')
        self.sysFields(tbl)
        tbl.column('game_id',name_long='game_id').relation('fate.game.id',relation_name='players', mode='foreignkey', onDelete='cascade',)
        tbl.column('player_id',name_long='player_id').relation('fate.player.id',relation_name='games', mode='foreignkey', onDelete='cascade')
        tbl.column('character_id',name_long='character_id').relation('fate.player_character.id',relation_name='player', mode='foreignkey', onDelete='setnull')
        tbl.column('role' ,size='2',name_long='!!Role',values='GM:Game Master,PL:Player,VO:View Only')
        tbl.formulaColumn('role_desc',"""(CASE WHEN $role='VO' THEN 'VO'
                                         ELSE '' END)
                                        """)
        tbl.pyColumn('page_id')

    def pyColumn_page_id(self,record=None,field=None):
        return 'pippo'

   #def trigger_onUpdated(self,record=None,old_record=None):
   #    self.checkCharacter(record,old_record=old_record)

   #def trigger_onInserted(self,record=None):
   #    self.checkCharacter(record)

    def defaultValues(self):
        return dict(role='PL')

    #def checkCharacter(self,record=None,old_record=None):
    #    if record['role'] == 'PL' and not record['character_id']:
    #        game_record = self.db.table('fate.game').record(record['id']).output('dict')
    #        if game_record['status'] != 'CO':
    #            record['character_id'] = self.db.table('fate.player_character').createEmptySheet(record['player_id'], game_record)

