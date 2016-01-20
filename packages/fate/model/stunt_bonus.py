# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('stunt_bonus',pkey='code',name_long='Stunt Bonus',name_plural='Stunt Bonus',caption_field='name',rowcaption='$name',lookup=True)
        self.sysFields(tbl,id=False)
        tbl.column('code',size='2',name_long='Code',name_short='Code',unique=True)
        tbl.column('name',name_long='Name',name_short='Name')
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('num_value',dtype='I',name_long='Roll bonus',name_short='Roll bonus')

    def sysRecord_B2(self):
        return self.newrecord(code='B2',
                              name='+2',
                              num_value=2,
                              description='+2 On Roll')

    def sysRecord_CA(self):
        return self.newrecord(code='CA',
                              name='Create aspect',
                              description='Create aspect')

    def sysRecord_BO(self):
        return self.newrecord(code='BO',
                              name='Create boost',
                              description='Create boost')
    def sysRecord_DS(self):
        return self.newrecord(code='DS',
                              name='Deal Stress',
                              description='Deal Stress')
    def sysRecord_RS(self):
        return self.newrecord(code='RS',
                              name='Reduce Stress',
                              description='Reduce Stress')
    def sysRecord_TO(self):
        return self.newrecord(code='TO',
                              name='Turn order',
                              description='Turn order')
    def sysRecord_IC(self):
        return self.newrecord(code='IC',
                              name='Inflict Cons.',
                              description='Inflict Consequence')
    def sysRecord_RC(self):
        return self.newrecord(code='RC',
                              name='Reduce Cons.',
                              description='Reduce Consequences')
    def sysRecord_FI(self):
        return self.newrecord(code='FI',
                              name='Free invoke',
                              description='Free invoke')
