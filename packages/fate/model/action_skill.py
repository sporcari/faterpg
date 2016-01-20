# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('action_skill',pkey='id',name_long='Action for skill',name_plural='Actions for skill',caption_field='id',lookup=False)
        self.sysFields(tbl)
        tbl.column('action_type',size='2',name_long='Action Type',name_short='Action').relation('fate.action_type.code',relation_name='skills', mode='foreignkey')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='actions', mode='foreignkey', onDelete='cascade')
        tbl.column('description',name_long='Description',name_short='Description')
