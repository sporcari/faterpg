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
        r.fieldcell('template_game',width='100%', name='-')
        r.cell('join_game',name="Join Game",calculated=True,width='6em',
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
        bar = top.bar.replaceSlots('5,vtitle','20,sections@status')
        bar = bar.replaceSlots('addrow','newgame')
        bar.newgame.slotButton('New Game',action='frm.newrecord({__ins_user:user,ruleset:"CORE",use_approaches:false})',
                                frm=self.newGameForm(bar).js_form,user=self.user,iconClass='iconbox add_row')


    def newGameForm(self,pane):
        dlg = pane.dialog(title='New Game')
        form = dlg.frameForm(frameCode='newgame',datapath='.newgame',height='140px',width='300px',store='memory',form_locked=False)
        fb = form.center.contentPane(padding='5px',datapath='.record').formbuilder(cols=1,border_spacing='3px',dbtable='fate.game')
        fb.dataController('dlg.show();',formsubscribe_onLoaded=True,dlg=dlg.js_widget)
        fb.dataController('dlg.hide();',formsubscribe_onDismissed=True,dlg=dlg.js_widget)
        fb.field('title',lbl='!!Title',width='18em',validate_notnull=True)
        fb.field('ruleset',lbl='!!Rulset',width='18em',validate_notnull=True)
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

class Form(BaseComponent):

    def th_form(self, form):
        form.record


class ConfigurationForm(BaseComponent):

    def th_form(self, form):
        form.dataController("this.form.goToRecord(pkey)",subscribe_configureGame=True)

        tc = form.center.tabContainer(datapath='.record',margin='2px')
        
        self.gameInfo(tc.borderContainer(title='Game'))
        
        self.configOptions(tc.borderContainer(region='center', title='Rules settings'))
        self.skillPreferences(tc.borderContainer(region='bottom',  datapath='#FORM', title='Skills', hidden='^#FORM.record.use_approaches'))
        form.dataRpc('#FORM.pcsheets',
                        self.db.table('fate.game').createCharacterSheets,
                                 game_id='=#FORM.record.id',
                                 _fired='^#FORM.prepareEmptySheets',
                                 _onResult="""var shared_id = 'game_'+kwargs._user+'_'+kwargs._code;
                                                var path = 'shared_game_data.'+shared_id;
                                                genro.setData(path,new gnr.GnrBag({'pcsheets':result}));
                                                
                            """,_user='=#FORM.record.__ins_user',_code='=#FORM.record.code')
        form.dataController("""
            var shared_id = 'game_'+user+'_'+code;
            var path = 'shared_game_data.'+shared_id;
            genro.som.registerSharedObject(path,shared_id,{expire:10000, saveOnClose:true, autoLoad:true});
            """,user='=#FORM.record.__ins_user',
               code='=#FORM.record.code',
                _fired='^#FORM.controller.loaded')

    def gameInfo(self, bc):
        top = bc.contentPane(region='top', height='80px').div(margin='10px')
        fb = top.formbuilder(cols=1, border_spacing='4px')
        fb.field('title', width='40em')
        fb.field('setting_tags', tag='checkBoxText', 
                  cols=2,
                  lbl='World tags',
                   popup=True,
                   table='fate.setting',
                   width='40em')
        center = bc.borderContainer(region='center')
        note = center.contentPane(region='center').roundedGroupFrame(title='Abstract')
        note.simpleTextArea(value='^.description',editor=True,speech=True)
        self.playersGrid(center.contentPane(region='right', width='280px', datapath='#FORM'))


    def playersGrid(self, pane):
        pane.inlineTableHandler(relation='@players',
            viewResource='ViewFromGame',
            searchOn=False,
            margin='2px',
            title='Players',pbl_classes='*')

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

    def configOptions(self,bc):

        self.stressTracksEditor(bc.contentPane(region='right', width='210px', margin='4px'))
        self.consequencesEditor(bc.contentPane(region='bottom', height='150px'))
        fb =bc.contentPane(region='center').div(margin='8px').formbuilder(cols=3,border_spacing='4px')
        fb.field('game_creation',lbl='', label='Coop Game creation', colspan=3)
        fb.field('use_phases', lbl='',label='Phases PC creation', colspan=3)       
        fb.field('approach_set', hidden='^.use_approaches?=!#v', colspan=3,width='100%', lbl='Appr.Set')
        fb.field('pc_phases', lbl='N.Phases', width='4em', hidden='^.use_phases?=!#v', validate_max=3)
        fb.field('pc_aspects', lbl='N.Aspects', width='4em')
        #fb.field('consequences_slots',lbl='Cons. slots', width='3em')
        fb.field('refresh',lbl='Refresh rate', width='4em')
        fb.field('initial_stunts',lbl='Initial Stunts', width='4em')
        fb.field('skill_cap',  width='4em', hidden='^.use_approaches')
        fb.div()
        fb.field('stunt_sets' ,width='100%', tag='checkBoxText',
                   colspan=3, 
                   lbl='Stunt sets',
                   cols='1',
                   popup=True,
                   table='fate.stunt_set')

    def consequencesEditor(self, pane):
        def struct(struct):
            r = struct.view().rows()
            r.cell('shifts', dtype='I', name='Shifts',width='4em', edit=True)
            r.cell('label', name='Label', width='100%', edit=True)
            r.cell('code', dtype='I', name='Code',width='4em', edit=True)
        pane.bagGrid(storepath='#FORM.record.consequences_slots',
            title='Consequences',pbl_classes=True,margin='2px',struct=struct,datapath='#FORM.consequences')




    def skillPreferences(self, bc):
        top = bc.roundedGroup(title='Skill sets' ,height='80px', region='top')
        fb =top.formbuilder(cols=1,border_spacing='3px', datapath='#FORM.record')
        fb.field('skill_sets' ,width='100%', colspan=2, tag='checkBoxText', 
                   lbl='',
                   cols='3',
                   table='fate.skill_set')
        skillpane = bc.contentPane(region='center', datapath='#FORM')
        skillpane.plainTableHandler(relation='@custom_skills',
             title='Custom skills',
             searchOn=False,
             configurable=False,
             addrow=True,
             delrow=True,
             pbl_classes=True,
             viewResource='ViewCustomFromGame')


    def stressTracksEditor(self, pane):
        def struct(struct):
            r = struct.view().rows()
            r.cell('track_name', name='Track', width='100%', edit=True)
            r.cell('n_boxes', dtype='I', name='Boxes',width='4em', edit=True)
            r.cell('max_boxes', dtype='I', name='Max',width='4em', edit=dict(validate_min='=.n_boxes'))

        pane.bagGrid(storepath='#FORM.record.stress_tracks',datapath='#FORM.stress',
            title='Stress tracks',pbl_classes=True,struct=struct,
                              grid_selfsubscribe_addrow="""genro.dlg.prompt('Add stress track', {
                                                    lbl:'Code',
                                                     action:function(value){
                                                        genro.publish('newtrack',{code:value})
                                                     }
                                                    });""")
        pane.dataController('stress_tracks.setItem(code,new gnr.GnrBag())', subscribe_newtrack=True, stress_tracks='=.stress_tracks')



    def th_bottom_custom(self,bottom):
        bar = bottom.slotBar('*,back,confirm,2',margin_bottom='2px')
        bar.back.button('!!Cancel',action='this.form.abort();')
        box = bar.confirm.div()
        box.slotButton('!!Create Empty Sheets',action="""SET #FORM.record.status = game_creation_status;
                                                        var that = this;
                                                        this.form.save({onReload:function(){
                                                                that.fireEvent('#FORM.prepareEmptySheets',true);
                                                            }});
                                                        """,game_creation_status = 'CR')#,hidden='^#FORM.record.status?=#v!="CO"')
        box.slotButton('!!Join Game',action="""genro.childBrowserTab('/tabletop/play/'+user+'/'+code);
                                                        """,
                                                        hidden='^#FORM.record.status?=#v=="CO"',
                                                        user='=#FORM.record.__ins_user',
                                                        code='=#FORM.record.code')

    def th_options(self):
        return dict(dialog_parentRatio=.8, showtoolbar=False)
