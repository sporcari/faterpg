#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag


class PlayManager(BaseComponent):

    @struct_method
    def ft_playPage(self,parent,**kwargs):
        frame = parent.roundedGroupFrame(**kwargs)
        bar = frame.top.slotBar('5,ftitle,*',_class='pbl_roundedGroupLabel')
        bar.ftitle.div('^current_scene.metadata.title')
        bc = frame.center.borderContainer()
        top = bc.contentPane(region='top', height='30px', datapath='current_scene.metadata')
        top.div('^.description',_class='scene_desc')
        sc = bc.stackContainer(region='center')
        bc.dataController("status = status || 'no_action'; sc.switchPage((status=='no_action' || status=='action' || status=='waiting_active_player')?0:1)",sc=sc.js_widget,status='^current_scene.action_status')
        bc.dataController("""
            Fate.setAvailableCharacters(pcsheets,npcs,gm_id);
            """,npcs='^npcs',gm_id=self.game_record['gm_id'],pcsheets='=play_data.pcsheets',
            _delay=100)
        bc.dataController("""
            SET current_scene.current_action.phase = new gnr.GnrBag(_subscription_kwargs);
            """,subscribe_player_phase=True)
        dlg = self.act_character_dialog(bc)
        self.aspect_picker(bc)

        bc.dataController("""
            if(!pars.getItem('player_id')){
                return;
            }
            if(player_id==pars.getItem('player_id')){
                dlg.show();
            }
            """,pars='^current_scene.current_action.phase',_if='pars',player_id=self.rootenv['player_id'],
            dlg=dlg.js_widget)
        
        no_action = sc.borderContainer(region='center')
        self.currentSceneAspects(no_action.contentPane(region='left', width='50%'))
        self.npcsInScene(no_action.contentPane(region='center'))
        self.act_actionViewer(sc.borderContainer(datapath='.current_action'))


    def aspect_picker(self,pane):
        dlg = pane.dialog(title='Aspects',datapath='main.aspect_picker',
                            subscribe_aspect_picker="""SET .store = Fate.prepareAspectPickerData();this.widget.show();
                                                       SET .exit_mode = $1.reason;
                                                       SET .caller = $1.caller; 
                                                        """,
                            closable=True)
        frame = dlg.framePane(width='400px',height='450px')
        frame.center.contentPane(overflow='auto',padding='5px').tree(storepath='.store',hideValues=True,excludeRoot=True,
                         labelAttribute='caption',selectedLabelClass='selectedAspect',
                         connect_ondblclick="""function(e){
                            var wdg = dijit.getEnclosingWidget(e.target);
                            var item = wdg.item;
                            if(item.attr.phrase){
                                this.fireEvent('.invoked_aspect',item.attr.phrase);
                            }
                         }""")
        frame.dataController("""
            dlg.hide();
            if(exit_mode=='get_bonus'){
                Fate.writeActionStep(caller,new gnr.GnrBag({description:'Invoked '+invoked_aspect+' to increase modifiers',modifier:2}),{aspect:true});
            }else{
                Fate.writeActionStep(caller,new gnr.GnrBag({description:'Invoked aspect '+invoked_aspect +' to roll again' ,modifier:0}),{aspect:true});
                if(caller=='opposition'){
                    genro.setData('current_scene.current_action.opponent_player.rolled',false);
                }else{
                    genro.setData('current_scene.current_action.active_player.rolled',false);
                }
                
            }
            """,invoked_aspect='^.invoked_aspect',exit_mode='=.exit_mode',dlg=dlg.js_widget,caller='=.caller')


    def act_character_dialog(self,pane):
        dlg = pane.dialog(title='^.phase.name',datapath='current_scene.current_action',closable=True)
        frame = dlg.framePane(height='200px',width='320px')
        fb = frame.formbuilder(cols=1,border_spacing='3px',lbl_width='6em',datapath='.phase',margin='15px')
        fb.filteringSelect(value='^.action_type',
                            validate_onAccept="""SET .target_id=null;""",
                            hidden='^.action_type_hidden',disabled='^.action_type_disabled',
                          values=self.db.table('fate.action_type').actionTypes(),

                        cursor='pointer',lbl='Action')
        fb.callbackSelect(value='^.target_id',callback="""function(kw){
                return Fate.getAvailableCharacterSelector(kw);
            }""",lbl='Target',
            blacklist='=.character_id',
            selected_name='.target_name',
            selected_image_url='.target_image_url',
            hidden='^.action_type?=!(#v=="CA" || #v=="AT")',
            hasDownArrow=True)
        fb.callbackSelect(value='^.skill',callback="""function(kw){
                return Fate.skillSelectValues(kw);
            }""",auxColumns='skillname,level',
            selected_level='.modifier',
            action_type='=.action_type',
            character_skills='=.character_skills',
            lbl='Skill',hasDownArrow=True)
        fb.numberTextBox(value='^.modifier',lbl='Modifier')
        fb.simpleTextArea(value='^.details',lbl='Details')
        bar = frame.bottom.slotBar('*,confirm,2')
        bar.confirm.slotButton('Confirm',action="""Fate.actionPhaseConfirmed(data,status);
                                                  dlg.hide();""",
            dlg=dlg.js_widget,data='=.phase',status='=current_scene.action_status',
            character_id='=.character_id')
        return dlg


    def act_activeStruct(self,struct):
        r = struct.view().rows()
        r.cell('description',width='100%')
        r.cell('modifier',width='2em',dtype='I',totalize='current_scene.current_action.active_player.modifiers',
                cellClasses='modifier_cell')

    def act_opponentStruct(self,struct):
        r = struct.view().rows()
        r.cell('description',width='100%')
        r.cell('modifier',width='2em',dtype='I',totalize='current_scene.current_action.opponent_player.modifiers',
                cellClasses='modifier_cell')



    def act_actionViewer(self, bc):


        active = bc.borderContainer(region='left',_class='active_box',width='50%')
        opponent = bc.borderContainer(region='center',_class='opponent_box')

        bc.dataController("""
            genro.dom.setClass(opponent,'is_owner',opponent_player_id==player_id);
            """,opponent_player_id='^#opponent_player.player_id',
                player_id=self.rootenv['player_id'],opponent=opponent)
        bc.dataController("""
            genro.dom.setClass(active,'is_owner',active_player_id==player_id);
            """,active_player_id='^#active_player.player_id',player_id=self.rootenv['player_id'],
                active=active)

        frame = active.bagGrid(storepath='current_scene.current_action.active_steps',
                                addrow=False,pbl_classes='*',
                                struct=self.act_activeStruct,datapath='main.action_viewer_active',
                                margin='2px',region='center')
        
        bar = frame.top.bar.replaceSlots('#','2,avt,*,vtitle,*',_class='action_log_bar')
        bar.vtitle.div('^#active_player.name')
        bar.avt.div(padding='2px').img(src='^#active_player.image_url',height='60px')
        frame = opponent.bagGrid(storepath='current_scene.current_action.opposition_steps',addrow=False,delrow=False,pbl_classes='*',
                                struct=self.act_opponentStruct,margin='2px',region='center')
        
        bar = frame.top.bar.replaceSlots('#','*,vtitle,*,avt,2',_class='action_log_bar')
        bar.vtitle.div('^#opponent_player.name')
        bar.avt.img(src='^#opponent_player.image_url',height='60px',margin_top='2px')
        self.act_finalActive(active.roundedGroup(region='bottom',height='200px',datapath='current_scene.current_action.active_player',nodeId='active_player'))
        self.act_finalOpposition(opponent.roundedGroup(region='bottom',height='200px',datapath='current_scene.current_action.opponent_player',nodeId='opponent_player'))
        
        end_action = bc.contentPane(height='50px',border_top='1px solid silver',region='bottom')

        end_action.dataController("""
                            var delta = active_overall-opponent_overall;
                            var result;
                            SET current_scene.current_action.final_delta = delta;
                            if(delta<0){
                                result = 'Fail';
                            }else if(delta==0){
                                result = 'Tie';
                            }else if(delta>0 && delta<3){
                                result = 'Success';
                            }else{
                                result = 'Success with style'
                            }
                            SET current_scene.current_action.final_result = result;
                            """,
                        active_overall='^#active_player.overall',
                        active_rolled='^#active_player.rolled',
                        opponent_rolled='^#opponent_player.rolled',
                        active_rolling='^#active_player.rolling',
                        opponent_rolling='^#opponent_player.rolling',
                        opponent_overall='^#opponent_player.overall',
                        _if='(opponent_rolled&&active_rolled) && !(active_rolling || opponent_rolling)',
                        _else="""
                            SET current_scene.current_action.final_result = null;
                        """)

        end_action.div('^current_scene.current_action.final_result',font_size='22px',text_align='center',
                        color='#006AC2',margin='3px')
