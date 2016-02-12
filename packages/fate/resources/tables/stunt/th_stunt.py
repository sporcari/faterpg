#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', width='20em')
        r.fieldcell('stunt_set',name='Set', width='3em')
        r.fieldcell('description',width='100%')
        #r.fieldcell('skill_id',name='Skill', width='11em')
        #r.fieldcell('approach_id',name='Approach', width='11em')
        #
        #r.fieldcell('action_type',name='Action', width='11em')
        #r.fieldcell('stunt_type', name='Type', width='14em')
        #r.fieldcell('bonus',name='Bonus', width='9em')
        #r.fieldcell('skill_stunt',name='Skill Stunt', width='8em')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

    def th_options(self):
        return dict(virtualStore=False)

class ViewPicker_skill(BaseComponent):

    #def th_top_custom(self,top):
    #    top.bar.replaceSlots('vtitle','sections@skill_code', 
    #                           sections_skill_code_multiButton=False,
    #                           sections_skill_code_all_begin=False)

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('skill_code',name='Skill', width='8em')
        r.fieldcell('name', width='17em')
        r.fieldcell('description',width='100%')
        r.fieldcell('action_type',name='Action', width='11em')
        r.fieldcell('stunt_type', name='Type', width='14em')
        r.fieldcell('bonus',name='Bonus', width='9em')

    def th_order(self):
        return 'skill_code,name'
        



class Form(BaseComponent):

    def th_form(self,form):
        form.record
        

class ViewFromSkill(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', edit=True, width='20em')
        r.fieldcell('description', edit=dict(tag='simpletextarea', height='10ex'), width='100%')
        r.fieldcell('action_type', edit=True, name='Action', width='11em')
        r.fieldcell('stunt_type', edit=dict(condition="$ruleset='CORE'"), name='Type', width='14em')
        r.fieldcell('bonus',name='Bonus', width='9em', edit=True)
        r.fieldcell('n_per_session',name='TPSes.', width='4em', edit=True)
        r.fieldcell('n_per_scene',name='TPScn', width='4em', edit=True)
        r.fieldcell('scene_type',name='Only for', width='8em', edit=True)
        r.fieldcell('spend_fp',name='Spend FP', width='6em', edit=True)

    def th_order(self):
        return 'name'

class ViewStuntsPicker(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name',  width='20em')
        r.fieldcell('description',width='100%')
        r.fieldcell('action_type',name='Action', width='11em')
        r.fieldcell('stunt_type', name='Type', width='14em')
        r.fieldcell('bonus',name='Bonus', width='9em')
   
    def th_order(self):
        return 'name'


