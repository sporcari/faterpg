# -*- coding: UTF-8 -*-
            
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler,public:Public,fate_component'
    css_requires='css/fate'
    css_theme = 'fate'
    css_icons = 'retina/red'
    js_requires = 'fate'

    auth_main='user'

    def isDeveloper(self):
        return True

    def main(self,root,*args, **kwargs):

        kw = self.getCallArgs('__ins_user','code')
        self.game_tbl = self.db.table('fate.game')
        self.game_record = self.game_tbl.record(**kw).output('bag')
        #root.data('game',Bag())
        self.game_shared_id = self.game_record['play_data_id']
        root.data('play_data', None, shared_id=self.game_shared_id,
                                     shared_autoLoad=True,
                                     shared_autoSave=True,
                                     shared_dbSaveKw=dict(table='sys.shared_object', backup=4))


        root.data('main.game_skills', self.getGameSkills())
        root_bc = root.borderContainer(design='sidebar',datapath='main')
        self.gameHeader(root_bc.borderContainer(region='top',height='80px'))
        bc = root_bc.borderContainer(region='center')
        self.gameCharacters(root_bc)
        #self.gameCommon(bc)
        bc.data('game_record',self.game_record)
        #root.dataController("""if(!loaded){
        #        SET play_data = game_play_data.deepCopy();
        #        SET play_data.loaded=true;
        #    }""", loaded='=play_data.loaded',
        #         game_play_data='=game_record.play_data',
        #         _onStart=1)
        tc = root_bc.tabContainer(region='center',margin='2px')
        self.gameCreation(tc.borderContainer(title='Game creation'))
        tc.playPage(title='Play')

        #if self.game_record['status'] == 'CR':
        #    self.gameCreation(bc)
        #else:
        #    self.gamePlay(bc)

    def gameHeader(self,bc):
        center = bc.contentPane(region='center').img(src='/_site/resources/images/fate_head.jpg',height='60px')
        center.button('Save',action="genro.som.saveSharedObject(shared_id);",shared_id=self.game_shared_id)

    def gameCharacters(self,bc):
        tc = bc.tabContainer(region='right',width='670px',margin='2px',datapath='main.pcsheets')
        game_players = self.db.table('fate.game_player').query(where='$game_id=:gid AND $is_gm IS FALSE',
                                                    gid=self.game_record['id'],
                                                    columns="""$player_id,
                                                               $username""").fetchAsDict(key='username')
        my_rec = game_players.pop(self.user,None)
        if my_rec:
            tc.characterSheet(self.user, detachable=True)
            bc.skillsPicker()
        elif self.game_record['gm_id'] == self.rootenv['player_id']:
            tc.gmTools(self.user)
        for username in sorted(game_players.keys()):
            tc.characterSheet(username, detachable=True)
        tc.npcPage()

    #def gameCommon(self,main_bc):
    #    bc = main_bc.borderContainer(region='top',height='160px')
    #    bc.contentPane(region='left',width='500px').plainTableHandler(relation='@players',viewResource='ViewGamePlayers',
    #                                                    condition='$player_id!=:env_player_id',pbl_classes=True,configurable=False,
    #                                                    nodeId='playersTH')
    #    fb = bc.contentPane(region='center').formbuilder(cols=1,border_spacing='3px',datapath='.record')
    #    fb.textbox(value='^.description',lbl='Description')
    #    fb.button('Test',fire='test')
    #    fb.dataRpc('dummy',self.pagesTest,_fired='^test',game_id=self.game_record['id'],
    #                _onResult="""
    #                    var s = GET #playersTH.view.store;
    #                    s.forEach(function(n){
    #                            var r = result.getItem(n.attr.player_id);
    #                            if(r){
    #                                n.updAttributes({page_id:r.getItem('page_id'),_customClasses:r.getItem('_customClasses')},true);
    #                            }
    #                        });
#
    #                """,_timing=2)
