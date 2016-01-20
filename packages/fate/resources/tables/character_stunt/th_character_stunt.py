#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('stunt_id')
        r.fieldcell('pc_id')
        r.fieldcell('npc_id')

    def th_order(self):
        return 'stunt_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')


class ViewFromPC(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('name', edit=dict(tag='dbcombobox',
                                    dbtable='fate.stunt',
                                    hasDownArrow='True',
                                    limit=30,
                                    selected_description='.description',
                                    selected_id='.stunt_id',
                                    selected_skill_id='.skill_id',
                                    selected_approach_id='.approach_id',
                                    selected_action_type='.action_type',
                                    selected_stunt_type='.stunt_type'), width='15em')

        r.fieldcell('description', edit=True, width='100%')
        #r.fieldcell('skill_id', edit=True, hidden='^.use_approaches')
        #r.fieldcell('approach_id', edit=True, hidden='^.use_approaches?=!#v')
        #r.fieldcell('action_type', edit=True)
        r.fieldcell('stunt_type', edit=True, name='Type', width='12em')
        #r.fieldcell('bonus',name='Bonus', width='9em', edit=True)
        #r.fieldcell('n_per_session',name='TPSes.', width='4em', edit=True)
        #r.fieldcell('n_per_scene',name='TPScn', width='4em', edit=True)
        #r.fieldcell('scene_type',name='Only for', width='8em', edit=True)
        #r.fieldcell('spend_fp',name='Spend FP', width='6em', edit=True)
#
    def th_order(self):
        return 'rate'



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('stunt_id')
        fb.field('pc_id')
        fb.field('npc_id')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
