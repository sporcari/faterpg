# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('skill',pkey='id',name_long='Skill',name_plural='Skills',caption_field='name',lookup=True)
        self.sysFields(tbl)
        tbl.column('name',size=':20',name_long='Name',name_short='Name',unique=True)
        tbl.column('description',name_long='Description',name_short='Description')
        tbl.column('skill_set',size='3',name_long='Skill set',name_short='Skill set').relation('fate.skill_set.code',relation_name='skills', mode='foreignkey', onDelete='cascade')
