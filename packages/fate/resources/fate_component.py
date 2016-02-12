#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method
from gnr.core.gnrbag import Bag

class AspectGrid(BaseComponent):
    py_requires='gnrcomponents/framegrid:FrameGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_aspectGrid(self, pane, frameCode=None, 
                     title=None, datapath=None,
                     aspect_type=None,
                     storepath=None,
                     **kwargs):
        frame = pane.bagGrid(frameCode=frameCode , 
                            title=title,
                            _class='aspectGrid grid_%s' %(aspect_type or 'BASE'),
                            pbl_classes='*',
                            datapath='.%s'%frameCode, 
                            struct=self.ft_aspectStruct,
                            storepath=storepath, **kwargs)
        form = frame.grid.linkedForm(datapath='.form', _class='aspectForm',
                              frameCode='%s_form' % frameCode,
                              dialog_height='280px',
                              store='memory',
                              loadEvent='onRowDblClick',
                              dialog_title=title,
                              dialog_width='370px',
                              default_aspect_type=aspect_type)
        getattr(self,'ft_aspectForm_%s' %aspect_type,self.ft_aspectForm_base)(form)
        bar = form.bottom.slotBar('*,cancel,confirm,2',_class='slotbar_dialog_footer')
        bar.cancel.slotButton('!!Cancel',action='this.form.abort()')
        bar.confirm.slotButton('!!Confirm',action='this.form.save({destPkey:"*dismiss*"})')
        return frame


    def ft_aspectForm_base(self,form):
        #bc = form.center.borderContainer()

        fb = form.record.formbuilder(cols=1, fld_width='220px',lblpos='T')
        fb.textbox(value='^.phrase', lbl='Phrase')
        fb.simpleTextArea(value='^.description', lbl='Description', height='170px')
        
    def tf_aspectForm_SKILLS(self, form):
        pass

    def ft_aspectForm_FACES(self,form):
        self._ft_aspectForm_FACES_PLACES(form)

    def ft_aspectForm_PLACES(self,form):
        self._ft_aspectForm_FACES_PLACES(form)

    def _ft_aspectForm_FACES_PLACES(self,form):
        fb = form.record.formbuilder(cols=1)
        fb.textbox(value='^.name', lbl='Name')
        fb.simpleTextArea(value='^.description', lbl='Description', height='170px')

    def ft_aspectForm_STUNT(self,form):
        fb = form.record.formbuilder(cols=1)
        fb.textbox(value='^.name', lbl='Name')
        fb.textbox(value='^.description', lbl='Description')

    def ft_aspectForm_CA(self,form):
        box = form.record.div(wrp_width='100%', wrp_display='block',wrp_margin='2px')
        box.div('==Fate.getPreviousBackstory(this, _phase)', _phase='^.phase',_class='prev_backstory')
        box.simpleTextArea('^.backstory', lbl='Backstory', height='90px', 
                                wrp_hidden='^.aspect_type?=#v!="PH"')
        box.textbox('^.phrase', lbl='Phrase',width='100%')


    def ft_aspectStruct(self,struct):
        r = struct.view().rows()
        r.cell('aspect', _customGetter='function(row){return Fate.renderAspectRow(row);}',
                width='100%')

