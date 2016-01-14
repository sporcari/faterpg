# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt',pkey='id',name_long='Stunt',name_plural='Stunt',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',size=':30',name_long='Name',name_short='Name',unique=True,indexed=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('approach_id',size='22',name_long='Approach',name_short='Approach').relation('fate.approach.name',relation_name='stunts', mode='foreignkey')
        #tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='stunts', mode='foreignkey')
        tbl.column('action_type',size='2',name_long='Action Type',name_short='Action Type').relation('fate.action_type.code',relation_name='stunts', mode='foreignkey')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='stunts', mode='foreignkey')
        tbl.column('custom',dtype='B',name_long='Custom',name_short='Custom')
        tbl.column('once_per_scene',dtype='B',name_long='Once per scene',name_short='OP Scene')
        tbl.column('n_per_session',dtype='I',name_long='N per session',name_short='NP Session')
        tbl.column('in_conflict',dtype='B',name_long='In conflict',name_short='In conflict')
        tbl.column('spend_fp',dtype='B',name_long='Spend fate point',name_short='Spend FP')



