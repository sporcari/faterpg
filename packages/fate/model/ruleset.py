# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('ruleset',pkey='code',name_long='Ruleset',name_plural='Rulesets',caption_field='name',lookup=True)
        tbl.column('code',size=':4',name_long='Code',name_short='Code',unique=True,indexed=True)
        tbl.column('name',size=':30',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
