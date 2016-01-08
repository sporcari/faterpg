# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt',pkey='id',name_long='Stunt',name_plural='Stunt',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',size=':30',name_long='Name',name_short='Name',unique=True,indexed=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('approach_id',size='22',name_long='Approach',name_short='Approach').relation('fate.approach.id',relation_name='stunts', mode='foreignkey')
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='stunts', mode='foreignkey')
        tbl.column('action_type_id',size='22',name_long='Action Type',name_short='Action Type').relation('fate.action_type.id',relation_name='stunts', mode='foreignkey')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='stunts', mode='foreignkey')
        tbl.column('custom',dtype='B',name_long='Custom',name_short='Custom')
