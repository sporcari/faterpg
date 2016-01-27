# encoding: utf-8

from gnr.core.gnrdecorator import public_method


class Table(object):
    def config_db(self,pkg):
        tbl =  pkg.table('friend',pkey='id',name_long='Friend',name_plural='Friends',caption_field='id')
        self.sysFields(tbl)
        tbl.column('me_id',size='22',name_long='me_id').relation('fate.player.id',relation_name='friends', onDelete='cascade', mode='foreignkey')
        tbl.column('friend_id',size='22',name_long='friend_id').relation('fate.player.id',relation_name='friended_by', onDelete='cascade', mode='foreignkey')
        tbl.aliasColumn('friend_username', relation_path='@friend_id.username', name_long='Username')
        tbl.aliasColumn('friend_fullname', relation_path='@friend_id.fullname', name_long='Name')
        tbl.aliasColumn('friend_nickname', relation_path='@friend_id.nickname', name_long='Nickname')
        tbl.aliasColumn('avatar_img', relation_path='@friend_id.avatar_img', name_long='Avatar')
        tbl.formulaColumn('current_player_friend', '($me_id=:env_player_id)', dtype='B')

    @public_method
    def addFriend(self, friend_id):
        self.insert(dict(me_id=self.db.currentEnv.get('player_id'), friend_id=friend_id))
        self.db.commit()

        