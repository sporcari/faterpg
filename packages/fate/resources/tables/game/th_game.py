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
        return '$code,$title,$description,$setting_tags,$ruleset'

    def th_struct(self,struct):

        r = struct.view().rows()
        r.fieldcell('template_game',width='100%')
        r.cell('apri_tab',name="Apri",calculated=True,width='3em',
                    cellClasses='cellbutton',
                    format_buttonclass='icon48 arrow_right iconbox',
                    format_isbutton=True,format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                                           var user = genro.getData('gnr.avatar.user');
                                                           genro.childBrowserTab('/tabletop/play/'+user+'/'+row['code']);""")

        #r.fieldcell('weekday')
        #r.fieldcell('image')

    def th_order(self):
        return 'title'

    def th_condition(self):
        return dict(condition='$current_player_game IS TRUE')

class FormNewGame(BaseComponent):
    def th_form(self, form):
        fb = form.record.formbuilder(cols=1,border_spacing='3px')
        fb.field('title')
        fb.field('code', validate_regex='![^A-Za-z0-9_]', width='4em',
                validate_regex_error='!!Invalid code: "." char is not allowed')
        fb.field('ruleset')

    def th_options(self):
        return dict(dialog_parentRatio=.5,modal=True)

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        top = bc.borderContainer(region='top', height='160px')
        base_info = top.roundedGroup(region='left', width='50%', title='Game info').div(margin_right='10px')
        fb = base_info.formbuilder(cols=2, border_spacing='4px', width='100%', fld_width='100%')
        fb.field('title', colspan=2)
        fb.field('code', validate_regex='![^A-Za-z0-9_]', 
                validate_regex_error='!!Invalid code: "." char is not allowed')
        fb.field('ruleset')
        fb.dataController("""var stBag = new gnr.GnrBag();
                             if (ruleset=='CORE'){
                                stBag.setItem('p.track_name','Phisical');
                                stBag.setItem('p.n_boxes',2);
                                stBag.setItem('m.track_name','Mental');
                                stBag.setItem('m.n_boxes',2);
                                stBag.setItem('m.skill_id',2);
                                SET .use_approaches=false;
                             }
                             if (ruleset=='FAE'){
                                stBag.setItem('s.track_name','Stress');
                                stBag.setItem('s.n_boxes',3);
                                SET .use_approaches=true;
                                SET .stunt_sets='';
                             }
                             SET .stress_tracks = stBag;""",
                             ruleset='^.ruleset', _userChanges=True)

        fb.field('setting_tags', tag='checkBoxText', 
                  cols=2,
                   popup=True, 
                   colspan=2, 
                   table='fate.setting')
        fb.field('description', tag='simpleTextArea', colspan=2, height='8ex')
        self.playersGrid(top.contentPane(region='center', datapath='#FORM'))
        center = bc.borderContainer(region='center')
        self.configOptions(center.roundedGroupFrame(region='bottom', height='160px', title='Game configuration'))
        self.imagePane(center.roundedGroup(title="Game's banner", region='center'))
        self.skillPreferences(bc.borderContainer(region='bottom', height='200px',  hidden='^.use_approaches'))

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
        fb.field('use_approaches', lbl='', label='Use approaches', disabled="==(ruleset=='FAE')", ruleset='^.ruleset')
        fb.field('use_phases', lbl='',label='Phases PC creation')
        fb.dataController("SET .stunt_sets=''; SET .skill_sets=''; SET approach_set=FAE;",
                          use_approaches='^.use_approaches', _if='use_approaches')
        

        fb.button('Create Characters', action='FIRE #FORM.createCharacters')
        fb.dataRpc('dummy', self.db.table('fate.game').createCharacterSheets, game_id='=#FORM.pkey', _fired='^#FORM.createCharacters' )
       
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



    def th_options(self):
        return dict(dialog_height='660px', dialog_width='880px')


class FormNewGame(Form):
    def th_form(self, form):
        fb = form.record.formbuilder(cols=1,border_spacing='3px')
        fb.field('title')
        fb.field('code', validate_regex='![^A-Za-z0-9_]', width='4em',
                validate_regex_error='!!Invalid code: "." char is not allowed')
        fb.field('ruleset')

    def th_options(self):
        return dict(dialog_parentRatio=.5,modal=True)
