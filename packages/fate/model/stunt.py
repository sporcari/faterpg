# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt',pkey='id',name_long='Stunt',name_plural='Stunt',caption_field='name',rowcaption='$name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',size=':30',name_long='Name',name_short='Name',unique=True,indexed=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('approach_id',size='22',name_long='Approach',name_short='Approach').relation('fate.approach.name',relation_name='stunts', mode='foreignkey')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='stunts', mode='foreignkey')
        tbl.column('stunt_type', size='4', name_long='Stunt Type').relation('fate.stunt_type.code', relation_name='stunts', mode='foreignkey', onDelete='raise')

        tbl.column('action_type',size='2',name_long='Action Type',name_short='Action Type').relation('fate.action_type.code',relation_name='stunts', mode='foreignkey')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill').relation('fate.skill.id',relation_name='stunts', mode='foreignkey')
        tbl.column('bonus',name_long='Bonus',name_short='Bonus').relation('fate.stunt_bonus.code')
        tbl.column('n_per_scene',dtype='I',name_long='Times per scene',name_short='T.Scene')
        tbl.column('n_per_session',dtype='I',name_long='Times per session',name_short='T.Session')
        tbl.column('scene_type',name_long='Scene type restriction',name_short='Only for').relation('fate.scene_type.code', relation_name='stunts',mode='foreignkey')
        tbl.column('spend_fp',dtype='B',name_long='Spend fate point',name_short='Spend FP')
