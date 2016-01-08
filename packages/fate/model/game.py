# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game',pkey='id',name_long='Game',name_plural='Games',caption_field='id',lookup=False)
        self.sysFields(tbl,df=True)
        tbl.column('title',name_long='Title',name_short='Title',unique=True,indexed=True)
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='games', mode='foreignkey', onDelete='raise')
        tbl.column('gm_id',size='22',name_long='Game Master',name_short='GM').relation('fate.player.id',relation_name='gm_campaigns', mode='foreignkey', onDelete='setnull', one_name='Game Master', many_name='Gm for campaigns')
        tbl.column('weekday',size=':12',name_long='Preferred weekday',name_short='Weekday')
        tbl.column('image',name_long='Image',name_short='Image')
        tbl.column('skill_sets',name_long='Skill Sets',name_short='Skill Sets')
        tbl.column('approach_set',size=':3',name_long='Approach set',name_short='Approach set')
