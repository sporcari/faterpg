# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt_type',pkey='code',name_long='Stunt Type',name_plural='Stunt Types',caption_field='name',lookup=True)
        self.sysFields(tbl, id=False)
        tbl.column('code',size='4',name_long='Code',unique=True)
        tbl.column('name',name_long='Name')
        tbl.column('description',name_long='Description')
        tbl.column('ruleset',size=':4',name_long='Ruleset',name_short='Ruleset').relation('fate.ruleset.code',relation_name='stunt_types', mode='foreignkey', onDelete='raise')

    def sysRecord_NATS(self):
        return self.newrecord(code = 'NATS',
                            name='New action to skill',
                              description="""The most basic option for a stunt is to allow a skill to do something that it normally can’t do. It adds a new action onto the base skill in certain situations, for those with this stunt. This new action can be one that’s available to another skill (allowing one skill to swap for another under certain circumstances), or one that’s not available to any skill.""",
                              ruleset=self.db.table('fate.ruleset').sysRecord('CORE')['code'])


    def sysRecord_ABTA(self):
        return self.newrecord(code ='ABTA', name='Add bonus to action',
                              description="""Another use for a stunt is to give a skill an automatic bonus under a particular, very narrow circumstance, effectively letting a character specialize in something. The circumstance should be narrower than what the normal action allows, and only apply to one particular action or pair of actions.""",
                              ruleset=self.db.table('fate.ruleset').sysRecord('CORE')['code'])
    def sysRecord_CREX(self):
        return self.newrecord(code = 'CREX', name='Rules exception',
                              description="""Finally, a stunt can allow a skill to make a single exception, in a narrow circumstance, for any other game rule that doesn’t precisely fit into the category of an action. The Challenges, Contests, and Conflicts section is full of different little rules about the circumstances under which a skill can be used and what happens when you use them. Stunts can break those, allowing your character to stretch the boundaries of the possible.
The only limit to this is that a stunt can’t change any of the basic rules for aspects in terms of invoking, compelling, and the fate point economy. Those always remain the same.""",
                                ruleset=self.db.table('fate.ruleset').sysRecord('CORE')['code'])
    def sysRecord_BNAS(self):
        return self.newrecord(code='BNAS', name='+2 Bonus certain approach in a certain situation',
                              description="""Because I [describe some way that you are exceptional, have a cool bit of gear, or are otherwise awesome], I get a +2 when I [pick one: Carefully, Cleverly, Flashily, Forcefully, Quickly, Sneakily][pick one: attack, defend, create advantages, overcome] when [describe a circumstance].""",
                              ruleset=self.db.table('fate.ruleset').sysRecord('FAE')['code'])
    def sysRecord_OPSE(self):
        return self.newrecord(code='OPSE',name='Once per session exception',
                              description="""The second type of stunt lets you make something true, do something cool, or otherwise ignore the usual rules in some way. Use this template:""",
                              ruleset=self.db.table('fate.ruleset').sysRecord('FAE')['code'])
