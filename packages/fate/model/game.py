# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game',pkey='id',name_long='Game',name_plural='Games',caption_field='id',lookup=False)
        self.sysFields(tbl,df=True)
        tbl.column('title',name_long='Title',name_short='Title',unique=True,indexed=True)
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='games', mode='foreignkey', onDelete='raise')
        tbl.column('gm_id',size='22',name_long='Game Master',name_short='GM').relation('fate.player.id',relation_name='gm_campaigns', mode='foreignkey', onDelete='setnull', one_name='Game Master', many_name='Gm for campaigns')
        tbl.column('weekday',size=':12',name_long='Preferred weekday',name_short='Weekday')
        tbl.column('banner_url',name_long='Banner URL',name_short='Banner URL')
        tbl.column('skill_sets',name_long='Skill Sets',name_short='Skill Sets')
        tbl.column('approach_set',size=':3',name_long='Approach set',name_short='Approach set').relation('fate.approach_set.code',relation_name='games', mode='foreignkey')
        tbl.column('pc_aspects',dtype='I',name_long='PC aspects',name_short='PC aspects')
        tbl.column('pc_phases',dtype='I',name_long='PC phases',name_short='PC phases')
        tbl.column('skill_max_rate',dtype='I',name_long='Skill maximum rate',name_short='Skill max')
        tbl.column('refresh',dtype='I',name_long='Refresh',name_short='Refresh')
        tbl.column('initial_stunts',dtype='I',name_long='Initial stunts',name_short='N.Stunts')
        tbl.column('stress_tracks',name_long='Stress tracks',name_short='Stress tracks')
        tbl.column('dflt_stress_boxes',dtype='I',name_long='Default stress boxes',name_short='Stress boxes')
        tbl.column('consequences_slots',name_long='Consequences slots',name_short='Cons. slots')
        tbl.formulaColumn('banner_img', "banner_url" ,dtype='P',name_long='!!Banner image',name_short='Banner', cell_format='auto:.5')