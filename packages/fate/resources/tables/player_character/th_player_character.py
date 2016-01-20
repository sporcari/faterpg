#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('player_id')
        r.fieldcell('game_id')
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('high_concept_id')
        r.fieldcell('trouble_id')
        r.fieldcell('refresh')
        r.fieldcell('fate_points')

    def th_order(self):
        return 'player_id'

    def th_options(self):
        return dict(virtualStore=False)


class ViewFromEmptyGamesheet(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('player_id', edit=True, width='100%')
        #r.fieldcell('name')
        #r.fieldcell('description')
        #r.fieldcell('high_concept')




class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='200px')
        topleft = top.contentPane(region='left', width='50%', margin='2px')
        topright= top.contentPane(region='center', datapath='#FORM', margin='2px')
        fb = topleft.formbuilder(cols=2, border_spacing='4px', fld_width='100%')
        fb.field('player_id')
        fb.field('game_id')
        fb.field('name', colspan=2)
        fb.field('description', tag='simpleTextArea', colspan=2, height='8ex')
        fb.field('fate_points')
        fb.field('refresh')
        topright.inlineTableHandler(relation='@aspects',
                                viewResource='ViewFromPC',
                                pbl_classes=True, title='Aspects',addrow=False,
                                delrow=False,
                                searchOn=False)

        center = bc.borderContainer(region='center', datapath='#FORM')
        cleft = center.contentPane(region='left', width='200px',margin='2px')
        ccenter = center.contentPane(region='center',margin='2px')

        
        cleft.inlineTableHandler(relation='@skills',
                                viewResource='ViewFromPC',
                                pbl_classes=True, title='Skills',
                                addrow=False,
                                delrow=False,
                                searchOn=False)
        ccenter.inlineTableHandler(relation='@stunts',
                                viewResource='ViewFromPC',
                                pbl_classes=True,
                                picker='stunt_id',
                                title='Stunts',addrow=False,
                                delrow=False,
                                searchOn=False)

        bottom = bc.borderContainer(region='bottom', height='190px')
        self.stressTracksGrid(bottom.contentPane(region='left', width='50%',margin='2px'))
        self.consequencesGrid(bottom.contentPane(region='center',margin='2px'))

    def stressTracksGrid(self, pane):
        grid = pane.quickGrid(value='^.stress_tracks',
                         title='Stress tracks')
        grid.column('track_name', name='Track', width='100%')
        grid.column('stress_boxes', name='Marked boxes',width='20em', 
                   edit=dict(tag='checkboxtext', values='=.values'))

    def consequencesGrid(self, pane):
        pane.div('conseq')
        #pane.inlineTableHandler(relation='@consequences',
        #                        viewResource='ViewFromPC',
        #                        pbl_classes=True, title='Consequences')
#


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
