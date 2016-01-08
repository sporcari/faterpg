# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('scene',pkey='id',name_long='Scene',name_plural='Scenes',caption_field='id')
        self.sysFields(tbl,counter=True)
        tbl.column('game_id',size='22',name_long='Title',name_short='Title')
        tbl.column('where',name_long='Where',name_short='Where')
        tbl.column('abstract',name_long='Abstract',name_short='Abstract')
        tbl.column('image',name_long='Image',name_short='Image')
        tbl.column('session_id',size='22',name_long='Session',name_short='Session')
        tbl.column('scenario_id',size='22',name_long='Scenario',name_short='Scenario')
