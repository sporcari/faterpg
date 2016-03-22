#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('df_fbcolumns')
        r.fieldcell('df_colswith')
        r.fieldcell('name')
        r.fieldcell('description')
        r.fieldcell('game_id')
        r.fieldcell('image')
        r.fieldcell('npc_type_id')

    def th_order(self):
        return 'df_fbcolumns'

    def th_query(self):
        return dict(column='name', op='contains', val='')


class ViewFromGmTools(BaseComponent):

    def th_top_bar_custom(self,top):
        top.bar.replaceSlots('5,vtitle','5,vtitle,*,sections@npc_type')

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('npc_type')
        r.fieldcell('name', width='12em')
        r.fieldcell('description', width='100%')
        r.fieldcell('image_img')
        

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='140px')
        fb = top.contentPane(region='center').formbuilder(cols=4,width='94%',
                border_spacing='4px',lbl_width='6em', colswidth='auto',
                fld_width='100%')
        
        fb.field('name', lbl='Name', colspan=2)
        fb.field('npc_type', lbl='Type', colspan=1, validate_onAccept='if(value!="NL"){SET .mob=null;}')
        fb.field('mob' , lbl='Is Mob', hidden='^.@npc_type.can_be_mob?=!#v')

        fb.field('high_concept', lbl='High Concept',colspan=4, validate_notnull=True)
        fb.field('description', lbl='Description',colspan=4, height='64px')
        
        image_pane = top.contentPane(region='left',width='130px')
        image_pane.img(src='^.image_url', margin_right='10px',
                        crop_width='110px',crop_height='120px',
                        placeholder=self.getResourceUri('images/missing_photo.png'),
                        upload_folder='site:img/npc/avatar',edit=True,
                        rowspan=2,
                        upload_filename='=#FORM.record.id',crop_border='2px solid #ddd',
                        crop_rounded=8,crop_margin='5px',
                        crop_margin_left='10px',
                        zoomWindow=True)
        center = bc.borderContainer(region='center', datapath='.data')
        grid = self.aspects(center.contentPane(region='left', width='30%'))
        grid.dataController('grid.storebag().setItem("hc.phrase",hc, {_protect_delete:true})', hc='^#FORM.setHC', grid=grid.js_widget)

        self.skills(center.contentPane(region='center'))
        self.stunts(center.borderContainer(region='right', width='40%'))
        bottom = bc.borderContainer(region='bottom', datapath='.data', height='140px')
        self.stressTracksEditor(bottom.contentPane(region='left',
                                                   width='30%', title='Stress Tracks',
                                                   datapath='#FORM.record'))
        self.consequencesEditor(bottom.contentPane(region='center'))

    def stunts(self, bc):
        frame = bc.templateGrid(region='center',frameCode='npcStunts',
                           title='Stunts',
                           _class='aspectGrid',
                           datapath='#FORM.stunts',
                           storepath='.data.stunts',
                           template_resource='tpl/stunt',
                           contentCb='Fate.stuntsForm(pane, kw)')

        bar = frame.top.bar.replaceSlots('#','#,stuntsPicker')
        #bar.stuntsPicker.palettePicker(
        #    grid=frame.grid,
        #    width='600px',height='350px',
        #    table='fate.stunt',
        #    viewResource='ViewPicker_skill',
        #    checkbox=True,
        #    autoInsert=True,
        #    relation_field='name',
        #    defaults='name,description')

    def aspects(self, tc):
        frame = tc.templateGrid(title='Other Aspects',
                           frameCode='npcAspects',
                           datapath='#FORM.aspects',
                            _class='aspectGrid',
                            addrow=True,
                            delrow=True,
                           storepath='#FORM.record.data.aspects',
                           template_resource='tpl/aspect_CA',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                                   dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])
        return frame.grid

    def skills(self, pane):
        def struct(struct):
            r = struct.view().rows()
            r.cell('lv', dtype='I', name='Rate', width='4em', edit=dict(validate_max='=#FORM.record.skill_cap'))
            r.cell('skill', name='Skill', width='100%',
                    edit=dict(tag='dbSelect',
                              dbtable='fate.skill',
                              exclude=True,
                              condition='$skill_set IN :sets OR $game_id= :game_id',
                        condition_sets='^game_record.skill_sets?=#v?#v.split(","):[]',
                        condition_game_id='=game_record.id'))

            
        pane.bagGrid(storepath='#FORM.record.data.skills',
            title='Skills',pbl_classes=True,
            margin='2px',
            struct=struct,
            datapath='#FORM.skills')

    def stressTracksEditor(self, pane):


        def struct(struct):
            r = struct.view().rows()
            r.cell('track_name', name='Track', width='100%', edit=True)
            r.cell('n_boxes', dtype='I', name='Std. Boxes', width='6em', edit=True)

        frame = pane.bagGrid(storepath='#FORM.record.stress_tracks',
                    datapath='#FORM.stress',
                    title='Stress tracks',
                    grid_canSort=False,
                    pbl_classes=True,
                    struct=struct)

        bar = frame.top.bar.replaceSlots('addrow','addmenu')

        menu = bar.addmenu.menudiv(iconClass='add_row',tip='!!Add',
                        action='FIRE .grid.addTrack=$1',
                        #hiddenItemCb= 'genro.bp(true);',
                        parentForm=True)
        menu.menuLine('Physical', code='p', name='Physical')
        menu.menuLine('Mental', code='m', name='Mental')
        grid = frame.grid
        grid.dataController("""
                        var trackBag = grid.storebag();
                        var row = new gnr.GnrBag();
                        row.setItem('track_name', newtrack.name);
                        row.setItem('n_boxes', 1);
                        trackBag.setItem(newtrack.code, row);""",
                newtrack='^.addTrack' ,
                grid=grid.js_widget)  


    def consequencesEditor(self, pane):
        def struct(struct):
            r = struct.view().rows()
            r.cell('shifts', dtype='I', name='Shifts',width='4em', edit=dict(validate_notnull=True, validate_min=1, tag='combobox', values='2,4,6,8'))
            r.cell('cons_type', name='Type', width='100%', edit=dict(validate_notnull=True, tag='combobox', values='Mild,Mild2,Moderate,Severe'))

        frame = pane.bagGrid(storepath='#FORM.record.consequences_slots',
            title='Consequence slots',
            pbl_classes=True,
            margin='2px',
            struct=struct,
            grid_canSort=False,
            datapath='#FORM.consequences')

        bar = frame.top.bar.replaceSlots('addrow','addmenu')

        menu = bar.addmenu.menudiv(iconClass='add_row',tip='!!Add',
                        action='FIRE .grid.addCons=$1',
                        #'FIRE .grid.addTrack=$1.code',
                        #hiddenItemCb=hiddenItemCb,
                        parentForm=True)
        menu.menuLine('Mild', code='mild', name='Mild', shifts=2)
        menu.menuLine('Moderate', code='moderate', name='Moderate', shifts=4)
        menu.menuLine('Severe', code='severe', name='Severe', shifts=6)
        menu.menuLine('Other', code='other', name='Other', shift=1)
        grid = frame.grid
        grid.dataController("""
                        var consBag = grid.storebag();
                        var row = new gnr.GnrBag();
                        row.setItem('cons_type', newcons.name);
                        row.setItem('shifts', newcons.shifts);
                        consBag.setItem(newcons.code, row);""",
                newcons='^.addCons' ,
                grid=grid.js_widget)  




    def th_options(self):
        return dict(dialog_height='500px', dialog_width='900px', modal=True)

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        if newrecord:
            data = Bag()
            record['data'] = data
