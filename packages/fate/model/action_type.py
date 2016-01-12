# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('action_type',pkey='code',name_long='Action type', name_plural='Action types', caption_field='name',lookup=False)
        self.sysFields(tbl, id=False)
        tbl.column('code', size='2',name_long='Code')
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('succeed',name_long='Succeed',name_short='Succeed')
        tbl.column('with_style',name_long='Succeed with style',name_short='With style')
        tbl.column('fail',name_long='Fail',name_short='Fail')
        tbl.column('tie',name_long='Tie',name_short='Tie')
        tbl.formulaColumn('icon', """ ' <div class="action_20 action_'|| $code ||' "></div>' """ ,
                       name_long='!!Icon')


    def sysRecord_OV(self):
        return self.newrecord(code='OV',
                              name='Overcome',
                              description='Overcome')

    def sysRecord_CA(self):
        return self.newrecord(code='CA',
                              name='Create advantage',
                              description='Create advantage')

    def sysRecord_AT(self):
        return self.newrecord(code='AT',
                              name='Attack',
                              description='Attack')

    def sysRecord_DF(self):
        return self.newrecord(code='DF',
                              name='Defend',
                              description='Defend')


