#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method
from gnr.core.gnrbag import Bag

class GmTools(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'
    css_requires='fate'

    @struct_method
    def ft_gmTools(self, parent, username=None, **kwargs):
        parent.contentPane(title='GM Tools')

    @struct_method
    def ft_npcPage(self, parent, **kwargs):
        parent.contentPane(title='NPCs')



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
                                             datapath='game.pcsheets.%s.stress_tracks'% username))
        self.consequences(bottom.roundedGroup(region='center', title='Consequences',
                                              datapath='game.pcsheets.%s.consequences'% username))
        

        #defaultbag =Bag()
        #center.dataFormula()

    def idGroup(self, bc, username):
        box = bc.roundedGroup(title='ID',region='left',width='310px', 
                             datapath='game.pcsheets.%s'%username,
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
                             datapath='game.pcsheets.%s'%username,
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
                           _class='aspectGrid',
                           storepath='game.pcsheets.%s.aspects'% username,
                           template_resource='tpl/aspect_CA',
                           contentCb='Fate.characterAspectsForm(pane, kw)')

    def characterSkills(self, bc, username):
        pane = bc.roundedGroup(title='Skills',region='top', height='140px', datapath='game.pcsheets.%s' %username)
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
        #pane.dataController("Fate.skillsForStress(skills,stress_tracks,consequences,game_record);", 
        #                    skills='^.skills',_if='skills',
        #                    stress_tracks='=.stress_tracks',
        #                    consequences='=.consequences',
        #                    game_record='=game_record')

    def characterStunts(self, bc, username):
        frame = bc.templateGrid(region='center',frameCode='%s_stunts' %username,
                           title='Stunts',
                           _class='aspectGrid',
                           storepath='game.pcsheets.%s.stunts'% username,
                           template_resource='tpl/stunt',
                           contentCb='Fate.stuntsForm(pane, kw)')
                           #fields=[dict(value='^.name', wdg='textbox', lbl='Name', width='15em'),
                           #        dict(value='^.description', wdg='simpleTextArea', lbl='Description', width='30em', height='40px')])
#
        frame.dataController("""var n_stunts = stuntsBag.len();
                                var n_max_stunts = initial_stunts+refresh-1;
                                var extra_stunts = n_stunts-initial_stunts;
                                SET .max_stunts= (n_stunts==n_max_stunts);
                                SET .refresh = refresh-Math.max(extra_stunts,0);
                                """, 
                            stuntsBag='^.stunts',
                            initial_stunts='=game_record.initial_stunts',
                            refresh='=game_record.refresh',
                            datapath='game.pcsheets.%s' % username,
                            _if='stuntsBag')
        if self.user==username:
            bar = frame.top.bar.replaceSlots('#','#,stuntsPicker')#, addrow_disabled='^game.pcsheets.%s.max_stunts' % username)
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
                         padding='2px',
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
        st = pane.div(margin_right='10px').formbuilder(border_spacing='2px',width='100%',colswidth='auto',lblvalign='middle')
        cs = self.game_record['consequences_slots']
        for c in cs:
            c = c.getAttr()
            st.textbox(value='^.%s.phrase' % c['code'],
                       lbl='%s-%i' % (c['label'],c['shifts']),
                       hidden='^.%s.available?=!#v' % c['code'])     

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
