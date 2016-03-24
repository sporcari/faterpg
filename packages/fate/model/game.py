# encoding: utf-8

from gnr.core.gnrbag import Bag
from gnr.core.gnrstring import slugify
from gnr.core.gnrdecorator import public_method


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('game',pkey='id',name_long='Game',name_plural='Games',caption_field='title', rowcaption='$title', lookup=False)
        self.sysFields(tbl,df=True, user_ins=True)
        tbl.column('title',name_long='Title',name_short='Title', indexed=True, validate_notnull=True, validate_case='c')
        tbl.column('description', name_long='Description')
        tbl.column('code', size=':20', name_long='Code',name_short='Code', indexed=True)
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
        tbl.column('consequences_slots', dtype='X', name_long='Consequences slots',name_short='Cons. slots')

        #tbl.column('status',size='2',values='CO:Configuration,CR:Creating,IP:In play,EN:Ended')
        #tbl.column('play_data_id', size='22', name_long='Play data id').relation('sys.shared_object.id',
        #                                                                          relation_name='games',
        #                                                                           mode='foreignkey',
        #                                                                           onDelete='cascade')
        tbl.column('shared_data', dtype='X')
        tbl.column('shared_backup', dtype='X')

        tbl.formulaColumn('banner_img', "banner_url" ,dtype='P',name_long='!!Banner image',name_short='Banner', cell_format='auto:.5')
        tbl.formulaColumn('current_player_game', '(@players.player_id=:env_player_id)', dtype='B')
        tbl.formulaColumn('current_player_gm', '$gm_id=:env_player_id',  dtype='B')

        tbl.pyColumn('template_game',dtype='A',group='_',py_method='templateColumn', template_name='playcell')

    def defaultValues(self):
        consequences_slots=Bag()
        consequences_slots.setItem('mild', Bag(dict(code='mi', shifts=2, label='Mild')))
        consequences_slots.setItem('moderate', Bag(dict(code='mo', shifts=4, label='Moderate')))
        consequences_slots.setItem('severe', Bag(dict(code='se', shifts=6, label='Severe')))

        return dict( refresh=3,
                     pc_phases=3,
                      pc_aspects=5,initial_stunts=3,
                     gm_id=self.db.currentEnv.get('player_id'),
                     stress_tracks=Bag(),
                     #status='CO',
                     consequences_slots=consequences_slots)

    def configDefault_CORE(self, record=None):
        stressbag = record['stress_tracks']
        stressbag['p'] = Bag(dict(track_name='Physical',
                          n_boxes=2, code='p', 
                          skill='PHYSIQUE', 
                          extra_box_1=1,
                          extra_box_2=3,
                          extra_box_3=None))
        stressbag['m'] = Bag(dict(track_name='Mental',
                              n_boxes=2, 
                              code='m', 
                              skill='WILL',
                              extra_box_1=1,
                              extra_box_2=3,
                              extra_box_3=None))

        record.update(dict(pc_phases=3,
                     game_creation=True,
                     use_phases=True))

        if record['use_approaches']:
            record.update(dict( approach_set='STD'))
        else:
            consequences_slots = Bag(record['consequences_slots'])
            consequences_slots.setItem('mild2', Bag(dict(code='m2', 
                                      shifts=2, label='Mild opt.', 
                                      skill='PHYSIQUE',
                                      lv=5)),
                                      _position=1)
            record.update(dict(stunt_sets='STD',
                                skill_sets='STD',
                                 skill_cap=4,
                                 consequences_slots=consequences_slots))

    def configDefault_FAE(self, record=None):
        stressbag = record['stress_tracks']
        stressbag['s'] = Bag(dict(track_name='Stress',n_boxes=3, code='s'))
        record.update(dict(use_approaches=True,
                             approach_set='STD',
                             game_creation=False,
                             use_phases=False))

    @public_method
    def createNewPlayData(self, game_id, user, code, **kwargs):
        result = Bag()
        result['pcsheets'] = self.createCharacterSheets(game_id)
        result['world_aspects'] = Bag(dict(impending=Bag(),
                                           current = Bag(),
                                           faces=Bag(),
                                           places=Bag()))
        result['gm_tools'] = Bag()
        with self.recordToUpdate(game_id) as record:
            record['shared_data'] = result
        self.db.commit()
        return result

    def createCharacterSheets(self, game_id):
        game_player_tbl = self.db.table('fate.game_player')
        game_record = self.record(game_id).output('bag')
        players = game_player_tbl.query(columns='$player_id,$username',
                                        where='$game_id=:game_id AND $is_gm IS FALSE',
                                        game_id=game_id).fetch()
        result=Bag()
        for p in players:
            result[p['username']] = self.createEmptySheet(game_record)
        return result

    def prepareStressTrack(self, stress_tracks):
        result = Bag()
        for k,v in stress_tracks.items():
            n_boxes = v['n_boxes']
            max_boxes = n_boxes
            boxesBag = Bag([('b%i' % (i+1), None) for i in range(n_boxes)])
            if v['skill']:
                if v['extra_box_1']:
                    max_boxes = n_boxes+1
                    boxesBag.setItem('b%i'% (n_boxes+1), None)
                if v['extra_box_2']:
                    max_boxes = n_boxes+2
                    boxesBag.setItem('b%i'% (n_boxes+2), None)
                if v['extra_box_3']:
                    max_boxes = n_boxes+3
                    boxesBag.setItem('b%i'% (n_boxes+3), None)
            result[k] = Bag(dict(n_boxes = v['n_boxes'],
                                 boxes=boxesBag,
                                 max_boxes=max_boxes))
        return result

    def prepareApproaches(self, game_record):
        result = Bag()
        rates = [3,2,2,1,1,0]
        approaches = self.db.table('fate.approach').query(where='$approach_set=:approach_set',
                                            approach_set=game_record['approach_set']).fetch()
        for i,ap in enumerate(approaches):
            result[ap['name']] = rates['id']
        return result

    def prepareSkills(self, game_record):
        result = Bag()
        cap = game_record['skill_cap']
        for i in range(cap):
            #slots = cap - i
            rate = i+1
            result.setItem('lv%i'%rate,'')
        return result

    def prepareStunts(self, game_record):
        return Bag()
        #result = Bag()
        #for s in range(game_record['initial_stunts']):
        #    s =s+1
        #    stunt_key= 'st%i'%s
        #    result[stunt_key] = Bag(dict(name=None,
        #                                  description=None,
        #                                  _pkey=stunt_key,
        #                                  aspect_type='STUNT'))
        #return result

    def prepareAspects(self, game_record):
        result = Bag()
        aspect_types = self.db.table('fate.aspect_type').query().fetchAsDict(key='__syscode')
        story_labels = dict(PH1='Your Adventure', PH2='Crossing Paths', PH3='Crossing paths again')
        result['hc']= Bag(dict(aspect_type ='HC', _pkey='hc', 
                                phrase=None,
                                type_label=aspect_types['HC']['name']))
        result['tr'] = Bag(dict(aspect_type ='TR', _pkey='tr',
                                phrase=None,
                                type_label=aspect_types['TR']['name']))
        if game_record['use_phases']:
            for i in range(game_record['pc_phases']):
                p = i+1
                result['ph%i'%p]= Bag(dict(aspect_type ='PH',
                                       phase=p,
                                       type_label=aspect_types['P%i'%p]['name'],
                                       story_label=story_labels['PH%i'%p],
                                       phrase=None,
                                       _pkey='ph%i'%p,
                                       story=None))
        else:
            for i in range(2,game_record['pc_aspects']):
                i = i+1
                result['a%i'%i]= Bag(dict(aspect_type = 'PCA', 
                                       phrase=None,
                                       _pkey='a%i'%i))
        return result

    def prepareConsequences(self, consequences_slots):
        result = Bag()
        for cs in consequences_slots.values():
            result.setItem(cs['code'],
                           Bag(dict(phrase=None,
                                    shifts=cs['shifts'],
                                    code=cs['code'],
                                    label=cs['label'],
                                    is_hidden=(cs['skill'] != None))))
        return result
               
    def createEmptySheet(self, game_record):
        pcSheet = Bag()
        pcSheet['refresh'] = game_record['refresh']
        pcSheet['fate_points'] = pcSheet['refresh']
        pcSheet['skill_cap'] = game_record['skill_cap']
        pcSheet['n_stunts'] = game_record['initial_stunts']
        pcSheet['max_stunts'] = False
        pcSheet['stress_tracks'] = self.prepareStressTrack(game_record['stress_tracks'])
        pcSheet['consequences'] = self.prepareConsequences(game_record['consequences_slots'])
        if game_record['use_approaches']:
            pcSheet['approaches'] = self.prepareApproaches(game_record)
        else:
            pcSheet['skills'] = self.prepareSkills(game_record)
        pcSheet['stunts'] = Bag()
        pcSheet['aspects'] = self.prepareAspects(game_record)
        return pcSheet

    def trigger_onInserting(self,record=None):
        getattr(self,'configDefault_%(ruleset)s' %record)(record=record)
        if not record['code']:
            code = slugify(record['title'],'')[:20]
            record['code'] = code.upper()

    def trigger_onInserted(self,record=None):
        self.db.table('fate.game_player').insert(dict(game_id=record['id'],player_id=self.db.currentEnv.get('player_id')))

    #def trigger_onDeleted(self, record=None):
    #    if record['play_data_id']:
    #        self.db.table('sys.shared_object').delete(record['play_data_id'])
#