#
        bc.dataController("""opponent.setRegionVisible('bottom',action_status=='roll_dice');
                             active.setRegionVisible('bottom',action_status=='roll_dice');
                             mainbc.setRegionVisible('bottom',action_status=='roll_dice');""",
                        opponent = opponent.js_widget,
                        active = active.js_widget,
                        mainbc = bc.js_widget,
                        action_status='^current_scene.action_status')

    def act_finalActive(self,pane):
        tr = pane.table(width='100%').tbody().tr(_class='owner_only')
        tr.td('Invoke aspect',_class='rolled_value')
        tr.td().lightButton('+2',action="""
                        genro.publish('aspect_picker',{reason:'get_bonus',caller:caller});
                    """,_class='dice_button',caller='active')
        tr.td().lightButton('Re Roll',
                    action="""
                        genro.publish('aspect_picker',{reason:'re_roll',caller:caller});
                    """,
                        _class='dice_button',caller='active')
        self.roller(pane,'active')
        

 

    def act_finalOpposition(self,pane):
        tr = pane.table(width='100%').tbody().tr(_class='owner_only')
        tr.td('Invoke aspect',_class='rolled_value')
        tr.td().lightButton('+2',action="""
                        genro.publish('aspect_picker',{reason:'get_bonus',caller:caller});
                    """,_class='dice_button',caller='opposition')
        tr.td().lightButton('Re Roll',
                    action="""
                        genro.publish('aspect_picker',{reason:'re_roll',caller:caller});
                    """,_class='dice_button',caller='opposition',disabled='^.passive')
        self.roller(pane,'opponent')


    def roller(self,pane,mode=None,**kwargs):
        table = pane.table(width='100%').tbody()
        tr = table.tr()
        table.data('%s.timer' %mode,0)
        rollbtn = tr.td().div('Roll',connect_mousedown="FIRE %s.roll_run" %mode,
                      connect_mouseup="FIRE %s.roll_stop;" %mode,
                      connect_mouseout="""FIRE %s.roll_stop;""" %mode,
                      _class='dice_button dice_roller owner_only',
                      disabled='^.rolled')

        pane.dataController("""
                             SET %s.timer=0.01;
                             genro.dom.setClass(rollbtn,'dice_pressing',true)
                             """ %mode,
                             _fired='^%s.roll_run' %mode,rollbtn=rollbtn,
                             rolled='=.rolled',_if='!rolled')
        
        pane.dataController("""SET %s.timer=0;
                              genro.dom.setClass(rollbtn,'dice_pressing',false);
                              SET .rolled = true;
                             """ %mode,
                             _fired='^%s.roll_stop' %mode,rollbtn=rollbtn,timer='=%s.timer' %mode,
                             _if='timer')
        pane.dataController("""
            var tot = 0;
            var v;
            for (var i=0;i<4;i++){
                v = Math.floor(Math.random() *3)-1;
                this.setRelativeData('.dices.d_'+i,v);
                tot+=v;
            }
            SET .rolled_value = tot;
            var that = this;
            """,_timing='^%s.timer' %mode)
        box = tr.td()
        for k in range(4):
            box.div(innerHTML="""==Fate.diceContent(_dice_value);""",
                    _dice_value='^.dices.d_%s' %k,display='inline-block')
        tr.td().div('^.rolled_value',_class='rolled_value',width='22px',
                        text_align='right')
        tr = table.tr()
        tr.td(colspan=2).div('Result',_class='rolled_value',text_align='right')
        pane.dataFormula('.overall','(modifiers || 0)+(rolled_value || 0)',
                        rolled_value='^.rolled_value',modifiers='^.modifiers')
        tr.td().div('^.overall',_class='rolled_value',width='22px',
                        text_align='right')

    def currentSceneAspects(self, pane):
        frame = pane.templateGrid(title='Situation aspects',
                           frameCode='currentSceneAspects',
                           datapath='#FORM.current_scene_aspects',
                            _class='aspectGrid',
                           readOnly=not self.isGm,
                           storepath='current_scene.situation_aspects',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                                   dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])
        if self.isGm:
            r =frame.grid.struct.getItem('#0.#0')
            r.checkboxcell('hidden',width='2em')
        else:
            frame.grid.attributes.update(excludeListCb="""
                                   var result = [];
                                   this.store.getData().forEach(function(n){
                                           var v = n.getValue();
                                           if(v.getItem('hidden')){
                                               result.push(v.getItem('phrase'))
                                           }
                                   },'static');
                                   return result;
                                   """,
                                   excludeCol='phrase')
            frame.dataController("""if(_node.label=='hidden'){
                    grid.filterToRebuild(true);
                    grid.updateRowCount('*');
                }""",store='^current_scene.situation_aspects',grid=frame.grid.js_widget)

    def npcsInScene(self, pane):
        pane.templateGrid(title='Npcs in scene',
                           frameCode='currentSceneNpcs',
                           datapath='#FORM.current_scene_npcs',
                            _class='aspectGrid',
                            addrow=False,
                            delrow=False,
                           storepath='npcs',
                           template_resource='tpl/npcs_inscene')
                           #fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                           #        dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])



