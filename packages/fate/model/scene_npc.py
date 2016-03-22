# encoding: utf-8


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('scene_npc',pkey='id',name_long='Scene Npc',name_plural='Scene Npcs',caption_field='id')
        self.sysFields(tbl)
        tbl.column('scene_id',name_long='scene_id').relation('fate.scene.id',relation_name='npcs', mode='foreignkey', onDelete='cascade')
        tbl.column('npc_id',name_long='npc_id').relation('fate.npc.id',relation_name='scenes', mode='foreignkey', onDelete='setnull')