# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('approach_set',pkey='code',name_long='Approach set',name_plural='Approach set',caption_field='name',lookup=True)
        self.sysFields(tbl, id=False)
        tbl.column('code',size='3',name_long='Code',name_short='Code',unique=True,indexed=True)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        
    def sysRecord_STD(self):
        return self.newrecord(code='STD',
                              name='FAE Standard',
                              description='Accelerated Edition standard approaches')
                              
