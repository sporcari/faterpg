#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method,metadata

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
        return '$code,$title,$description,$setting_tags,$ruleset,$__ins_user,$banner_img,$banner_url'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('template_game',width='100%', name='-')
        r.cell('join_game',name="Join Game",calculated=True,width='6em',
                    cellClasses='cellbutton',
                    format_buttonclass='icon48 arrow_right iconbox',
                    format_isbutton=True,format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                                           genro.mainGenroWindow.genro.gotoURL('/tabletop/play/'+row['__ins_user']+'/'+row['code']);""")

        #r.fieldcell('weekday')
        #r.fieldcell('image')

    def th_order(self):
        return 'title'

    def th_condition(self):
        return dict(condition='$current_player_game IS TRUE')

    @metadata(variable_struct=False, isMain=True)
    def th_sections_gamestatus(self):

        l = [dict(code='all',caption='All'),
             dict(code='config', caption='Configurating', condition="$shared_data IS NULL"),
             dict(code='creation', caption='Game Creation', condition="$shared_data IS NOT NULL")]
        return l


    def th_top_bar_custom(self,top):
        bar = top.bar.replaceSlots('5,vtitle','20,sections@gamestatus')
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
        fb.field('ruleset',lbl='!!Ruleset',width='18em',validate_notnull=True)
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
        #form.dataController("""
        #                  console.log(shared_data, shared_data.len());
        #                  if(!shared_data || shared_data.len()==0){
        #                      SET #FORM.disable_game_edit = false;
        #                  }else{
        #                      SET #FORM.disable_game_edit = true;
        #                  }""", 
        #                  shared_data='=#FORM.record.shared_data',
        #                  loaded='^#FORM.controller.loaded')

        tc = form.center.tabContainer(datapath='.record',margin='2px')
        
        self.gameInfo(tc.borderContainer(title='Game'))
        
        self.configOptions(tc.borderContainer(region='center', title='Rules settings'))
        self.skillPreferences(tc.borderContainer(region='bottom',  datapath='#FORM', title='Skills', hidden='^#FORM.record.use_approaches'))
        form.dataRpc('#FORM.pcsheets',
                        self.db.table('fate.game').createNewPlayData,
                                 game_id='=#FORM.record.id',
                                 _onResult="genro.mainGenroWindow.genro.gotoURL('/tabletop/play/'+kwargs.user+'/'+kwargs.code);",
                                 _fired='^#FORM.createPlayData',
                                user='=#FORM.record.__ins_user',
                                 code='=#FORM.record.code')

    def gameInfo(self, bc):
        top = bc.contentPane(region='top', height='75px').div(margin='10px')
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
        note.simpleTextArea(value='^.description', editor=True)
        self.playersGrid(center.contentPane(region='right', width='280px', datapath='#FORM'))
        bc.roundedGroup(region='bottom',height='120px', title='Game Banner').img(src='^.banner_url', 
                        crop_width='690px',crop_height='80px',
                        upload_folder='site:img/game/banner',edit=True,
                        upload_filename='=#FORM.record.id',
                        placeholder=True,
                        crop_border='2px solid #ddd',
                        crop_rounded=8,crop_margin='5px',
                        crop_margin_left='10px',
                        zoomWindow=True)

    def playersGrid(self, pane):
        pane.inlineTableHandler(relation='@players',
            viewResource='ViewFromGame',
            searchOn=False,
            margin='2px',
            title='Players',
            pbl_classes=True,
            addrow=True,
            delrow=False)

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

        self.consequencesEditor(bc.contentPane(region='right', width='300px'))
        self.stressTracksEditor(bc.contentPane(region='bottom', height='150px'))
        fb =bc.roundedGroup(title='Options',region='center').div(margin='8px').formbuilder(cols=3,border_spacing='4px')
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
            r.cell('shifts', dtype='I', name='Shifts',width='4em', edit=dict(validate_notnull=True, validate_min=1))
            r.cell('label', name='Label', width='100%', edit=dict(validate_notnull=True))
            r.cell('skill', name='Skill', width='10em',
                    hidden='^#FORM.record.use_approaches',
                    edit=dict(tag='dbSelect', dbtable='fate.skill',exclude=True))
            r.cell('lv', dtype='I', name='at rate', width='4em', edit=True, hidden='^#FORM.record.use_approaches')
        
        pane.bagGrid(storepath='#FORM.record.consequences_slots',
            title='Consequences',pbl_classes=True,
            margin='2px',
            struct=struct,
            datapath='#FORM.consequences',
            grid_selfsubscribe_addrow="""genro.dlg.prompt('Consequence slot', {
                                                    lbl:'Code',
                                                     action:function(value){
                                                        genro.publish('newcons',{code:value})
                                                     }
                                                    });""")

        pane.dataController("""var b = new gnr.GnrBag();
                               b.setItem('code',code);
                               consequences.setItem(code,b);""", 
                            subscribe_newcons=True, 
                            consequences='=#FORM.record.consequences_slots')

    def skillPreferences(self, bc):
        top = bc.roundedGroup(title='Skill sets' ,height='80px', region='top')
        fb =top.formbuilder(cols=1,border_spacing='3px', datapath='#FORM.record')
        fb.field('skill_sets' ,width='100%', colspan=2, tag='checkBoxText', 
                   lbl='',
                   cols='3',
                   table='fate.skill_set')
        skillpane = bc.contentPane(region='center', datapath='#FORM')
        skillpane.dialogTableHandler(relation='@custom_skills',
             title='Custom skills',
             searchOn=False,
             configurable=False,
             addrow=True,
             delrow=True,
             pbl_classes=True,
             formResource ='FormFromGame',
             viewResource='ViewCustomFromGame')

    def stressTracksEditor(self, pane):
        def struct(struct):
            r = struct.view().rows()
            r.cell('track_name', name='Track', width='100%', edit=True)
            r.cell('n_boxes', dtype='I', name='Std. Boxes',width='6em', edit=True)
            #r.cell('max_boxes', dtype='I', name='Max',width='4em', edit=dict(validate_min='=.n_boxes'))
            r.cell('skill', name='Skill',
                width='7em',
                    hidden='^#FORM.record.use_approaches',
                    edit=dict(tag='dbSelect', dbtable='fate.skill',exclude=True))
            r.cell('extra_box_1', name='+1 at rate',
                width='7em',
                    hidden='^#FORM.record.use_approaches',
                    dtype='I',
                    edit=dict(tag='numbertextbox', validate_max=6, validate_min=1))
            r.cell('extra_box_2', name='+2 at rate',
                width='7em',
                    hidden='^#FORM.record.use_approaches',
                    dtype='I',
                    edit=dict(tag='numbertextbox', validate_max=6, validate_min='^.extra_box_1'))
            r.cell('extra_box_3', name='+3 at rate',
                width='7em',
                    hidden='^#FORM.record.use_approaches',
                    dtype='I',
                    edit=dict(tag='numbertextbox', validate_max=6, validate_min='^.extra_box_2'))


        pane.bagGrid(storepath='#FORM.record.stress_tracks',datapath='#FORM.stress',
            title='Stress tracks',pbl_classes=True,struct=struct,
                              grid_selfsubscribe_addrow="""genro.dlg.prompt('Add stress track', {
                                                    lbl:'Code',
                                                     action:function(value){
                                                        genro.publish('newtrack',{code:value})
                                                     }
                                                    });""")
        pane.dataController("""var b = new gnr.GnrBag();
                               b.setItem('code',code);
                               stress_tracks.setItem(code,b);""", 
                               subscribe_newtrack=True, stress_tracks='=.stress_tracks')

    def th_bottom_custom(self,bottom):
        bar = bottom.slotBar('*,back,confirm,2',margin_bottom='2px')
        bar.back.button('!!Cancel',action='this.form.abort();')
        box = bar.confirm.div()
        box.button('!!Save',
                    iconClass='fh_semaphore',
                    action='this.form.publish("save")')
        box.slotButton('!!Join Game',
                        action="""var that = this;
                                  console.log(shared_data);
                                  if(!shared_data || shared_data.len()==0){
                                      if(this.form.changed){
                                      console.log('SAVE and CREATE DATA');
                                              this.form.save({onReload:function(){
                                                  that.fireEvent('#FORM.createPlayData',true);
                                              }});
                                      }else{
                                      console.log('CREATE DATA');
                                              FIRE #FORM.createPlayData;
                                      }
                                  }else{
                                      console.log('OPEN PLAY WINDOW');
                                      genro.mainGenroWindow.genro.gotoURL('/tabletop/play/'+user+'/'+code);
                                  }
                                  """,
                                  shared_data='=#FORM.record.shared_data',
                                  user='=#FORM.record.__ins_user',
                                  code='=#FORM.record.code')
        #box.slotButton('!!Join Game',action="""genro.childBrowserTab('/tabletop/play/'+user+'/'+code);
        #                                                """,
        #                                                hidden='^#FORM.record.status?=#v=="CO"',
        #                                                user='=#FORM.record.__ins_user',
        #                                                code='=#FORM.record.code')

    def th_options(self):
        return dict(height='420px',width='740px',showtoolbar=False)
