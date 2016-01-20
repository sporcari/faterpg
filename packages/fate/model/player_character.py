# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('player_character',pkey='id',name_long='Player Character',name_plural='Characters',caption_field='name')
        self.sysFields(tbl)
        tbl.column('player_id',size='22',name_long='Player',name_short='Player').relation('fate.player.id',relation_name='characters', mode='foreignkey', onDelete='setnull')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game').relation('fate.game.id',relation_name='player_characters', mode='foreignkey')
        tbl.column('name',size=':40',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('refresh',dtype='I',name_long='Refresh',name_short='Refresh')
        tbl.column('high_concept_id',size='22',name_long='High concept',name_short='High concept').relation('fate.aspect.id',relation_name='defined_pc', mode='foreignkey', one_one=True,  onDelete='setnull')
        tbl.column('trouble_id',size='22',name_long='Trouble',name_short='Trouble').relation('fate.aspect.id',relation_name='troubled_pc', mode='foreignkey', one_one=True, onDelete='setnull')
        tbl.column('fate_points',dtype='I',name_long='Fate Points',name_short='Fate Points')
        tbl.column('image', name_long='Image',name_short='Image')
        tbl.column('stress_tracks', dtype='X', name_short='Stress tracks')
        tbl.aliasColumn('high_concept','@high_concept_id.phrase', name_long='High concept')
        tbl.aliasColumn('trouble', '@trouble_id.phrase', name_long='Trouble')

    def createEmptySheet(self, player_id, game_record):
        pc_record = dict()
        pc_record['player_id'] = player_id
        pc_record['game_id'] = game_record['id']
        pc_record['refresh'] = game_record['refresh']
        pc_record['fate_points'] = pc_record['refresh']
        char_approach_tbl = self.db.table('fate.character_approach')
        char_skill_tbl = self.db.table('fate.character_skill')
        char_stunt_tbl = self.db.table('fate.character_stunt')
        at_tbl = self.db.table('fate.aspect_type')
        aspect_tbl = self.db.table('fate.aspect')
        pc_record['stress_tracks'] = game_record['stress_tracks']
        for v in game_record['stress_tracks'].values():
            v.setItem('values', ','.join(['b%i' % (i+1) for i in range(v['n_boxes'])]))
        self.insert(pc_record)
        pc_oldrecord = dict(pc_record)
        character_id = pc_record['id']
        if game_record['use_approaches']:
            rates = [3,2,2,1,1,0]
            approaches = self.db.table('fate.approach').query(where='$approach_set=:approach_set',
                                                              approach_set=game_record['approach_set']).fetch()
            for i,ap in enumerate(approaches):
                char_approach_tbl.insert(dict(character_id=character_id, approach_id=ap['id'], rate=rates[i]))
        else:
            cap = game_record['skill_cap']
            for i in range(cap):
                slots = cap - i
                rate = i+1
                for s in range(slots):
                    char_skill_tbl.insert(dict(pc_id=character_id, rate=rate))
        for s in range(game_record['initial_stunts']):
            char_stunt_tbl.insert(dict(pc_id=character_id))
        hc = dict(game_id=game_record['id'],
                    pc_id=character_id, 
                 aspect_type_id = at_tbl.sysRecord('HC')['id'])
        aspect_tbl.insert(hc)
        pc_record['high_concept_id']= hc['id']
        tr = dict(game_id=game_record['id'],
                pc_id=character_id, 
                 aspect_type_id = at_tbl.sysRecord('TR')['id'])
        aspect_tbl.insert(tr)
        pc_record['trouble_id']= tr['id']
        if game_record['use_phases']:
            for i in range(game_record['pc_phases']):
                p = i+1
                aspect_tbl.insert(dict(pc_id=character_id,
                                game_id=game_record['id'],
                              aspect_type_id = at_tbl.sysRecord('P%i'%p)['id']))
        
        self.update(pc_record, pc_oldrecord)
        return pc_record['id']



