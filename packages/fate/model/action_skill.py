# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('action_skill',pkey='id',name_long='Action for skill',name_plural='Actions for skill',caption_field='id',lookup=True)
        self.sysFields(tbl)
        tbl.column('action_type_id',size='22',name_long='Action Type',name_short='Action')
        tbl.column('skill_id',size='22',name_long='Skill',name_short='Skill')
        tbl.column('description',name_long='Description',name_short='Description')
