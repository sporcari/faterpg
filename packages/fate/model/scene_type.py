# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('scene_type',pkey='code',name_long='Scene type',name_plural='Scene type',caption_field='name')
        self.sysFields(tbl,id=False)
        tbl.column('code',size='3',name_long='Code')
        tbl.column('name',name_long='Name')
        tbl.column('description',name_long='Description')

    def sysRecord_CSC(self):
        return self.newrecord(code = 'CSC',
                            name='Common Scene',
                            description="""Common scene, not zoomed.""")
    def sysRecord_CNF(self):
        return self.newrecord(code = 'CNF',
                            name='Conflict',
                            description="""When two or more characters are trying to directly harm each other""")
    def sysRecord_CTS(self):
        return self.newrecord(code = 'CTS',
                            name='Contest',
                            description="""When two or more characters are competing for a goal""")
    def sysRecord_CHL(self):
        return self.newrecord(code = 'CHL',
                            name='Challenge',
                            description="""When one or more characters try to achieve something dynamic or complicated""")


