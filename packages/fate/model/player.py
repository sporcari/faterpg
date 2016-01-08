# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('player',pkey='id',name_long='Player',name_plural='Players',caption_field='id')
        self.sysFields(tbl)
        tbl.column('firstname',name_long='firstname')
        tbl.column('lastname',name_long='lastname')
        tbl.column('nickname',name_long='nickname')
        tbl.column('user_id',name_long='user_id').relation('adm.user.id',relation_name='player', mode='foreignkey', onDelete='setnull', one_one=True)
        tbl.column('avatar_img',name_long='Avatar Img',name_short='Avatar')
