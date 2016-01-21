# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt_set',pkey='code',name_long='Stunt set',name_plural='Stunt set',caption_field='name',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size='3',name_long='Code',unique=True)
        tbl.column('name',name_long='Name',unique=True)
        tbl.column('description',name_long='Description')

    def sysRecord_STD(self):
        return self.newrecord(code='STD',
                              name='Core standard stunts',
                              description='Core standard stunts')