class GmTools(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_gmTools(self, parent, username=None, **kwargs):
        bc = parent.borderContainer(title='GM Tools', datapath='main.gm_tools')
        #top_pane.dataRpc('dummy', self.db.table('fate.game').savePlayData, 
        #                 _fired='^savePlayData',
        #                 game_id='=game_record.id',
        #                 play_data='=play_data')
        #top_pane.dataController("""SET play_data = game_play_data.deepCopy();""",
        #         game_play_data='=game_record.play_data', _fired='^loadPlayData')

        bc = bc.borderContainer(region='center')
        self.scenesMaker(bc.contentPane(region='top', height='150px'))
        self.npcMaker(bc.contentPane(region='center'))
        bottom = bc.framePane(region='bottom',height='150px')
        bar = bottom.top.slotBar("2,vtitle,*,reset,2",_class='pbl_roundedGroupLabel toolbar')
        bar.reset.button('Reset',action=""" SET current_scene.action_status = 'no_action';
                                            SET current_scene.current_action = new gnr.GnrBag();""")
        bar.vtitle.div('Action manager')
        sc = bottom.center.stackContainer(selectedPage='^current_scene.action_status',datapath='current_scene.current_action.data')
        no_action_pane = sc.contentPane(pageName='no_action')
        no_action_pane.button('New action',action="""Fate.loadAction();""")
        self.act_chooseCharacter(sc.contentPane(pageName='action'))
        sc.contentPane(pageName='waiting_active_player').div('Waiting active player',margin='20px',color='#217B1F',font_size='20px',text_align='center')
        self.act_chooseOpposition(sc.contentPane(pageName='opposition'))
        sc.contentPane(pageName='waiting_opposition').div('Waiting opposition player',margin='20px',color='#C22531',font_size='20px',text_align='center')
        sc.contentPane(pageName='roll_dice').button('Close action',
                                                    action="""
                                                        if(!action_log){
                                                            action_log = new gnr.GnrBag();
                                                            SET current_scene.action_log = action_log
                                                        }
                                                        action_log.setItem('r_'+action_log.len(),current_action);
                                                        SET current_scene.current_action = new gnr.GnrBag();
                                                        SET current_scene.action_status = 'no_action';
                                                    """,
                                                current_action='=current_scene.current_action',
                                                action_log='=current_scene.action_log')


    def act_chooseOpposition(self,pane):
        fb = pane.formbuilder(cols=3,border_spacing='3px')
        #fb.div('^.description')
        fb.button('^.target_name?=#v + " defends"',
                action="""var kw = Fate.characterPars(target_id);
                          kw['action_type'] = 'DF';
                          kw['action_type_disabled'] = true;
                          genro.setData('current_scene.action_status','waiting_opposition');
                          genro.publish('player_phase',kw);""",
                target_id='=.target_id',
                hidden='^.target_id?=!#v')
        fb.br()
        
        fb.callbackSelect(value='^.opponent_id',callback="""function(kw){
                return Fate.getAvailableCharacterSelector(kw);
            }""",lbl='Opponent',
            hasDownArrow=True,
            blacklist='=.opponent_blacklist')
        fb.button('Confirm',action="""var kw = Fate.characterPars(opponent_id);
                          kw['action_type'] = null;
                          kw['action_type_hidden'] = true;
                          genro.setData('current_scene.action_status','waiting_opposition');
                          genro.publish('player_phase',kw);""",
                opponent_id='=.opponent_id')
        fb.br()
        fb.textbox(value='^.passive_opposition',lbl='Opposition reason')
        fb.numberTextBox(value='^.passive_modifier',lbl='Modifier',width='5em')
        fb.button('Confirm',action="Fate.actionPhaseConfirmed(new gnr.GnrBag({modifier:passive_modifier,passive_opposition:passive_opposition || 'Obstacle',passive:true}),'waiting_opposition','Opposition $passive_opposition');",
                    passive_opposition='=.passive_opposition',
                    passive_modifier='=.passive_modifier')


    def act_chooseCharacter(self,pane):
        fb = pane.formbuilder(cols=2,border_spacing='3px')
        fb.callbackSelect(value='^.character_id',callback="""function(kw){
                return Fate.getAvailableCharacterSelector(kw);
            }""",lbl='Choose character',hasDownArrow=True,selected_name='.character_name',
                )
        fb.button('Confirm',action="""var kw = Fate.characterPars(character_id);
                                      genro.setData('current_scene.action_status','waiting_active_player');
                                      genro.publish('player_phase',kw);""",
                        character_id='=.character_id')

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
                                configurable=False,pbl_classes=True)
    def npcMaker(self, pane):
        pane.dialogTableHandler(table='fate.npc',
                                view_store_onStart=True,
                                condition='$game_id=:game_id',
                                condition_game_id ='=game_record.id',
                                default_game_id= '=game_record.id',
                                viewResource='ViewFromGmTools',
                                margin='2px',
                                searchOn=False,
                                #title='NPCs:',
                                addrow=True,
                                datapath='.npcs',
                                formResource='Form',
                                configurable=False,pbl_classes=True)
                                #pbl_classes=True)


