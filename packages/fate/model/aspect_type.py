# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('aspect_type',pkey='id',name_long='Aspect type',name_plural='Aspect types',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',size=':15',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description',unique=True)
