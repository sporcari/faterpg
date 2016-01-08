# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('scenario',pkey='id',name_long='Scenario',name_plural='Scenario',caption_field='title')
        self.sysFields(tbl)
        tbl.column('title',size=':50',name_long='Title',name_short='Title')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',relation_name='scenarios', mode='foreignkey')
        tbl.column('summary',name_long='Summary',name_short='Summary')
