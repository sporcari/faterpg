# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('setting',pkey='name',name_long='Setting',name_plural='Settings',caption_field='name',lookup=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name')
