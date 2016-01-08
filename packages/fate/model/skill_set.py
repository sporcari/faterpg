# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('skill_set',pkey='code',name_long='Skill set',name_plural='Skill sets',caption_field='name',lookup=True)
        tbl.column('code',size='3',name_long='Code',name_short='Code',unique=True)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
