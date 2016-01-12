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
        r.fieldcell('name', edit=True, width='12em')
        r.fieldcell('description', edit=True, width='100%')
        r.fieldcell('action_type', edit=True, name='Action', width='10em')
        #r.fieldcell('ruleset', edit=True, width='10em')

    def th_order(self):
        return 'name'