class CharacterSheet(BaseComponent):
    py_requires='gnrcomponents/framegrid:FrameGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_characterSheet(self, parent, username=None, **kwargs):
        parent.data('.%s.title' %username,username)
        bc = parent.contentPane(title='^.%s.title' %username, username=username, **kwargs).borderContainer()
        top = bc.borderContainer(region='top',height='250px')
        center = bc.borderContainer(region='center')
        bottom = bc.borderContainer(region='bottom', height='150px')
        self.idGroup(top, username=username)
        self.characterAspects(top, username=username)
        self.characterSkills(center, username=username)
        self.characterStunts(center,username=username)
        self.stressTracks(bottom.contentPane(region='left', width='50%',
                                             datapath='game.pcsheets.%s.stress_tracks'% username))
        self.consequences(bottom.contentPane(region='center'))
        #defaultbag =Bag()
        #center.dataFormula()

    def idGroup(self, bc, username):
        box = bc.roundedGroup(title='ID',region='left',width='50%', 
                             datapath='game.pcsheets.%s'%username,
                             wrp_border='1px solid #444',
                             lbl_background='transparent',
                             #wrp_margin='2px',
                             wrp_display='block',
                             lbl_color='#444',lbl_border=0,
                             overflow='hidden')
        t = box.table(border_spacing='2px').tbody()
        r = t.tr()
        r.td(colspan=2).textbox(value='^.name',lbl='Name',width='160px',border='0px')
        r.td(rowspan=3).div(lbl='Portrait', height='180px', wrp_width='100px')
        t.tr().td(colspan=2).simpleTextArea(value='^.description',lbl='Description', 
                            height='70px', width='160px',border=0)
        r = t.tr()
        r.td().numberTextBox(value='^.refresh', lbl='Refresh',
            font_size='2em',border=0, wrp_height='60px',width='60px')
        r.td().numberTextBox(value='^.fate_points',lbl='Fate points',
            font_size='2em',border=0, wrp_height='60px',width='60px')

    def characterAspects(self, bc, username):
        bc.aspectGrid(region='center',frameCode='%s_aspects' %username,
                           title='Aspects',
                           aspect_type='CA',
                           addrow=False,
                           delrow=False,
                           storepath='game.pcsheets.%s.aspects'% username)

    def characterSkills(self, bc, username):
        pane = bc.roundedGroup(title='Skills',region='top', height='130px', datapath='game.pcsheets.%s' %username)
        if self.user == username:
            pane.lightButton('==Fate.renderSkillsPyramid(_skills, _skill_cap)',
                                _skills='^.skills',
                                _skill_cap = '=game_record.skill_cap',
                                height='80px',
                                action='PUBLISH openSkillsPicker = {username:username}',
                                username=username)
        else:
            pane.div('==Fate.renderSkillsPyramid(_skills, _skill_cap)',
                                _skills='^.skills',
                                 _skill_cap = '=game_record.skill_cap',
                                height='80px')

    def characterStunts(self, bc, username):
        frame = bc.aspectGrid(region='center',frameCode='%s_stunts' %username,
                           title='Stunts',
                           aspect_type='STUNT',
                           addrow=False,
                           delrow=False,
                           storepath='game.pcsheets.%s.stunts'% username)
        
        if self.user==username:
            bar = frame.top.bar.replaceSlots('#','#,stuntsPicker,addStunt,2')
            bar.stuntsPicker.palettePicker(grid=frame.grid,
                width='600px',height='350px',
                table='fate.stunt',
                viewResource='ViewPicker_skill',
                checkbox=True,
                autoInsert="genro.bp(true); Fate.copyStunts(grid,data)")


    def stressTracks(self, pane):
        for v in self.game_record['stress_tracks'].values():
            st = pane.div(lbl=v['track_name'], wrp_width='100%',wrp_display='block',
                     height='30px', border='1px solid black', datapath='.%s' % v['code'])
            for n in range(v['max_boxes']):
                n=n+1
                st.checkbox(value='^.boxes.b%s'%str(n), wrp_margin='2px', 
                             wrp_display='inline block', wrp_width='30px',
                             lbl=str(n), 
                             disabled='==%s>n_boxes' % str(n), 
                             n_boxes='^.n_boxes')
            #st.numberTextBox(value='^.n_boxes')



    def consequences(self, pane):
        for i in range(4):
            pane.div(lbl='', wrp_width='100%',wrp_display='block', height='30px', border='1px solid black')
            

    def getGameSkills(self):
        return Bag(self.db.table('fate.skill').query(columns="""$name,$description,$code,
                                                     $skill_set,$action_types,
                                                     $stresstrack_changes""",
                                                     bagField=True).fetchAsDict(key='code'))



    @struct_method
    def ft_skillsPicker(self, pane):
        dlg = pane.dialog(title='Choose skills',
                          closable=True,
                          datapath='main.pickers.skills_picker',
                          subscribe_openSkillsPicker="""this.widget.show();
                                                         """)
        pickerStorePath = 'game.pcsheets.%s.skills'% self.user
        th = dlg.plainTableHandler(table='fate.skill',
            height='470px', width='290px',
            nodeId='skillsPickerGrid',
                        condition='$skill_set IN :sets OR $game_id= :game_id',
                        condition_sets='^game_record.skill_sets?=#v?#v.split(","):[]',
                        condition_game_id='=game_record.game_id',
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
