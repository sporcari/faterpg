#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('approach_id')
        r.fieldcell('ruleset')
        r.fieldcell('action_type_id')
        r.fieldcell('skill_id')
        r.fieldcell('custom')

    def th_order(self):
        return 'name'

    def th_query(self):
        return dict(column='name', op='contains', val='')

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


