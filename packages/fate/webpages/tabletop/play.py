# -*- coding: UTF-8 -*-
            
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag

class GnrCustomWebPage(object):
    py_requires='th/th:TableHandler,public:Public,fate_component'
    css_requires='css/fate'
    css_theme = 'fate'
    css_icons = 'retina/red'
    js_requires = 'fate'
    pageOptions={'enableZoom':False}
    auth_main='user'

    def isDeveloper(self):
        return True

    def main(self,root,*args, **kwargs):
        kw = self.getCallArgs('__ins_user','code')
        self.game_tbl = self.db.table('fate.game')
        self.game_record = self.game_tbl.record(**kw).output('bag')
        self.game_shared_id = self.game_record['id']
        self.isGm = (self.game_record['gm_id'] == self.rootenv['player_id'])
        root.sharedObject('play_data', shared_id=self.game_shared_id,
                                       autoLoad=True, autoSave=True,
                                       dbSaveKw=dict(table='fate.game', backup=4))
        #controller che imposta la shared scene
        root.sharedObject('current_scene', shared_id='^play_data.current_scene_id', 
                                       autoLoad=True, autoSave=True,
                                       dbSaveKw=dict(table='fate.scene', data_column='data'))

        #controller che imposta gli shared npcs
        root.dataController("""if(!npcs) {
                                  npcs = new gnr.GnrBag();
                                  SET npcs = npcs;
                                }
                               npc_pkeys = npc_pkeys? npc_pkeys.split(',') : [];
                               var current_pkeys= npcs? npcs.keys() : [];
                               if (npcs){
                                    current_pkeys.forEach(
                                         function(pkey){
                                             if (npc_pkeys.indexOf(pkey)<0){
                                                 genro.som.unregisterSharedObject(pkey);
                                             }
                                         })
                               }
                               npc_pkeys.forEach(
                                    function(pkey){
                                        if (npcs.index(pkey)<0){
                                            var path='npcs.'+pkey;
                                            genro.som.registerSharedObject(path, pkey,
                                                                          {autoSave:true,
                                                                          autoLoad:true,
                                                                          on_unregistered:function(pkey){npcs.popNode(pkey);},
                                                                          dbSaveKw:{table:"fate.npc", data_column:"data"} 
                                                                          });
                                        }
                                    })
                               """, 
                              npc_pkeys='^current_scene.npc_pkeys',
                              npcs = '=npcs')



        root.data('main.game_skills', self.getGameSkills())
        root_bc = root.borderContainer(datapath='main')
        self.gameHeader(root_bc.borderContainer(region='top',height='40px'))
        bc = root_bc.borderContainer(region='center')
        self.gameCharacters(root_bc)
        #self.gameCommon(bc)
        bc.data('game_record',self.game_record)

        sc = root_bc.stackContainer(region='center')
        root_bc.dataController("sc.switchPage(scene_id?1:0);",sc=sc.js_widget,scene_id='^play_data.current_scene_id')
        #self.gameCreation(tc.borderContainer(title='Game creation'))
        sc.contentPane().div()
        sc.playPage()

    def gameHeader(self,bc):
        center = bc.contentPane(region='center',overflow='hidden').img(src='/_site/resources/images/fate_head.jpg',height='40px')
       #center.button('Save',action="genro.som.saveSharedObject(shared_id);",shared_id=self.game_shared_id)
       #right = bc.contentPane(region='right',width='50%')
       #if self.isGm:
       #    right.button('SAVE', action="genro.som.saveSharedObject(shared_id);", shared_id=self.game_shared_id)
       #    right.button('LOAD PLAY DATA', action="genro.som.loadSharedObject(shared_id);", shared_id=self.game_shared_id)
       #    right.dbSelect(value='^play_data.current_scene_id', dbtable='fate.scene', rowcaption='$title')

    def gameCharacters(self,bc):
        tc = bc.tabContainer(region='left',width='670px',margin='2px',datapath='main.pcsheets')
        game_players = self.db.table('fate.game_player').query(where='$game_id=:gid AND $is_gm IS FALSE',
                                                    gid=self.game_record['id'],
                                                    columns="""$player_id,
                                                               $username""").fetchAsDict(key='username')
        my_rec = game_players.pop(self.user,None)
        if my_rec:
            tc.characterSheet(self.user, detachable=True)
            bc.skillsPicker()
        elif self.isGm:
            tc.gmTools(self.user)
        for username in sorted(game_players.keys()):
            tc.characterSheet(username, detachable=True)
        tc.npcPage()
        self.gameCreation(tc.borderContainer(title='World aspects',datapath='main'))



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
    