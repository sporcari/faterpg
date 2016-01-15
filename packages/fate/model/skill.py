# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('skill',pkey='id',name_long='Skill',name_plural='Skills',caption_field='name')
        self.sysFields(tbl)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('special',name_long='Special rule',name_short='Special')
        tbl.column('skill_set',size='3',name_long='Skill set',name_short='Skill set').relation('fate.skill_set.code',relation_name='skills', mode='foreignkey', onDelete='cascade')
        tbl.column('game_id', size='22', name_long='Game id').relation('fate.game.id', relation_name='custom_skills', mode='foreignkey', onDelete='cascade')
        tbl.aliasColumn('actions', relation_path='@actions.action_type', name_long='Actions')
        tbl.aliasColumn('set', relation_path='@skill_set.code', name_long='Set')
        tbl.aliasColumn('game', relation_path='@game_id.code', name_long='Game')