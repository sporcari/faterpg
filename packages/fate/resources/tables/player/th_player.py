#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('@user_id.firstname')
        r.fieldcell('@user_id.lastname')
        r.fieldcell('nickname')
        r.fieldcell('avatar_img')

    def th_order(self):
        return 'firstname'

    def th_query(self):
        return dict(column='id', op='contains', val='')
        
    def th_options(self):
        return dict(widget='dialog')


class Form(BaseComponent):

    def th_form(self, form):
        
        bc = form.center.borderContainer(datapath='.record')
        fb = bc.contentPane(region='center', margin='4px').formbuilder(cols=1, border_spacing='4px')
        fb.field('@user_id.email', )
        fb.field('@user_id.username',)
        fb.field('@user_id.firstname')
        fb.field('@user_id.lastname')
        fb.field('nickname')

        bc.contentPane(region='right',width='150px', margin='4px').img(src='^.avatar_img', crop_width='110px',crop_height='110px',
                        placeholder=self.getResourceUri('images/missing_photo.png'),
                        upload_folder='site:img/player/avatar',edit=True,
                        rowspan=2,
                        upload_filename='=#FORM.record.id',crop_border='2px solid #ddd',
                        crop_rounded=8,crop_margin='5px',
                        crop_margin_left='10px',
                        zoomWindow=True)
        
    def th_options(self):
        return dict(dialog_height='200px', dialog_width='500px')