class CharacterSheet(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_characterSheet(self, parent, username=None, **kwargs):
        parent.data('.%s.title' %username,username.capitalize())
        bc = parent.contentPane(title='^.%s.title' %username, username=username, **kwargs).borderContainer()
        

        top = bc.borderContainer(region='top',height='212px')
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
        r.td(colspan=2).textbox(value='^.name',lbl='Name',width='175px',border='0px', disabled=not (username==self.user))
        box = r.td(rowspan=3).div(height='172px',width='104px',border='1px solid #444',padding='2px')
        box.img(src='^.image_url',height='100%',width='100%',
                            placeholder=self.getResourceUri('css/images/social.svg'),
                             upload_folder='site:img/%s/pg' %self.game_record['id'],
                             upload_filename=username,edit=True)
        t.tr().td(colspan=2).simpleTextArea(value='^.description',lbl='Description', 
                            height='70px', width='175px',border=0, disabled=not (username==self.user))
        r = t.tr()
        r.td().numberTextBox(value='^.refresh', lbl='Refresh',
            font_size='2em',border=0, wrp_height='45px',width='60px', disabled=not (username==self.user))
        r.td().numberTextBox(value='^.fate_points',lbl='Fate points',
            font_size='2em',border=0, wrp_height='45px',width='60px', disabled=not (username==self.user))

    
    def characterAspects(self, bc, username):
        bc.templateGrid(region='center',frameCode='%s_aspects' %username,
                           title='Aspects',
                           readOnly= not (username == self.user),
                           addrow=False,
                           delrow=False,
                           datapath='.%s.aspects' %username,
                           _class='aspectGrid',
                           storepath='play_data.pcsheets.%s.aspects'% username,
                           template_resource='tpl/aspect_CA',
                           contentCb='Fate.characterAspectsForm(pane, kw)')

    def characterSkills(self, bc, username):
        frame = bc.roundedGroupFrame(title='Skills',region='top', height='120px', datapath='play_data.pcsheets.%s' %username)
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
                           readOnly= not (username == self.user),
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
                width='800px',height='300px',
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
        bar = th.view.bottom.slotBar('*,done,2',_class='slotbar_dialog_footer')
        bar.done.slotButton('!!Done',action="dlg.hide();",dlg=dlg.js_widget)
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

    