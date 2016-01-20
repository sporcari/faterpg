# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('character_skill',pkey='id',name_long='Character skill',name_plural='Character skills',caption_field='id',lookup=False)
        self.sysFields(tbl)
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='characters', mode='foreignkey')
        tbl.column('pc_id',size='22',name_long='Player character',name_short='PC').relation('fate.player_character.id',relation_name='skills', mode='foreignkey', onDelete='cascade')
        tbl.column('npc_id',size='22',name_long='NPC',name_short='NPC').relation('fate.npc.id',relation_name='skills',  onDelete='cascade')
        tbl.column('rate',dtype='I',name_long='Rate',name_short='Rate')
