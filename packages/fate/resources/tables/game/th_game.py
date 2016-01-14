#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        #r.fieldcell('df_fbcolumns')
        #r.fieldcell('df_colswith')
        r.fieldcell('title')
        r.fieldcell('ruleset')
        r.fieldcell('gm_id')
        #r.fieldcell('weekday')
        #r.fieldcell('image')

    def th_order(self):
        return 'title'

    def th_query(self):
        return dict(column='title', op='contains', val='')

class ViewFromPlayerDashboard(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('shortname')
        r.fieldcell('title')
        r.fieldcell('description')
        r.fieldcell('setting_tags')
        r.fieldcell('ruleset')

        #r.fieldcell('weekday')
        #r.fieldcell('image')

    def th_order(self):
        return 'title'

    def th_condition(self):
        return dict(condition='$current_player_game IS TRUE')


class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='150px')
        base_info = top.roundedGroup(region='left', width='50%', title='Game info').div(margin_right='10px')
        fb = base_info.formbuilder(cols=2, border_spacing='4px', width='100%', fld_width='100%')
        fb.field('title', colspan=2)
        fb.field('shortname')
        fb.field('ruleset')
        fb.dataController("""var stBag = new gnr.GnrBag();
                             if (ruleset=='CORE'){
                                stBag.setItem('p.track_name','Phisical');
                                stBag.setItem('p.n_boxes',2);
                                stBag.setItem('m.track_name','Mental');
                                stBag.setItem('m.n_boxes',2);
                                stBag.setItem('m.skill_id',2);
                             }
                             if (ruleset=='FAE'){
                                stBag.setItem('s.track_name','Stress');
                                stBag.setItem('s.n_boxes',3);
                             }
                             SET .stress_tracks = stBag;""", ruleset='^.ruleset', _userChanges=True)

        fb.field('setting_tags', tag='checkBoxText', height='20px', cols=2, popup=True, colspan=2, table='fate.setting')
        self.playersGrid(top.contentPane(region='center', datapath='#FORM'))
        center = bc.borderContainer(region='center')
        self.configOptions(center.borderContainer(region='left', width='500px'))

    def playersGrid(self, pane):
        pane.inlineTableHandler(relation='@players',
            viewResource='ViewFromGame',
                                pbl_classes=True,title='Players')


    def configOptions(self,bc):
        top = bc.contentPane(region='top', height='180px')
        self.stressTracksEditor(bc.contentPane(region='center'))
        
        fb =top.formbuilder(cols=2,border_spacing='3px')
        fb.field('game_creation', lbl='',label='Cooperative Game creation')
        fb.div()
        fb.field('use_phases',lbl='',label='PC creation with phases')
        fb.field('pc_phases', lbl='N.Phases', width='4em')

        fb.field('pc_aspects', lbl='N.Aspects', width='4em')
        fb.field('refresh',lbl='Refresh rate', width='4em')
        fb.field('initial_stunts',lbl='Initial Stunts', width='4em')
        fb.field('consequences_slots',lbl='Cons. slots', width='4em')

    def stressTracksEditor(self, pane):
        grid = pane.quickGrid(value='^.stress_tracks',
                              selfsubscribe_addrow="""genro.dlg.prompt('Add stress track', {
                                                    lbl:'Code',
                                                     action:function(value){
                                                        genro.publish('newtrack',{code:value})
                                                     }
                                                    });""")
        pane.dataController('stress_tracks.setItem(code,new gnr.GnrBag())', subscribe_newtrack=True, stress_tracks='=.stress_tracks')
        grid.column('track_name', name='Track', width='12em', edit=True)
        grid.column('n_boxes', dtype='I', name='Boxes',width='4em', edit=True)
        grid.tools('delrow,addrow', position='BL')


        #fb.field('stress_tracks', lbl='Stress tracks', tag='filteringselect', values='s:Single Track,pm:Phisical and Mental')
        #fb.field('dflt_stress_boxes', lbl='Stress boxes')
        #

    def core_fields(self, pane):
        fb =pane.formbuilder(cols=2,border_spacing='3px')
        fb.field('skill_sets')
        fb.field('pc_phases', dtype='I',name_long='PC phases',name_short='PC phases')
        fb.field('skill_max_rate',dtype='I',name_long='Skill maximum rate',name_short='Skill max')
        
    def fae_fields(self, pane):
        fb.field('approach_set')

        



    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
