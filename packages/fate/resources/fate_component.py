#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method
from gnr.core.gnrbag import Bag


class PlayManager(BaseComponent):

    @struct_method
    def ft_playPage(self,parent,**kwargs):
        bc = parent.borderContainer( **kwargs)
        top = bc.contentPane(region='top', height='50px', datapath='current_scene.metadata')
        top.div('^.title')
        top.div('^.description')
        center = bc.borderContainer(region='center')
        self.currentSceneAspects(center.contentPane(region='left', width='50%'))
        self.npcsInScene(center.contentPane(region='center'))

    def currentSceneAspects(self, pane):
        pane.templateGrid(title='Situation aspects',
                           frameCode='currentSceneAspects',
                           datapath='#FORM.current_scene_aspects',
                            _class='aspectGrid',
                            addrow=True,
                            delrow=True,
                           storepath='current_scene.situation_aspects',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                                   dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])
    def npcsInScene(self, pane):
        pane.div('aaa')
        #pane.templateGrid(title='Npcs in scene',
        #                   frameCode='currentSceneAspects',
        #                   datapath='#FORM.current_scene_aspects',
        #                    _class='aspectGrid',
        #                    addrow=True,
        #                    delrow=True,
        #                   storepath='current_scene.situation_aspects',
        #                   template_resource='tpl/game_issues',
        #                   fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
        #                           dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])



