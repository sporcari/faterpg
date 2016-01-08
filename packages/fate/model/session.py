# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('session',pkey='id',name_long='Session',name_plural='Sessions',caption_field='id')
        self.sysFields(tbl)
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',relation_name='sessions', mode='foreignkey')
        tbl.column('session_date',dtype='D',name_long='Date',name_short='Date')
        tbl.column('session_number',dtype='I',name_long='session_number')
        tbl.column('summary',name_long='Summary',name_short='Summary')
        tbl.column('gm_notes',name_long='GM Notes',name_short='GM Notes')
        tbl.column('game_creation',dtype='B',name_long='Game creation',name_short='Game creation')
