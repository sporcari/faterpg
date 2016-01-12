# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('ruleset',pkey='code',name_long='Ruleset',name_plural='Rulesets',caption_field='name',lookup=True)
        self.sysFields(tbl, id=False)
        tbl.column('code',size=':4',name_long='Code',name_short='Code',unique=True,indexed=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('skill_set',size='3',name_long='Skill set',name_short='Skill set').relation('fate.skill_set.code',
                                              relation_name='rulesets',
                                              mode='foreignkey',
                                              onDelete='raise')
        tbl.column('approach_set',size='3',name_long='Approaches',name_short='Approaches').relation('fate.approach_set.code',
                                                relation_name='rulesets',
                                                mode='foreignkey',
                                                onDelete='raise')

    def sysRecord_CORE(self):
        return self.newrecord(code='CORE',
                              name='Fate Core',
                              description='Fate Core',
                              skill_set=self.db.table('fate.skill_set').sysRecord('STD')['code'])

    def sysRecord_FAE(self):
        return self.newrecord(code='FAE',
                              name='Accelerated Edition',
                              description='Fate Accelerated Edition',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'])



