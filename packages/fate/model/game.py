# encoding: utf-8

from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game',pkey='id',name_long='Game',name_plural='Games',caption_field='title', rowcaption='$title', lookup=False)
        self.sysFields(tbl,df=True, user_ins=True)
        tbl.column('title',name_long='Title',name_short='Title', unique=True,indexed=True, validate_notnull=True, validate_case='c')
        tbl.column('description', name_long='Description')
        tbl.column('code', size=':8', name_long='Code',name_short='Code',unique=True, indexed=True)
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='games', mode='foreignkey', onDelete='raise')
        tbl.column('gm_id',size='22',name_long='Game Master',name_short='GM').relation('fate.player.id',relation_name='gm_campaigns', mode='foreignkey', onDelete='setnull', one_name='Game Master', many_name='Gm for campaigns')
        tbl.column('weekday',size=':12',name_long='Preferred weekday',name_short='Weekday')
        tbl.column('setting_tags',name_long='Setting tags',name_short='Setting')

        tbl.column('banner_url',name_long='Banner URL',name_short='Banner URL')
        tbl.column('skill_sets',name_long='Skill Sets',name_short='Skill Sets')
        tbl.column('stunt_sets',name_long='Stunt Sets',name_short='Stunt Sets')
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
        tbl.column('status',size='2',values='CO:Configuration,CR:Creating,IP:In play,EN:Ended')

        tbl.formulaColumn('banner_img', "banner_url" ,dtype='P',name_long='!!Banner image',name_short='Banner', cell_format='auto:.5')
        tbl.formulaColumn('current_player_game', '(@players.player_id=:env_player_id)', dtype='B')
        tbl.formulaColumn('current_player_gm', '$gm_id=:env_player_id',  dtype='B')

        tbl.pyColumn('template_game',dtype='A',group='_',py_method='templateColumn', template_name='playcell')

    def defaultValues(self):
        return dict( consequences_slots='2,4,6',
                     refresh=3,
                     pc_phases=3,
                      pc_aspects=5,initial_stunts=3,
                     gm_id=self.db.currentEnv.get('player_id'),
                     stress_tracks=Bag(),
                     status='CO')

    def configDefault_CORE(self, record=None):
        stressbag = record['stress_tracks']
        stressbag['p'] = Bag(dict(track_name='Phisical',n_boxes=2))
        stressbag['m'] = Bag(dict(track_name='Mental',n_boxes=2))
        record.update(dict(pc_phases=3,
                     game_creation=True,
                     use_phases=True))
        if record['use_approaches']:
            record.update(dict( approach_set='STD'))
        else:
            record.update(dict(stunt_sets='STD',
                                skill_sets='STD',
                                 skill_cap=4))

    def configDefault_FAE(self, record=None):
        stressbag = record['stress_tracks']
        stressbag['s'] = Bag(dict(track_name='Stress',n_boxes=3))
        record.update(dict(use_approaches=True,
                             approach_set='STD',
                             game_creation=False,
                             use_phases=False))



    @public_method
    def createCharacterSheets(self, game_id):
        game_player_tbl = self.db.table('fate.game_player')
        game_record = self.record(game_id).output('bag')
        players = game_player_tbl.query(where='$game_id=:game_id AND $player_id!=:gm_id',
                                                          game_id=game_id, gm_id=game_record['gm_id']).fetch()
        for p in players:
            old_record = dict(p)
            p['character_id'] = self.db.table('fate.player_character').createEmptySheet(p['player_id'], game_record)
            game_player_tbl.update(p, old_record)
        self.db.commit()


    def trigger_onInserting(self,record=None):
        getattr(self,'configDefault_%(ruleset)s' %record)(record=record)

    def trigger_onUpdated(self,record=None,old_record=None):
        if old_record['status']=='CO' and record['status'] =='CR':
            self.db.table('fate.game_player').touchRecords(where='$game_id=:g_id AND $role=:r',g_id=record['id'],r='PL')

    def trigger_onInserted(self,record=None):
        self.db.table('fate.game_player').insert(dict(game_id=record['id'],player_id=self.db.currentEnv.get('player_id'),
                                                      role='GM'))









