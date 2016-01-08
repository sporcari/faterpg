# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('aspect',pkey='id',name_long='Aspect',name_plural='Aspects',caption_field='phrase')
        self.sysFields(tbl)
        tbl.column('phrase',name_long='Phrase',name_short='Phrase',indexed=True)
        tbl.column('image',name_long='Image',name_short='Image')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',relation_name='aspects', mode='foreignkey')
        tbl.column('undiscovered',dtype='B',name_long='undiscovered',name_short='undiscovered')
        tbl.column('aspect_type_id',size='22',name_long='Aspect type',name_short='Aspect type').relation('fate.aspect_type',relation_name='aspects', mode='foreignkey', onDelete='raise')
        tbl.column('pc_id',size='22',name_long='PC',name_short='PC').relation('fate.player_character.id',relation_name='aspects', mode='foreignkey')
        tbl.column('npc_id',size='22',name_long='NPC',name_short='NPC').relation('fate.npc.id',relation_name='aspects', mode='foreignkey')
        tbl.column('scene_id',size='22',name_long='Scene',name_short='Scene')
        tbl.column('free_invocations',dtype='I',name_long='Free invocations',name_short='Free invocations')
        tbl.column('invoke_cnt',dtype='I',name_long='Invoke count',name_short='Invoke count')
        tbl.column('compel_cnt',dtype='I',name_long='Compel count',name_short='Compel count')