#
    #@public_method
    #def pagesTest(self,game_id=None):
    #    game_players = self.pageStore().getItem('game_players.%s' %game_id)
    #    if not game_players:
    #        game_players = dict([(r['user'],r['player_id']) for r in self.db.table('fate.game_player').query(columns='$player_id,@player_id.@user_id.username AS user',
    #                                                                                                    where='$game_id=:g AND $player_id!=:env_player_id',g=game_id).fetch()])
    #        
    #        self.pageStore().setItem('game_players.%s' %game_id,game_players)
    #    pages = self.site.register.pages(filters='relative_url:/tabletop/play/%(username)s/%(code)s' %self.getCallArgs('username','code'))
    #    result = Bag()
    #    for page_id,p in pages.items():
    #        if p['user'] in game_players:
    #            result[game_players[p['user']]] = Bag(dict(page_id =page_id))
    #    connected_users = self.connection.connected_users_bag(exclude_guest=True)
    #    for k,v in game_players.items():
    #        kw = connected_users.getAttr(k)
    #        result[game_players[k]] = result[game_players[k]] or Bag()
    #        if kw:
    #            result[game_players[k]] = result[game_players[k]] or Bag()
    #            result[game_players[k]]['_customClasses'] = kw['_customClasses']
    #        else:
    #            result[game_players[k]]['_customClasses'] = 'user_disconnected'
    #    return result

    def gameCreation(self,main_bc):
        top = main_bc.borderContainer(region='top', height='300px',datapath='.game_creation')
        center = main_bc.borderContainer(region='center',datapath='.game_creation')
        width='22em'
        height='40px'
        top.templateGrid(region='left',
                            width='50%',
                           frameCode='currentIssues',
                           title='Current Issues',
                           datapath='.current_issues',
                           _class='aspectGrid',
                           storepath='play_data.world_aspects.current',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect', width=width),
                                   dict(value='^.description', wdg='simpleTextArea', lbl='Description',
                                                width=width, height=height)])
        top.templateGrid(region='center',        
                            frameCode='impendingIssues',
                           title='Impending Issues',
                           _class='aspectGrid',
                           datapath='.impending_issues',
                          storepath='play_data.world_aspects.impending',
                           template_resource='tpl/game_issues',
                           fields=[dict(value='^.phrase', wdg='textbox', lbl='Aspect',width=width),
                                   dict(value='^.description', wdg='simpleTextArea', lbl='Description',width=width, height=height)])
        center.templateGrid(region='left',
                            width='50%',
                           frameCode='faces',
                           title='Faces',
                           datapath='.faces',
                           _class='aspectGrid',
                           storepath='play_data.world_aspects.faces',
                           template_resource='tpl/faces_places',
                           fields=[dict(value='^.name', wdg='textbox', lbl='Name',width=width),
                                   dict(value='^.description', wdg='simpleTextArea', lbl='Description',width=width, height=height),
                                   dict(value='^.phrase', wdg='textbox', lbl='Aspect',width=width),
                                   dict(value='^.image_url',wdg='textbox', lbl='Image Url',width=width)])
        center.templateGrid(region='center',
                           frameCode='places',
                           title='Places',
                           _class='aspectGrid',
                           datapath='.places',
                           storepath='play_data.world_aspects.places',
                           template_resource='tpl/faces_places',
                           fields=[dict(value='^.name', wdg='textbox', lbl='Name',width=width),
                                   dict(value='^.description', wdg='simpleTextArea', lbl='Description',width=width, height=height),
                                   dict(value='^.phrase', wdg='textbox', lbl='Aspect',width=width),
                                   dict(value='^.image_url',wdg='textbox', lbl='Image Url',width=width)])

    def commonBar(self,frame):
        return frame.top.slotToolbar('2,parentStackButtons,*')

    def gameAspects(self,center):
        frame = center.framePane(frameCode='gameAspects',title='Game Aspects',
                                datapath='.gameAspects')
        self.commonBar(frame)
        frame.div('gameAspects')

    def gameSetup(self,center):
        frame = center.framePane(frameCode='gameSetup',title='New Game Setup',
                                datapath='.gameSetup')
        self.commonBar(frame)
        if self.game_record['game_creation'] and self.game_record['use_phases']:
            tc = frame.center.tabContainer(margin='2px')
            tc.contentPane(title='Game Creation')
            tc.contentPane(title='Phases Creation')
        if self.game_record['game_creation']:
            frame.center.contentPane(title='Game Creation')
        if self.game_record['use_phases']:
            frame.center.contentPane(title='Phases Creation')

    def phasesPcCreation(self,center):
        frame = center.framePane(frameCode='phasesPcCreation',title='PG Phases creation',
                                datapath='.phasesPcCreation')
        self.commonBar(frame)
        frame.div('Pg phases')


    def characterSheets(self,center):
        frame = center.framePane(frameCode='characterSheets',title='Characters',
                                datapath='.characterSheets')
        self.commonBar(frame)
        frame.div('Characters')

    def playDashboard(self,center):
        frame = center.framePane(frameCode='playDashboard',title='Play dashboard',
                                datapath='.playDashboard')
        self.commonBar(frame)
        frame.div('play dashboard')

    def gmTools(self,center):
        frame = center.framePane(frameCode='gmTools',title='Game Master',
                                datapath='.gmTools')
        self.commonBar(frame)
        frame.div('gmTools')

    def offgameTools(self,center):
        frame = center.framePane(frameCode='offgameTools',title='...',
                                datapath='.offgameTools')
        self.commonBar(frame)
        frame.div('offgameTools')
    