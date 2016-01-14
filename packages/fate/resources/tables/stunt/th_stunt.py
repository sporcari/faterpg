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
        r.fieldcell('once_per_scene',name='OPSc.', width='7em', edit=True)
        r.fieldcell('n_per_session',name='NPSes.', width='7em', edit=True)
        r.fieldcell('in_conflict',name='Conflict', width='7em', edit=True)
        r.fieldcell('spend_fp',name='Spend FP', width='7em', edit=True)



    def th_order(self):
        return 'name'


