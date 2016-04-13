#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method,metadata

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('game_id')
        r.fieldcell('_row_count')

    def th_order(self):
        return 'game_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')

class ViewFromGmTools(BaseComponent):

    def th_struct_toplay(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', name='N.')
        r.fieldcell('scene_type',name='Type', width='10em')
        r.fieldcell('title',name='Title', width='14em', validate_notnull=True)
        r.fieldcell('description',name='Description', width='100%')
        r.cell('play_scene',name="Play",calculated=True,width='6em',
                    cellClasses='cellbutton',
                    format_buttonclass='svg_icon_24 play',
                    format_isbutton=True,
                    format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                      genro.publish('play_scene', {scene_id:row['_pkey']});""")
        r.cell('close_scene',name="Close",calculated=True,width='6em',
                    cellClasses='cellbutton',
                    format_buttonclass='svg_icon_24 exit',
                    format_isbutton=True,
                    format_onclick="""var row = this.widget.rowByIndex($1.rowIndex);
                                     this.widget.sourceNode.setRelativeData('play_data.current_scene_id',null);
                                     genro.publish('close_scene',{scene_id:row['_pkey']})""")
    def th_struct_closedscenes(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', name='N.')
        r.fieldcell('scene_type',name='Type', width='10em')
        r.fieldcell('title',name='Title', width='13em')
        r.fieldcell('description',name='Description', width='100%')

    def th_order(self):
        return '_row_count'

    def th_top_custom(self,top):
        top.bar.replaceSlots('vtitle','sections@is_closed')


    @metadata(variable_struct=True)
    def th_sections_is_closed(self):
        l = [dict(code='in_play', caption='To play', condition="$closed IS NOT TRUE", struct='toplay'),
             dict(code='closed', caption='Played', condition="$closed IS TRUE", struct='closedscenes')]
        return l





class Form(BaseComponent):
    py_requires='gnrcomponents/framegrid:TemplateGrid,gnrcomponents/formhandler:FormHandler'

    def th_form(self, form):
        bc = form.center.borderContainer(datapath='.record')
        fb = bc.contentPane(region='top').div(margin_right='30px', padding='10px').formbuilder(cols=2,width='100%',
                border_spacing='4px', lbl_width='6em')
        fb.field('scene_type', lbl='Type', width='12em', validate_notnull=True, hasDownArrow=True)
        fb.field('title', lbl='Title', width='17tem')
        fb.field('description', lbl='Description',colspan=2, height='50px', width='35em')
        fb.field('closed',html_label=True)
        self.situationAspects(bc)
        #self.npcs(tc)

    def situationAspects(self, bc):
        bc.templateGrid(title='Situation aspects',region='center',
                           frameCode='situationAspects',
                           datapath='#FORM.situation_aspects',
                            _class='aspectGrid',
                            addrow=True,
                            delrow=True,
                           storepath='#FORM.record.data.situation_aspects',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width='24em'),
                                   dict(value='^.hidden', wdg='checkbox', lbl='Hidden')])

    def npcs(self, tc):
        pane = tc.contentPane(title='Npcs in scene')
        pane.inlineTableHandler(relation='@npcs',
                               viewResource='ViewFromScene',
                               searchOn=False,
                                picker='npc_id',
                                picker_condition='game_id=:game_id AND $dead IS NOT TRUE',
                                picker_condition_game_id='=#FORM.record.game_id')
        #table='fate.npc',
        #condition='$id IN :npc_pkeys',
        #condition_npcs='=#FORM.record.npc_pkeys',

    @public_method
    def th_onLoading(self, record, newrecord, loadingParameters, recInfo):
        if newrecord:
            record['scene_type']='CSC'


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px', modal=True)

    def th_bottom_custom(self,bottom):
        bar = bottom.slotBar('*,back,confirm,2',margin_bottom='2px')
        bar.back.button('!!Cancel',action='this.form.abort();')
        box = bar.confirm.div()
        box.button('!!Save',
                    iconClass='fh_semaphore',
                    action='this.form.publish("save")')
        box.slotButton('!!Play Scene',action= """if(this.form.changed){
                                              console.log('SAVE and PLAY');
                                              var that=this; 
                                              this.form.save({onSaved:function(){
                                                                        genro.publish('play_scene', {scene_id:arguments[0].savedPkey});
                                                                        that.form.abort();
                                                                        }
                                                             });
                                          }else{
                                            console.log('PLAY');
                                                genro.publish('play_scene', {scene_id:scene_id});
                                                this.form.abort();
                                          }""",
                        hidden='^#FORM.record.closed', 
                        scene_id='=#FORM.pkey')



