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
        return dict(column='title', op='contains', val='' )

    def th_options(self):
        return dict(widget='dialog')

class ViewFromPlayerDashboard(BaseComponent):

    def th_hiddencolumns(self):
        return '$code,$title,$description,$setting_tags,$ruleset,$__ins_user'

    def th_struct(self,struct):

        r = struct.view().rows()
        r.fieldcell('template_game',width='100%')
        r.cell('apri_tab',name="Apri",calculated=True,width='3em',
                    cellClasses='cellbutton',
                    format_buttonclass='icon48 arrow_right iconbox',
                    format_isbutton=True,format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                                           genro.childBrowserTab('/tabletop/play/'+row['__ins_user']+'/'+row['code']);""")

        #r.fieldcell('weekday')
        #r.fieldcell('image')

    def th_order(self):
        return 'title'

    def th_condition(self):
        return dict(condition='$current_player_game IS TRUE')

    def th_top_bar_custom(self,top):
        bar = top.bar.replaceSlots('vtitle','sections@status')
        bar = bar.replaceSlots('addrow','newgame')
        bar.newgame.slotButton('New Game',action='frm.newrecord({__ins_user:user,ruleset:"CORE",use_approaches:false})',
                                frm=self.newGameForm(bar).js_form,user=self.user)


    def newGameForm(self,pane):
        dlg = pane.dialog(title='New Game')
        form = dlg.frameForm(frameCode='newgame',datapath='.newgame',height='200px',width='300px',store='memory',form_locked=False)
        fb = form.center.contentPane(padding='5px',datapath='.record').formbuilder(cols=1,border_spacing='3px',dbtable='fate.game')
        fb.dataController('dlg.show();',formsubscribe_onLoaded=True,dlg=dlg.js_widget)
        fb.dataController('dlg.hide();',formsubscribe_onDismissed=True,dlg=dlg.js_widget)
        fb.field('code',lbl='Code',width='4em',validate_nodup=True,
                            validate_nodup_relative='__ins_user')
        fb.field('title',lbl='!!Title',width='15em',validate_notnull=True)
        fb.field('ruleset',lbl='!!Rulset',width='15em',validate_notnull=True)
        fb.field('use_approaches',lbl='',label='!!Use approaches',row_hidden='^.ruleset?=#v=="FAE"')
        bar = form.bottom.slotBar('*,cancel,confirm,2',_class='slotbar_dialog_footer')
        bar.cancel.slotButton('!!Cancel',action='this.form.abort()')
        bar.confirm.slotButton('!!Confirm',action='FIRE #FORM.confirm;')
        bar.dataRpc('dummy',self.createNewGame,code='=#FORM.record.code',title='=#FORM.record.title',
                    use_approaches='=#FORM.record.use_approaches',
                    ruleset='=#FORM.record.ruleset',
                    _fired='^#FORM.confirm',
                    _onCalling="if(!this.form.isValid()){return;}",
                    _onResult="""
                                genro.publish('configureGame',{pkey:result});
                                this.form.abort();
                            """)
        return form

    @public_method
    def createNewGame(self,code=None,title=None,ruleset=None,use_approaches=None):
        tblobj = self.db.table('fate.game')
        record = tblobj.newrecord(code=code,title=title,ruleset=ruleset,use_approaches=use_approaches)
        tblobj.insert(record)
        self.db.commit()
        return record['id']


class ConfigurationForm(BaseComponent):

    def th_form(self, form):
        form.dataController("this.form.goToRecord(pkey)",subscribe_configureGame=True)
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='160px')
        base_info = top.roundedGroup(region='left', width='50%', title='Game info').div(margin_right='10px')
        fb = base_info.formbuilder(cols=2, border_spacing='4px', width='100%', fld_width='100%')
        fb.field('title', colspan=2)
        #fb.field('code', validate_regex='![^A-Za-z0-9_]', 
        #        validate_regex_error='!!Invalid code: "." char is not allowed',disabled=True)
        fb.field('setting_tags', tag='checkBoxText', 
                  cols=2,
                   popup=True, 
                   colspan=2, 
                   table='fate.setting')
        fb.field('description', tag='simpleTextArea', colspan=2, height='8ex')
        self.playersGrid(top.contentPane(region='center', datapath='#FORM'))
        self.configOptions(bc.roundedGroupFrame(region='center', title='Game configuration'))
        self.skillPreferences(bc.borderContainer(region='bottom', height='200px'))
        bc.dataController("bc.setRegionVisible('bottom',!use_approaches);",use_approaches='^.use_approaches',bc=bc.js_widget)

    def playersGrid(self, pane):
        pane.inlineTableHandler(relation='@players',
            viewResource='ViewFromGame',
                                pbl_classes=True,title='Players')

    def imagePane(self, pane):
        pane.img(src='^.banner_url', #crop_width='110px',crop_height='110px',
                        #placeholder=self.getResourceUri('images/missing_photo.png'),
                        upload_folder='site:img/games/banner',edit=True,
                        rowspan=2,
                        crop_height='78px',
                        upload_filename='=#FORM.record.id',crop_border='2px solid #ddd',
                        crop_rounded=8,crop_margin='4px',
                        #crop_margin_left='2px',
                        zoomWindow=True)

    def configOptions(self,frame):
        bc=frame.center.borderContainer(region='center')
        left = bc.contentPane(region='left', width='220px', margin='4px')
        center = bc.contentPane(region='center', margin='4px')
        self.stressTracksEditor(bc.contentPane(region='right', width='210px', margin='4px'))
        
        fb =left.formbuilder(cols=1,border_spacing='3px')
        fb.field('game_creation',lbl='', label='Coop Game creation')
        fb.field('use_phases', lbl='',label='Phases PC creation')       
        fb =center.formbuilder(cols=3,border_spacing='3px')
        fb.field('approach_set', hidden='^.use_approaches?=!#v', colspan=3,width='100%', lbl='Appr.Set')
        fb.field('pc_phases', lbl='N.Phases', width='3em', hidden='^.use_phases?=!#v', validate_max=3)
        fb.field('pc_aspects', lbl='N.Aspects', width='3em')
        fb.field('consequences_slots',lbl='Cons. slots', width='3em')
        
        fb.field('refresh',lbl='Refresh rate', width='3em')
        fb.field('initial_stunts',lbl='Initial Stunts', width='3em')
        fb.field('skill_cap',  width='3em', hidden='^.use_approaches')
        fb.field('stunt_sets' ,width='100%', tag='checkBoxText',
                   colspan=3, 
                   lbl='Stunt sets',
                   cols='1',
                   popup=True,
                   table='fate.stunt_set')

    def skillPreferences(self, bc):
        top = bc.roundedGroup(title='Skills configuration' ,height='50px', region='top')
        fb =top.formbuilder(cols=1,border_spacing='3px')
        
        fb.field('skill_sets' ,width='100%', colspan=2, tag='checkBoxText', 
                   lbl='',
                   cols='3',
                   table='fate.skill_set')
        skillpane = bc.contentPane(region='center', datapath='#FORM')
        skillpane.dialogTableHandler(relation='@custom_skills',
            title='Custom skills',
                                      viewResource='ViewCustomFromGame',
                                      formResource='FormFromGame')


    def stressTracksEditor(self, pane):
        grid = pane.quickGrid(value='^.stress_tracks',
            title='Stress tracks',
                              selfsubscribe_addrow="""genro.dlg.prompt('Add stress track', {
                                                    lbl:'Code',
                                                     action:function(value){
                                                        genro.publish('newtrack',{code:value})
                                                     }
                                                    });""")
        pane.dataController('stress_tracks.setItem(code,new gnr.GnrBag())', subscribe_newtrack=True, stress_tracks='=.stress_tracks')
        grid.column('track_name', name='Track', width='100%', edit=True)
        grid.column('n_boxes', dtype='I', name='Boxes',width='4em', edit=True)
        grid.tools('delrow,addrow', position='BR')


    def th_bottom_custom(self,bottom):
        bar = bottom.slotBar('*,back,confirm,2',margin_bottom='2px',_class='slotbar_dialog_footer')
        bar.back.button('!!Cancel',action='this.form.abort();')
        box = bar.confirm.div()
        box.slotButton('!!Start Game',action="""SET #FORM.record.status = game_creation_status;
                                                        this.form.save();
                                                        """,game_creation_status = 'CR',
                                                        hidden='^#FORM.record.status?=#v!="CO"')
        box.slotButton('!!Open Game',action="""genro.childBrowserTab('/tabletop/play/'+user+'/'+code);
                                                        """,
                                                        hidden='^#FORM.record.status?=#v=="CO"',
                                                        user='=#FORM.record.__ins_user',
                                                        code='=#FORM.record.code')

    def th_options(self):
        return dict(dialog_height='660px', dialog_width='880px', autoSave=True,showtoolbar=False)
