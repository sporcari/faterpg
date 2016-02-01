#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.web.gnrwebstruct import struct_method

class FateComponent(BaseComponent):
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
                            _class='aspectGrid',
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
        fb.textbox(value='^.phrase', lbl='Aspect')
        

    def ft_aspectStruct(self,struct):
        r = struct.view().rows()
        r.cell('aspect', _customGetter='function(row){return Fate.renderAspectRow(row);}',
                width='100%')
