# encoding: utf-8

from gnr.core.gnrbag import Bag


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('npc',pkey='id',name_long='Non-player character',name_plural='NPCS',caption_field='name')
        self.sysFields(tbl,df=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('high_concept',name_long='High Concept',name_short='HC')
        tbl.column('game_id',size='22',name_long='Game',name_short='Game')
        tbl.column('image_url',name_long='Image',name_short='Image')
        tbl.column('npc_type',size=':2',name_long='NPC Type',name_short='Type').relation('fate.npc_type.code', mode='foreignkey',onDelete='raise')
        tbl.column('mob', dtype='B', name_long='Mob')
        tbl.column('mob_size', dtype='L', name_long='Mob Size')
        tbl.column('dead', dtype='B', name_long='Dead')
        tbl.column('stress_tracks', dtype='X')
        tbl.column('consequences_slots', dtype='X')
        tbl.column('data', dtype='X', _sendback=True)
        tbl.formulaColumn('image_img', "image_url" ,dtype='P',name_long='!!Portrait',name_short='Portrait', cell_format='auto:.5')

    def prepareEmptyStressTracks(self, st_definition, st_data):
        for k,v in st_definition.items():
            n_boxes = v['n_boxes']
            for j in range(n_boxes):
                st_data.setItem('%s.boxes.%i' % (k,j+1), False)

    def shared_onLoading(self, record):
        record['data.metadata'] = Bag(name=record['name'],
                                       description=record['description'],
                                       mob=record['mob'],
                                       image_url=record['image_url'],
                                       mob_size=record['mob_size'],
                                       npc_type=record['npc_type'],
                                       high_concept=record['high_concept'])
        if record['data.aspects']:
            record['data.aspects'].setItem('hc', Bag(phrase=record['high_concept']), _position='<')
        record['data.boosts'] = Bag()
        record['data.situation_aspects'] = Bag()

        if not record['data.stress_tracks'] and record['stress_tracks']:
            record['data.stress_tracks']= Bag()
            if not record['mob']:
                self.prepareEmptyStressTracks(record['stress_tracks'], record['data.stress_tracks'])

            else:
                for i in range(record['mob_size']):
                    minion_st= Bag()
                    self.prepareEmptyStressTracks(record['stress_tracks'], minion_st)
                    record['data.stress_tracks'].setItem('nl%i' % i, minion_st)

        if not record['data.consequences'] and record['consequences_slots']:
            record['data.consequences'] = Bag(record['consequences_slots'])
            for k,v in record['data.consequences']:
                v.setItem('phrase',None)


    def shared_onSaving(self, record):
        print 'ON SAVING NPC'
        #if not record['data.aspects']:
        #    print x
        record['data.aspects'].pop('hc',None)




                
        





