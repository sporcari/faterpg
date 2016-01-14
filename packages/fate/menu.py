#!/usr/bin/python
# -*- coding: UTF-8 -*-

def config(root,application=None):
    fate = root.branch('Fate')
    fate.thpage('Aspect types',table='fate.aspect_type')
    fate.thpage('Aspects',table='fate.aspect')
    fate.thpage('Character Approaches',table='fate.character_approach')
    fate.thpage('Character stunts',table='fate.character_stunt')
    fate.thpage('Games',table='fate.game')
    fate.thpage('NPCS',table='fate.npc')
    fate.thpage('Players',table='fate.player')
    fate.thpage('Characters',table='fate.player_character')
    fate.thpage('Scenarios',table='fate.scenario')
    fate.thpage('Scenes',table='fate.scene')
    fate.thpage('Sessions',table='fate.session')
    fate.thpage('Actions',table='fate.action_type')
    fate.thpage('Skills',table='fate.skill')
    fate.lookups('Lookup tables',lookup_manager='fate')
