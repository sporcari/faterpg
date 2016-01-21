# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('aspect_type', pkey='id',name_long='Aspect type',
                          name_plural='Aspect types',caption_field='name', rowcaption='$name')
        self.sysFields(tbl, hierarchical='name',counter=True, df=True)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description',unique=True)

    def sysRecord_GA(self):
        return self.newrecord(name='Game aspect',
                              description="""Game aspects are permanent fixtures of the game, hence the name. While they might change over time, they’re never going to go away. If you’ve already gone through game creation, you’ve already defined these—the current or impending issues that you came up with. They describe problems or threats that exist in the world, which are going to be the basis for your game’s story. Everyone can invoke, compel, or create an advantage on a game aspect at any time; they’re always there and available for anyone’s use.""")
    def sysRecord_CA(self):
        return self.newrecord(name='Character aspect',
                              description="""Character aspects are just as permanent, but smaller in scope, attached to an individual PC or NPC.""")
    def sysRecord_HC(self):
        return self.newrecord(name='High Concept',
                              description="""Your high concept is a phrase that sums up what your character is about—who he is and what he does. It’s an aspect, one of the first and most important ones for your character.""",
                              parent_id=self.sysRecord('CA')['id'])
    def sysRecord_TR(self):
        return self.newrecord(name='Trouble',
                              description="""Your trouble is the answer to a simple question: what complicates your character’s existence?
                              Trouble brings chaos into a character’s life and drives him into interesting situations. Trouble aspects are broken up into two types: personal struggles and problematic relationships.""",
                              parent_id=self.sysRecord('CA')['id'])
    def sysRecord_P1(self):
        return self.newrecord(name='Phase 1',
                              description="""The first phase is your character’s first true adventure—his first book, episode, case, movie, whatever—starring him""",
                              parent_id=self.sysRecord('CA')['id'])
    def sysRecord_P2(self):
        return self.newrecord(name='Phase 2',
                              description="""Your character has a supporting role in the story you’re holding, which you get to come up with right now.""",
                              parent_id=self.sysRecord('CA')['id'])
    def sysRecord_P3(self):
        return self.newrecord(name='Phase 3',
                              description="""Phase three, where you’ll contribute to this second adventure and determine your next aspect. Follow the directions from phase two.""",
                              parent_id=self.sysRecord('CA')['id'])
    def sysRecord_SA(self):
        return self.newrecord(name='Situation aspect',
                              description="""A situation aspect is temporary, intended to last only for a single scene or until it no longer makes sense (but no longer than a session, at most). Situation aspects can be attached to the environment the scene takes place in—which affects everybody in the scene—but you can also attach them to specific characters by targeting them when you create an advantage.""")
    def sysRecord_CO(self):
        return self.newrecord(name='Consequence',
                              description="""A consequence is more permanent than a situation aspect, but not quite as permanent as a character aspect. They’re a special kind of aspect you take in order to avoid getting taken out in a conflict, and they describe lasting injuries or problems that you take away from a conflict (Dislocated Shoulder, Bloody Nose, Social Pariah). Consequences stick around for a variable length of time, from a few scenes to a scenario or two, depending on how severe they are.""")
    def sysRecord_BO(self):
        return self.newrecord(name='Boost',
                              description="""Boosts are a super-transient kind of aspect. You get a boost when you’re trying to create an advantage but don’t succeed well enough, or as an added benefit to succeeding especially well at an action. You get to invoke them for free, but as soon as you do, the aspect goes away. If you want, you can also allow another character to invoke your boost, if it’s relevant and could help them out.""")
    def sysRecord_FP(self):
        return self.newrecord(name='Faces & Places',
                              description='Decide who the important people and locations are')
    