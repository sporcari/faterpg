# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('player',pkey='id',name_long='Player',name_plural='Players',caption_field='id')
        self.sysFields(tbl)
        tbl.column('nickname',name_long='Nickname')
        tbl.column('user_id',name_long='user_id').relation('adm.user.id',relation_name='player', mode='foreignkey', onDelete='setnull', one_one=True)
        tbl.column('avatar_url',name_long='Avatar Url',name_short='Avatar url')
        tbl.column('favourite_settings', name_long='Favourite settings')
        tbl.column('is_gm', dtype='B', name_long='GM')
        tbl.formulaColumn('avatar_img', "avatar_url" ,dtype='P',name_long='!!Avatar image',name_short='Avatar', cell_format='auto:.5')
