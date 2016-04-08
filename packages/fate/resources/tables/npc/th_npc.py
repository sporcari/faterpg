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
        bar = top.bar.replaceSlots('5,vtitle','5,npctitle,*,sections@npc_type')
        bar.npctitle.div('NPCS')

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('npc_type')
        r.fieldcell('name', width='12em')
        r.fieldcell('description', width='100%')
        r.checkboxcolumn('set_in_scene', name='In Scene', width='6em', checkedId='current_scene.npc_pkeys')

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        bar = form.bottom.bar.replaceSlots('#','#,clearSC')
        bar.clearSC.slotButton('Clear Stress & Cons', action="""SET #FORM.record.data.stress_tracks =null;
                                                                SET #FORM.record.data.consequences =null;""")


        top = bc.borderContainer(region='top', height='140px')
        fb = top.contentPane(region='center').formbuilder(cols=5,width='94%',
                border_spacing='4px',lbl_width='6em', colswidth='auto',
                fld_width='100%')
        
        fb.field('name', lbl='Name', colspan=2)
        fb.field('npc_type', lbl='Type', colspan=1, validate_onAccept='if(value!="NL"){SET .mob=null;}')
        fb.field('mob' , lbl='Is Mob', hidden='^.@npc_type.can_be_mob?=!#v')
        fb.field('mob_size' , lbl='Mob size', hidden='^.mob?=!#v', validate_notnull='^.mob', width='4em')

        fb.field('high_concept', lbl='High Concept',colspan=5, validate_notnull=True)
        fb.field('image_url', lbl='Img Url',colspan=5)

        #fb.field('description', lbl='Description',colspan=5, height='64px')
        
        image_pane = top.contentPane(region='left',width='130px')
        image_pane.div(width='110px',height='120px',margin_right='10px',margin='5px',margin_left='10px',rowspan=2
                    ).img(src='^.image_url',placeholder=self.getResourceUri('css/images/social.svg'),
                            upload_folder='site:img/npc/avatar',height='100%',width='100%',edit=True,
                            upload_filename='=#FORM.record.id')

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
                           storepath='#FORM.record.data.stunts',
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
            r.cell('lv', dtype='I', name='Rate', width='4em',
                    _customGetter="""function(row,idx){
                        var n = this.grid.dataNodeByIndex(idx);
                        return parseInt(n.label.slice(2));
                    }""")
            r.cell('skills',_customGetter="""function(row,idx){
                        var n = this.grid.dataNodeByIndex(idx);
                        return n.getValue();
                    }""", name='Skills', width='100%')

        self.npcSkillsPicker(pane)
        pane.dataController('skillbag.sort("#k");', skillbag='^#FORM.record.data.skills', _if='skillbag')
        frame = pane.bagGrid(storepath='#FORM.record.data.skills',
                            title='Skills',
                            pbl_classes=True,
                            margin='2px',
                            datamode='attr',
                            addrow=False,delrow=False,
                            struct=struct,
                            datapath='#FORM.npc_skills')

        bar = frame.top.bar.replaceSlots('#','#,skillsButton,2')
        bar.skillsButton.slotButton('View Skills',
                                iconClass='iconbox app',
                                action='PUBLISH openNpcSkillsPicker;')
        

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
            r.cell('label', name='Type', width='100%', edit=dict(validate_notnull=True, tag='combobox', values='Mild,Mild2,Moderate,Severe'))

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
        menu.menuLine('Mild', code='mi', name='Mild', shifts=2)
        menu.menuLine('Moderate', code='mo', name='Moderate', shifts=4)
        menu.menuLine('Severe', code='se', name='Severe', shifts=6)
        menu.menuLine('Other', code='m2', name='Mild Opt', shift=2)
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

    def npcSkillsPicker(self, pane):
        dlg = pane.dialog(title='Choose skills',
                          closable=True,
                          datapath='main.pickers.npc_skills_picker',
                          subscribe_openNpcSkillsPicker="""this.widget.show();
                                                         """)
        
        th = dlg.plainTableHandler(table='fate.skill',
            height='490px', width='350px',
            nodeId='npcSkillsPickerGrid',
                        condition='$skill_set IN :sets OR $game_id= :game_id',
                        condition_sets='^game_record.skill_sets?=#v?#v.split(","):[]',
                        condition_game_id='=game_record.id',
                        configurable=False,
                        viewResource='ViewPicker',
                        view_store_onStart=True,
                        view_grid_userSets='#FORM.record.data.skills')
        bar = th.view.bottom.slotBar('*,done,2',_class='slotbar_dialog_footer')
        bar.done.slotButton('!!Done',action="dlg.hide();",dlg=dlg.js_widget)

        dlg.dataController("""for (var i=1; i<=skill_cap;i++){
                                grid.addNewSetColumn({field:'lv'+i, 
                                                      name:i, 
                                                      skillmax:skill_cap,
                                                      position:'>',
                                                      _customGetter:function(rowdata,rowIdx){return Fate.skillsSetGetter(this,rowdata,rowIdx)}
                                                      })
                                }
                                """, grid=th.view.grid.js_widget,
                               skill_cap = 8, 
                               _onStart=True)





    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        if newrecord:
            data = Bag()
            record['data'] = data
