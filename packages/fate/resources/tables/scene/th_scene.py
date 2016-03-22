#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('game_id')
        r.fieldcell('_row_count')

    def th_order(self):
        return 'game_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromGmTools(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', name='N.')
        r.fieldcell('scene_type',name='Type', width='6em')
        r.fieldcell('title',name='Title', width='13em')
        r.fieldcell('description',name='Description', width='100%')
        #r.fieldcell('template_scene',width='100%', name='-')

    def th_order(self):
        return '_row_count'




class Form(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        fb = bc.contentPane(region='top').div(margin_right='30px', padding='10px').formbuilder(cols=2,width='100%',
                border_spacing='4px', lbl_width='6em')
        fb.field('scene_type', lbl='Type', width='8em')
        fb.field('title', lbl='Title', width='17tem')
        fb.field('description', lbl='Description',colspan=2, height='50px', width='35em')
        tc =bc.tabContainer(region='center', datapath='#FORM')
        self.situationAspects(tc)
        self.npcs(tc)

    def situationAspects(self, tc):
        tc.templateGrid(title='Situation aspects',
                           frameCode='situationAspects',
                           datapath='#FORM.situation_aspects',
                            _class='aspectGrid',
                            addrow=True,
                            delrow=True,
                           storepath='#FORM.record.data.situation_aspects',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                                   dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])

    def npcs(self, tc):
        pane = tc.contentPane(title='Npcs in scene')
        pane.inlineTableHandler(relation='@npcs',
                               viewResource='ViewFromScene',
                               searchOn=False,
                                picker='npc_id',
                                picker_condition='game_id=:game_id AND $dead IS NOT TRUE',
                                picker_condition_game_id='=#FORM.record.game_id')
        #table='fate.npc',
        #condition='$id IN :npc_pkeys',
        #condition_npcs='=#FORM.record.npc_pkeys',



    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
