# encoding: utf-8

from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game',pkey='id',name_long='Game',name_plural='Games',caption_field='id',lookup=False)
        self.sysFields(tbl,df=True, user_ins=True)
        tbl.column('title',name_long='Title',name_short='Title',unique=True,indexed=True, validate_notnull=True, validate_case='l')
        tbl.column('description', name_long='Description')
        tbl.column('code', size=':8', name_long='code',name_short='code',unique=True, indexed=True)
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='games', mode='foreignkey', onDelete='raise')
        tbl.column('gm_id',size='22',name_long='Game Master',name_short='GM').relation('fate.player.id',relation_name='gm_campaigns', mode='foreignkey', onDelete='setnull', one_name='Game Master', many_name='Gm for campaigns')
        tbl.column('weekday',size=':12',name_long='Preferred weekday',name_short='Weekday')
        tbl.column('setting_tags',name_long='Setting tags',name_short='Setting')

        tbl.column('banner_url',name_long='Banner URL',name_short='Banner URL')
        tbl.column('skill_sets',name_long='Skill Sets',name_short='Skill Sets')
        tbl.column('approach_set',size=':3',name_long='Approach set',name_short='Approach set').relation('fate.approach_set.code',relation_name='games', mode='foreignkey')
        tbl.column('pc_aspects',dtype='I',name_long='PC aspects',name_short='PC aspects')
        tbl.column('use_phases', dtype='B', name_long='Use phases')
        tbl.column('use_approaches', dtype='B', name_long='Use approaches')
        tbl.column('game_creation', dtype='B', name_long='Game creation')
        tbl.column('pc_phases',dtype='I',name_long='PC phases',name_short='PC phases')
        tbl.column('skill_cap',dtype='I',name_long='Skill cap',name_short='Skill cap')
        tbl.column('refresh',dtype='I',name_long='Refresh',name_short='Refresh')
        tbl.column('initial_stunts',dtype='I',name_long='Initial stunts',name_short='N.Stunts')
        tbl.column('stress_tracks', dtype='X', name_long='Stress tracks',name_short='Stress tracks')
        tbl.column('consequences_slots',name_long='Consequences slots',name_short='Cons. slots')
        tbl.formulaColumn('banner_img', "banner_url" ,dtype='P',name_long='!!Banner image',name_short='Banner', cell_format='auto:.5')
        tbl.formulaColumn('current_player_game', '(@players.player_id=:env_player_id)', dtype='B')
        tbl.formulaColumn('current_player_gm', '$gm_id=:env_player_id',  dtype='B')

    def defaultValues(self):
        stressbag = Bag()
        stressbag.setItem('p.track_name', 'Phisical')
        stressbag.setItem('p.n_boxes', 2)
        stressbag.setItem('m.track_name', 'Mental')
        stressbag.setItem('m.n_boxes', 2)

        return dict(ruleset='CORE',
                     stress_tracks = stressbag,
                     use_approaches=False,
                     skill_sets='STD',
                     approach_set='STD',
                     consequences_slots='2,4,6',
                     refresh=3,
                     skill_cap=4,
                     pc_phases=3,
                     game_creation=True,
                     use_phases=True,
                     pc_aspects=5,initial_stunts=3,
                     gm_id=self.db.currentEnv.get('player_id'))