class GmTools(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_gmTools(self, parent, username=None, **kwargs):
        bc = parent.borderContainer(title='GM Tools', datapath='main.gm_tools')
        top_pane = bc.contentPane(region='top', height='80px')
        top_pane.button('SAVE', action="genro.som.saveSharedObject(shared_id);", shared_id=self.game_shared_id)
        top_pane.button('LOAD PLAY DATA', action="genro.som.loadSharedObject(shared_id);", shared_id=self.game_shared_id)
        top_pane.dbSelect(value='^main.current_scene_id', dbtable='fate.scene', rowcaption='$title')
        #top_pane.dataRpc('dummy', self.db.table('fate.game').savePlayData, 
        #                 _fired='^savePlayData',
        #                 game_id='=game_record.id',
        #                 play_data='=play_data')
        #top_pane.dataController("""SET play_data = game_play_data.deepCopy();""",
        #         game_play_data='=game_record.play_data', _fired='^loadPlayData')

        tc = bc.tabContainer(region='center')
        self.scenesMaker(tc.contentPane(region='center', title='Scenes'))
        self.npcMaker(tc.contentPane(region='center', title='NPCs'))
        #pane.button('Start game')
        #pane.button('New scene')
        



    @struct_method
    def ft_npcPage(self, parent, **kwargs):
        parent.contentPane(title='NPCs')

    def scenesMaker(self, pane):
        pane.dialogTableHandler(table='fate.scene',
                                view_store_onStart=True,
                                condition='$game_id=:game_id',
                                condition_game_id ='=game_record.id',
                                default_game_id= '=game_record.id',
                                viewResource='ViewFromGmTools',
                                margin='2px',
                                searchOn=False,
                                datapath='.scenes',
                                formResource='Form',
                                configurable=False)
    def npcMaker(self, pane):
        f = self.db.table('fate.npc_type').query().fetch()
        addrowDict=[(r['name'],dict(npc_type=r['code'])) for r in f]

        pane.dialogTableHandler(table='fate.npc',
                                view_store_onStart=True,
                                condition='$game_id=:game_id',
                                condition_game_id ='=game_record.id',
                                default_game_id= '=game_record.id',
                                viewResource='ViewFromGmTools',
                                margin='2px',
                                searchOn=False,
                                #title='NPCs:',
                                addrow=addrowDict,
                                datapath='.npcs',
                                formResource='Form',
                                configurable=False)
                                #pbl_classes=True)

class CharacterSheet(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_characterSheet(self, parent, username=None, **kwargs):
        parent.data('.%s.title' %username,username)
        bc = parent.contentPane(title='^.%s.title' %username, username=username, **kwargs).borderContainer()
        

        top = bc.borderContainer(region='top',height='225px')
        center = bc.borderContainer(region='center')
        bottom = bc.borderContainer(region='bottom', height='120px')
        self.idGroup(top,username=username)

        self.characterAspects(top, username=username)
        self.characterSkills(center, username=username)
        self.characterStunts(center,username=username)
        self.stressTracks(bottom.roundedGroup(region='left', width='310px',title='Stress Tracks',
                                             datapath='play_data.pcsheets.%s.stress_tracks'% username))
        self.consequences(bottom.roundedGroup(region='center', title='Consequences',
                                              datapath='play_data.pcsheets.%s.consequences'% username))
        

        #defaultbag =Bag()
        #center.dataFormula()

    def idGroup(self, bc, username):
        box = bc.roundedGroup(title='ID',region='left',width='310px', 
                             datapath='play_data.pcsheets.%s'%username,
                             wrp_border='1px solid #444',
                             lbl_background='transparent',
                             #wrp_margin='2px',
                             wrp_display='block',
                             lbl_color='#444',lbl_border=0,
                             overflow='hidden')
        t = box.table(border_spacing='2px').tbody()
        r = t.tr()
        r.td(colspan=2).textbox(value='^.name',lbl='Name',width='175px',border='0px')
        r.td(rowspan=3).div(lbl='Portrait', height='161px', wrp_width='110px')
        t.tr().td(colspan=2).simpleTextArea(value='^.description',lbl='Description', 
                            height='70px', width='175px',border=0)
        r = t.tr()
        r.td().numberTextBox(value='^.refresh', lbl='Refresh',
            font_size='2em',border=0, wrp_height='45px',width='60px')
        r.td().numberTextBox(value='^.fate_points',lbl='Fate points',
            font_size='2em',border=0, wrp_height='45px',width='60px')

    def idGroup_z(self, bc, username):
        box = bc.roundedGroup(title='ID',region='left',width='282px', 
                             datapath='play_data.pcsheets.%s'%username,
                             wrp_border='1px solid #444',
                             lbl_background='transparent',
                             #wrp_margin='2px',
                             wrp_display='block',
                             lbl_color='#444',lbl_border=0,
                             overflow='hidden')
        t = box.table(border_spacing='2px',width='100%').tbody()
        t.tr().td(colspan=3).textbox(value='^.name',lbl='Name',#width='160px',
                            border='0px')
        r = t.tr()
        r.td(colspan=2).simpleTextArea(value='^.description',lbl='Description', 
                            height='55px', #width='160px',
                            border=0)
        r.td(rowspan=2).div(lbl='Portrait', height='130px', wrp_width='100px')

        r = t.tr()
        r.td().numberTextBox(value='^.refresh', lbl='Refresh',
            font_size='2em',border=0, wrp_height='45px',width='60px')
        r.td().numberTextBox(value='^.fate_points',lbl='Fate points',
            font_size='2em',border=0, wrp_height='45px',width='60px')

    def characterAspects(self, bc, username):
        bc.templateGrid(region='center',frameCode='%s_aspects' %username,
                           title='Aspects',
                           addrow=False,
                           delrow=False,
                           datapath='.%s.aspects' %username,
                           _class='aspectGrid',
                           storepath='play_data.pcsheets.%s.aspects'% username,
                           template_resource='tpl/aspect_CA',
                           contentCb='Fate.characterAspectsForm(pane, kw)')

    def characterSkills(self, bc, username):
        frame = bc.roundedGroupFrame(title='Skills',region='top', height='140px', datapath='play_data.pcsheets.%s' %username)
        if self.user == username:
            bar = frame.top.bar.replaceSlots('#','#,skillsButton,2')
            bar.skillsButton.slotButton('View Skills',
                                iconClass='iconbox app',
                                action='PUBLISH openSkillsPicker = {username:username}',
                                username=username)
        
        frame.div('==Fate.renderSkillsPyramid(_skills, _skill_cap)',
                                _skills='^.skills',
                                 _skill_cap = '=game_record.skill_cap',
                                height='80px')
        frame.dataController("Fate.onSkillsUpdate(this, skills,game_record);", 
                            skills='^.skills',_if='skills',
                            game_record='=game_record')

    def characterStunts(self, bc, username):
        frame = bc.templateGrid(region='center',frameCode='%s_stunts' %username,
                           title='Stunts',
                           _class='aspectGrid',
                           datapath='.%s.stunts' %username,
                           storepath='play_data.pcsheets.%s.stunts'% username,
                           template_resource='tpl/stunt',
                           contentCb='Fate.stuntsForm(pane, kw)')
        
        frame.dataController("""var n_stunts = stuntsBag.len();
                                var n_max_stunts = initial_stunts+refresh-1;
                                var extra_stunts = n_stunts-initial_stunts;
                                SET .max_stunts= (n_stunts==n_max_stunts);
                                SET .refresh = refresh-Math.max(extra_stunts,0);
                                """, 
                            stuntsBag='^.stunts',
                            initial_stunts='=game_record.initial_stunts',
                            refresh='=game_record.refresh',
                            datapath='play_data.pcsheets.%s' % username,
                            _if='stuntsBag')
        
        if self.user==username:
            bar = frame.top.bar.replaceSlots('#','#,stuntsPicker')
            #, addrow_disabled='^play_data.pcsheets.%s.max_stunts' % username)
            bar.stuntsPicker.palettePicker(grid=frame.grid,
                width='600px',height='350px',
                table='fate.stunt',
                viewResource='ViewPicker_skill',
                checkbox=True,
                autoInsert=True,
                relation_field='name',
                defaults='name,description')

    def stressTracks(self, pane):
        for v in self.game_record['stress_tracks'].values():
            st = pane.div(margin_right='10px').formbuilder(datapath='.%s' % v['code'],margin='2px',border_spacing='2px',width='100%',colswidth='auto',lblvalign='middle')
            box = st.div(lbl=v['track_name'],
                         padding='1px',
                        width='100%',
                        lbl_width='5em',
                        lbl_font_size='10pt')
            n_boxes = v['n_boxes']
            max_boxes = n_boxes
            if v['skill']:
                if v['extra_box_1']:
                    max_boxes = n_boxes+1
                if v['extra_box_2']:
                    max_boxes = n_boxes+2
                if v['extra_box_3']:
                    max_boxes = n_boxes+3

            for n in range(max_boxes):
                n=n+1
                box.lightButton(str(n),
                    #_class='==Fate.switchStressBox(current)',
                    _class='stressbox',
                    hidden='==%s>n_boxes' % str(n),
                    n_boxes='^.n_boxes',
                    action="""console.log(current);
                              current = !current;
                              console.log(current);
                              SET .boxes.b%i = current;
                              genro.dom.setClass(this,'stressbox_marked',current)
                              """% n, 
                    current='=.boxes.b%i' % n)

    def consequences(self, pane):
        st = pane.div(margin_right='10px').formbuilder(border_spacing='1px',width='100%',colswidth='auto',lblvalign='middle', fld_width='80%')
        cs = self.game_record['consequences_slots']
        for c in cs.values():
            st.textbox(value='^.%s.phrase' % c['code'],
                       lbl='%s (%i)' % (c['label'],c['shifts']),
                       hidden='^.%s.is_hidden'% c['code'])     

    def getGameSkills(self):
        game_id = self.game_record['id']
        return Bag(self.db.table('fate.skill').query(columns="""$name,$description,$code,
                                                     $skill_set,$action_types,
                                                     $stresstrack_changes""",
                                                     where='$game_id IS NULL or $game_id=:game_id',
                                                     game_id=game_id,
                                                     bagField=True).fetchAsDict(key='code'))

    @struct_method
    def ft_skillsPicker(self, pane):
        dlg = pane.dialog(title='Choose skills',
                          closable=True,
                          datapath='main.pickers.skills_picker',
                          subscribe_openSkillsPicker="""this.widget.show();
                                                         """)
        pickerStorePath = 'play_data.pcsheets.%s.skills'% self.user
        th = dlg.plainTableHandler(table='fate.skill',
            height='490px', width='290px',
            nodeId='skillsPickerGrid',
                        condition='$skill_set IN :sets OR $game_id= :game_id',
                        condition_sets='^game_record.skill_sets?=#v?#v.split(","):[]',
                        condition_game_id='=game_record.id',
                        configurable=False,
                        viewResource='ViewPicker',
                        view_store_onStart=True,
                        view_grid_userSets=pickerStorePath)

        dlg.dataController("""for (var i=1; i<=skill_cap;i++){
                                grid.addNewSetColumn({field:'lv'+i, 
                                                      name:i, 
                                                      skillmax:skill_cap-i+1,
                                                      position:'>',
                                                      _customGetter:function(rowdata,rowIdx){return Fate.skillsSetGetter(this,rowdata,rowIdx)}
                                                      })
                                }
                                """, grid=th.view.grid.js_widget,
                               skill_cap = '=game_record.skill_cap', 
                               _onStart=True)
