var Fate = {
    aspectTemplates: {
        BASE:"<div class='txtLabel'>$type_label</div><div class='mainTxt'>$phrase</div><div class='aspect_description'>$description</div>", 
        STUNT:"<div class='txtLabel'>$name</div><div class='mainTxt'>$description</div>"  
    },
    renderAspectRow: function(row){
        var tpl = this.aspectTemplates[row.aspect_type] || this.aspectTemplates['BASE'];
        return dataTemplate('<div class="tplcell tpl_'+row.aspect_type+'">'+tpl+'</div>',row);
    },
    skillDict: function(code,field){
        return genro.getData('main.game_skills.'+code+'.'+field);
    },
    characterAspectsForm:function(pane, kw){
        var data = kw.rowDataNode.getValue();
        var width = '25em';
        if (data.getItem('aspect_type')=='PH'){
            if(data.getItem('phase')>1){
                pane._('div', {innerHTML:this.getPreviousBackstory(kw.grid.sourceNode,data.getItem('phase')),
                            width:width,lbl:'Backstory',_class:'bs_prevstories'});
            }
            pane._('simpleTextArea', {height:'60px',width:width, lbl:data.getItem('story_label'),value:'^.backstory'});
        }
        pane._('textbox',{value:'^.phrase', width:width,lbl:data.getItem('type_label')});
    },
    stuntsForm:function(pane, kw){
        pane._('textbox',{value:'^.name', width:'15em',lbl:'Name'});
        pane._('simpleTextArea',{value:'^.description', width:'38em',lbl:'Description', height:'60px'});
    },
    onSkillsUpdate:function(sourceNode, skills, game_record){
        var skilldict = this.getSkillLevelDict(skills);
        this.updateStressTracks(sourceNode, game_record.getItem('stress_tracks'), skilldict);
        this.updateConsequences(sourceNode, game_record.getItem('consequences_slots'), skilldict);
    },
    updateConsequences: function(sourceNode, consequences_slots, skilldict){
        var cons_code;
        var sk;
        var lv;
        var requested_lv;
        var cs;
        var is_hidden;
        consequences_slots.forEach(
            function(n){
                cs = n.getValue();
                sk = cs.getItem('skill');
                requested_lv = cs.getItem('lv') || 1;
                if (sk){
                    lv = skilldict[sk] || 0;
                    is_hidden = (lv < requested_lv);
                    sourceNode.setRelativeData('.consequences.'+cs.getItem('code')+'.is_hidden',is_hidden);
                }
            }
        );
    },
    updateStressTracks: function(sourceNode, stress_tracks, skilldict){
        var that = this;
        var st;
        var track_code;
        var sk;
        var n_boxes;
        var lv;
        stress_tracks.forEach(
            function(n){
                st = n.getValue();
                track_code = st.getItem('code');
                sk = st.getItem('skill');
                n_boxes = st.getItem('n_boxes');
                if (sk){
                    lv = skilldict[sk] || 0;
                    n_boxes = n_boxes + that.getExtraBoxes(st, lv);
                    sourceNode.setRelativeData('.stress_tracks.'+track_code+'.n_boxes',n_boxes);
                }
            });
    },
    getExtraBoxes:function(st, lv){
        var extra_box_1 = parseInt(st.getItem('extra_box_1') || '1000');
        var extra_box_2 = parseInt(st.getItem('extra_box_2') || '1000');
        var extra_box_3 = parseInt(st.getItem('extra_box_3') || '1000');
        var extra_boxes = 0;
        if (lv >= extra_box_1){
            extra_boxes = 1;
        }
        if (lv >= extra_box_2){
            extra_boxes = 2;
        }
        if (lv >= extra_box_3){
            extra_boxes = 3;
        }
        return extra_boxes;
    },
    getSkillLevelDict:function(skills){
        var result = {};
        skills.forEach(function(n){
            var skillsforlevel = n.getValue().split(',');
            var lv = parseInt(n.label.slice(2));
            skillsforlevel.forEach(function(sk){
                result[sk]=lv;
            });
        });
        return result;
    },
    getPreviousBackstory: function(sourceNode, phase){
       if (!phase || phase <2){
           return '';
       }
       var username = sourceNode.getInheritedAttributes()['username'];
       var pc_sheets = genro.getData('play_data.pcsheets');
       var index = pc_sheets.index(username);
       var backstories = [];
       var backstory;
       var character;
       var name;
       var phrase;
       var aspectrec;
       while(phase>=2){
           index = index > 0 ? index-1 : pc_sheets.len()-1;
           character = pc_sheets.getItem('#'+index);
           name = character.getItem('name') || '';
           phase=phase-1;
           aspectrec = character.getItem('aspects.ph'+phase);
           backstory = aspectrec.getItem('backstory') || '';
           phrase = aspectrec.getItem('phrase') || '';
           backstories.push('<div class="bs_phase"><div class="bs_name">'+name+'</div><div class="bs_story">'+backstory+'</div><div class="bs_phrase">'+phrase+'</div></div>');
       }
       return backstories.reverse().join('');

    },

    copyStunts:function(grid, data){
        if(!data.length){
            return;
        }
        var pc_stunts = grid.storebag();
        var empty_slot;
        var value;
        var r;
        pc_stunts.forEach(function(n){
            value = n.getValue();
            if (value.getItem('name') || value.getItem('description')){
                return;
            }
            r = data.shift();
            if(r){
                value.setItem('name',r.name);
                value.setItem('description',r.description);
            }
        })
    },
    renderSkillsPyramid: function(skills, skill_cap){
        if(skills){
            var slots;
            var result = [];
            var skillname;
            var levelskills;
            var skillcode;
            var k;
            var skillrecord;
            var row;
            var description;
            for (var i=skill_cap; i>=0; i--){
                slots =  skill_cap - i;
                row = ['<tr>'];
                for (var j=0; j<slots; j++){
                    k = "lv"+(i+1);
                    levelskills = skills.getItem(k).split(',');
                    skillcode = levelskills[j] || null;
                    
                    if (skillcode){
                        skillrecord = genro.getData('main.game_skills.'+skillcode);
                        skillname = skillrecord.getItem('name');
                        description = skillrecord.getItem('description');
                    }else{
                        skillname='&nbsp;';
                        description='';
                    }
                       
                    row.push('<td class="skillCell" title="'+description+'">'+skillname+'</td>');
                }
                row.push('</tr>')
                row = row.join('');
                result.push(row);
            }
            result = result.join('');
            return '<table class="skillPyramid"></tbody>'+ result+'</tbody></table>';
        }
    },
    skillsSetGetter:function(cell,row,rowIdx){
        var sourceNode = cell.grid.sourceNode;
        var sets = sourceNode.getRelativeData(sourceNode.attr.userSets);
        if(!sets){
            return;
        }
        var cellname = cell.field;
        var setsNodes = sets.getNodes();
        var disabled = '<div class="checkboxOff" disabled="true"></div>';
        var regexp = new RegExp('(^|,)'+row._pkey+'($|,)');
        for(var i=0; i<setsNodes.length; i++){
            var n = setsNodes[i];
            var v = n.getValue();
            if(v.match(regexp)!=null){
                if(n.label == cellname){
                    return true;
                }else{
                    return disabled;
                }
            }
        }
        var currSet = sets.getItem(cellname);
        var slen = currSet? currSet.split(',').length:0;
        if(slen>=cell.skillmax){
            return disabled;
        }
        return false;
    },

    currentActionBag:function(){
        return genro.getData('current_scene.current_action');
    },

    loadAction:function(label){
        var actions = genro.getData('current_scene.actions');
        if(!actions){
            actions = new gnr.GnrBag();
            genro.setData('current_scene.actions',actions);
        }
        if(label){
            genro.setData('current_scene.current_action',actions.getItem(label).deepCopy());
        }else{
            var newaction = new gnr.GnrBag();
            newaction.setItem('active_steps',new gnr.GnrBag());
            newaction.setItem('opposition_steps',new gnr.GnrBag());
            newaction.setItem('data',new gnr.GnrBag());
            genro.setData('current_scene.current_action',newaction);
            genro.setData('current_scene.action_status','action');
        }
    },

    actionPhaseConfirmed:function(data,status,template){
        var steps;

        var d = data.deepCopy();
        var character_id = d.getItem('character_id');
        var phase_description;
        var current_action = this.currentActionBag();
        if(status=='waiting_active_player'){
            if(!(d.getItem('action_type') || d.getItem('skill'))){
                return;
            }
            steps = current_action.getItem('active_steps');
            phase_description = dataTemplate(template || "$name $action_type${ $target_name} $skill ${<br>$details}",d);
            d.setItem('description',phase_description);            
            var blacklist = [character_id];
            var target_id = data.getItem('target_id');
            var target_name = data.getItem('target_name');
            if(target_id){
                blacklist.push(target_id);
            }
            current_action.setItem('data.target_id',target_id);
            current_action.setItem('data.target_name',target_name);
            current_action.setItem('data.opponent_blacklist',blacklist.join(','));
            current_action.setItem('active_player.name',d.getItem('name'));
            current_action.setItem('active_player.image_url',d.getItem('image_url'));
            current_action.setItem('active_player.player_id',d.getItem('player_id'));
            current_action.setItem('active_player.rolled',false);
            genro.setData('current_scene.action_status','opposition');
            steps.setItem('r_'+steps.len(),d);
        }else if(status=='waiting_opposition'){
            if(d.getItem('name')){
                phase_description = dataTemplate(template || "Opposition: $name $action_type${ $target_name} $skill ${<br>$details}",d);
                d.setItem('description',phase_description);
            }else{
                phase_description = dataTemplate(template || "Opposition $passive_opposition",d);
                d.setItem('description',phase_description);
            }
            steps = current_action.getItem('opposition_steps');
            var passive = d.getItem('passive');
            var passive_opposition =  d.getItem('passive_opposition') || 'Opposition';
            current_action.setItem('opponent_player.name',d.getItem('name') || passive_opposition);
            if(passive){
                current_action.setItem('opponent_player.passive',true);
                current_action.setItem('opponent_player.rolled',true);
            }
            current_action.setItem('opponent_player.player_id',d.getItem('player_id'));
            current_action.setItem('opponent_player.image_url',d.getItem('image_url'));
            genro.setData('current_scene.action_status','roll_dice');
            steps.setItem('r_'+steps.len(),d);
        }
        genro.setData('current_scene.current_action.phase',null);
    },

    writeActionStep:function(type,data,attributes){
        var steps = this.currentActionBag().getItem(type+'_steps');
        steps.setItem('r_'+steps.len(),data,attributes);
    },

    getAvailableCharacterSelector:function(kw){
        var available_characters = genro.getData('current_scene.available_characters');
        var data = available_characters.getNodes().map(function(n){return n.attr;});
        var blacklist = kw._sourceNode.getAttributeFromDatasource('blacklist');
        blacklist = blacklist? blacklist.split(','):[];
        var _id = kw._id;
        var _querystring = kw._querystring;
        var cbfilter = function(n){return true;};
        if(_querystring){
            _querystring = _querystring.slice(0,-1).toLowerCase();
            cbfilter = function(n){
                if(blacklist.length>0 && blacklist.indexOf(n._pkey)>=0){
                    return false;
                }
                return n.name.toLowerCase().indexOf(_querystring)>=0;
            };
        }else if(_id){
            cbfilter = function(n){return n._pkey==_id;};
        }
        data = data.filter(cbfilter);
        return {headers:'name:Name',data:data};
    },



    setAvailableCharacters:function(players_character,npcs,gm_id){
        var result = new gnr.GnrBag();
        var v,name,skilldict,skills,image_url;
        var that = this;
        players_character.forEach(function(n){
            v = n.getValue();
            name = v.getItem('name') || n.label;
            skills = v.getItem('skills');
            if(skills){
                skilldict = that.getSkillLevelDict(skills);
            }
            image_url = v.getItem('image_url');
            image_url = image_url?image_url.split('?')[0]:null;
            result.setItem(n.label,null,{name:name,player_id:n.attr.player_id,caption:name,
                                          image_url:image_url,
                                          npc:false,_pkey:n.label,character_id:n.label,
                                          character_skills:skilldict});
        });
        npcs.forEach(function(n){
            v = n.getValue();
            name = v.getItem('metadata.name');
            image_url = v.getItem('metadata.image_url');
            image_url = image_url?image_url.split('?')[0]:null;
            skilldict = {};
            skills = v.getItem('skills');
            if(skills){
                skills.values().forEach(function(v){skilldict[v.getItem('skill')] = parseInt(v.getItem('lv'));});
            }
            result.setItem(n.label,null,{name:name,player_id:gm_id,caption:name,npc:true,image_url:image_url,
                                        character_skills:skilldict,character_id:n.label,_pkey:n.label});
        });
        genro.setData('current_scene.available_characters',result);
    },

    characterPars:function(character_id){
        var characters = genro.getData('current_scene.available_characters');
        var pars = characters.getAttr(character_id);
        return objectUpdate({},pars);
    },

    diceContent:function(dice_value){
        var dice_class = 'dice_box ';
        if(dice_value!==null){
            dice_class =dice_class +['dice_minus','dice_blank','dice_plus'][dice_value+1];
        }
        return '<div class="'+dice_class+'">&nbsp;</div>';
    },

    skillSelectValues:function(kw){
        var sourceNode = kw._sourceNode;
        var action_type = sourceNode.getAttributeFromDatasource('action_type');
        var character_skills = sourceNode.getAttributeFromDatasource('character_skills') || {};
        var data = [];
        var skills = sourceNode.getRelativeData('main.game_skills');
        var _id = kw._id;
        var _querystring = kw._querystring;
        skills.forEach(function(n){
            var v = n.getValue();
            var code = v.getItem('code');
            var action_types = new gnr.GnrBag(v.getItem('action_types'));
            if(!action_type || action_types.getNode(action_type)){
                data.push({skillname:v.getItem('name'),caption:v.getItem('name'),
                            _pkey:code,level:character_skills[code] || 0});
            }
        });
        var cbfilter = function(n){return true;};
        if(_querystring){
            _querystring = _querystring.slice(0,-1).toLowerCase();
            cbfilter = function(n){return n.skillname.toLowerCase().indexOf(_querystring)>=0;};
        }else if(_id){
            cbfilter = function(n){return n._pkey==_id;};
        }
        data = data.filter(cbfilter);
        data = data.sort(function(a,b){return a.level>=b.level?-1:1;});
        return {headers:'skillname:Skill,level:Level',data:data};
    },

    prepareAspectPickerData:function(){
        var situation_aspects = new gnr.GnrBag();
        var cb = function(node,kw){
            var sv = node.getValue();
            var phrase = sv.getItem('phrase');
            kw.appendTo.setItem(node.label,null,{caption:phrase,phrase:phrase});
        };
        genro.getData('current_scene.situation_aspects').forEach(cb,null,{appendTo:situation_aspects});
        var world_aspects = new gnr.GnrBag();
        world_aspects.setItem('current',new gnr.GnrBag(),{caption:'Current'});
        world_aspects.setItem('places',new gnr.GnrBag(),{caption:'Places'});
        world_aspects.setItem('impending',new gnr.GnrBag(),{caption:'Impending'});
        world_aspects.setItem('faces',new gnr.GnrBag(),{caption:'Faces'});
        var world_aspects_source =genro.getData('play_data.world_aspects');
        world_aspects.forEach(function(n){
            var v = n.getValue();
            world_aspects_source.getItem(n.label).forEach(cb,null,{appendTo:v});
        });
        var pgaspects = new gnr.GnrBag();
        genro.getData('play_data.pcsheets').forEach(function(n){
            var v = n.getValue();
            var asp = v.getItem('aspects');
            var name = v.getItem('name') || n.label;
            var appendTo = new gnr.GnrBag();
            pgaspects.setItem(n.label,appendTo,{caption:name});
            asp.forEach(cb,null,{appendTo:appendTo});
        });

        var npcaspects = new gnr.GnrBag();
        genro.getData('npcs').forEach(function(n){
            var v = n.getValue();
            var asp = v.getItem('aspects');
            var name = v.getItem('metadata.name') || n.label;
            var appendTo = new gnr.GnrBag();
            npcaspects.setItem(n.label,appendTo,{caption:name});
            asp.forEach(cb,null,{appendTo:appendTo});
        });
        var result = new gnr.GnrBag();
        result.setItem('world',world_aspects,{caption:'World'});
        result.setItem('players',pgaspects,{caption:'Players'});
        result.setItem('npcs',npcaspects,{caption:'NPC'});
        result.setItem('situation',situation_aspects,{caption:'Situation'});
        return result;
    }
};
