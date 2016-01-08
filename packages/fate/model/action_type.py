# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('action_type',pkey='id',name_long='Action type',name_plural='Action types',caption_field='name',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('icon',name_long='Icon',name_short='Icon')
        tbl.column('succeed',name_long='Succeed',name_short='Succeed')
        tbl.column('with_style',name_long='Succeed with style',name_short='With style')
        tbl.column('fail',name_long='Fail',name_short='Fail')
        tbl.column('tie',name_long='Tie',name_short='Tie')
