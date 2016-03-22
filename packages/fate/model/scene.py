# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('scene',pkey='id',name_long='Scene',name_plural='Scenes',caption_field='id')
        self.sysFields(tbl,counter='game_id')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',
                                                                mode='foreignkey',
                                                                relation_name='scenes',onDelete='cascade')
        tbl.column('title', name_long='Title')
        tbl.column('description', name_long='Description')
        tbl.column('scene_type').relation('fate.scene_type.code', mode='foreignkey',onDelete='raise')
        tbl.column('data', dtype='X', _sendback=True)
        tbl.column('npc_pkeys', name_long='Npc Pkeys')
        tbl.pyColumn('template_scene',dtype='A',group='_',py_method='templateColumn', template_name='scenecell')
