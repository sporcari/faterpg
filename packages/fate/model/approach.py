# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('approach',pkey='name',name_long='Approach',name_plural='Approaches',caption_field='name',lookup=True)
        tbl.column('name',name_long='Name',name_short='Name',unique=True,indexed=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('approach_set',size='3',name_long='Set',name_short='Set').relation('fate.approach_set.code',relation_name='approaches', mode='foreignkey', onDelete='cascade')
