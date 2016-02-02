# encoding: utf-8

from gnr.core.gnrdecorator import metadata
from gnr.core.gnrbag import Bag

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('skill',pkey='code',name_long='Skill',name_plural='Skills',caption_field='name')
        self.sysFields(tbl, id=False)
        tbl.column('code', size=':20',name_long='Code',name_short='Code',unique=True)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('special',name_long='Special rule',name_short='Special')
        tbl.column('skill_set',size='3',name_long='Skill set',name_short='Skill set').relation('fate.skill_set.code',relation_name='skills', mode='foreignkey', onDelete='cascade')
        tbl.column('game_id', size='22', name_long='Game id').relation('fate.game.id', relation_name='custom_skills', mode='foreignkey', onDelete='cascade')
        tbl.column('stresstrack_changes', dtype='X')
        tbl.column('action_types', dtype='X')
        tbl.aliasColumn('actions', relation_path='@actions.action_type', name_long='Actions')
        #tbl.aliasColumn('set', relation_path='@skill_set.code', name_long='Set')
        tbl.aliasColumn('game', relation_path='@game_id.code', name_long='Game')

    def assignCode(self, record):
        record['code'] = record['name'].upper().replace(',','_').replace(' ','_')

    def trigger_onInserting(self, record):
        if not record['code']:
            self.assignCode(record)

    def setActionTypes(self, record):
        actSkills = self.db.table('fate.action_skill').query(where='$skill_id=:id', id=record['id']).fetch()
        asbag = Bag()
        for action_skill in actSkills:
            print record['name'],action_skill['action_type']
            asbag[action_skill['action_type']] = Bag(dict(description=action_skill['description'], 
                                                          action_type=action_skill['action_type']))
        record['action_types'] = asbag

    @metadata(doUpdate=True)
    def touch_assignCode(self, record, old_record):
        self.assignCode(record)

    @metadata(doUpdate=True)
    def touch_setActionTypes(self, record, old_record):
        self.setActionTypes(record)

