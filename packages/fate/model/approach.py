# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('approach',pkey='name',name_long='Approach',name_plural='Approaches',caption_field='name',lookup=True)
        self.sysFields(tbl, id=False)
        tbl.column('name',name_long='Name',name_short='Name',unique=True,indexed=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('approach_set',size='3',name_long='Set',name_short='Set').relation('fate.approach_set.code',
                                                                                  relation_name='approaches', 
                                                                                  mode='foreignkey', onDelete='cascade')

    def sysRecord_CA(self):
        return self.newrecord(name='Careful',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description="""A Careful action is when you pay close attention to detail and take your time to do the job right. Lining up a long-range arrow shot. Attentively standing watch. Disarming a bank’s alarm system.""")
    def sysRecord_CL(self):
        return self.newrecord(name='Clever',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description="""A Clever action requires that you think fast, solve problems, or account for complex variables. Finding the weakness in an enemy swordsman’s style. Finding the weak point in a fortress wall. Fixing a computer.""")
    def sysRecord_FL(self):
        return self.newrecord(name='Flashy',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description="""A Flashy action draws attention to you; it’s full of style and panache. Delivering an inspiring speech to your army. Embarrassing your opponent in a duel. Producing a magical fireworks display.""")
    def sysRecord_FO(self):
        return self.newrecord(name='Forceful',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description="""A Forceful action isn’t subtle—it’s brute strength. Wrestling a bear. Staring down a thug. Casting a big, powerful magic spell.""")
    def sysRecord_QU(self):
        return self.newrecord(name='Quick',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description="""A Quick action requires that you move quickly and with dexterity. Dodging an arrow. Getting in the first punch. Disarming a bomb as it ticks 3… 2… 1…""")
    def sysRecord_SN(self):
        return self.newrecord(name='Sneaky',
                              approach_set=self.db.table('fate.approach_set').sysRecord('STD')['code'],
                              description=""" A Sneaky action is done with an emphasis on misdirection, stealth, or deceit. Talking your way out of getting arrested. Picking a pocket. Feinting in a sword fight.""")



                              


