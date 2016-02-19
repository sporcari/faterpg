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
        var width = '25em'
        
        if (data.getItem('aspect_type')=='PH'){
            if(data.getItem('phase')>1){
                pane._('div', {innerHTML:this.getPreviousBackstory(kw.grid.sourceNode,data.getItem('phase')),
                            width:width,lbl:'Backstory',_class:'bs_prevstories'})
            }
            pane._('simpleTextArea', {height:'60px',width:width, lbl:data.getItem('story_label'),value:'^.backstory'})
        }
        pane._('textbox',{value:'^.phrase', width:width,lbl:data.getItem('type_label')});
        console.log('params',kw);
    },

    getPreviousBackstory: function(sourceNode, phase){
       if (!phase || phase <2){
           return '';
       }
       var username = sourceNode.getInheritedAttributes()['username'];
       var pc_sheets = genro.getData('game.pcsheets');
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
           console.log(name,backstory,phrase)
           backstories.push('<div class="bs_phase"><div class="bs_name">'+name+'</div><div class="bs_story">'+backstory+'</div><div class="bs_phrase">'+phrase+'</div></div>');
       }
       return backstories.reverse().join('')

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
            result = result.join('')
            return '<table class="skillPyramid"></tbody>'+ result+'</tbody></table>'
        }
    },
    skillsSetGetter:function(cell,row,rowIdx){
        var sourceNode = cell.grid.sourceNode;
        var sets = sourceNode.getRelativeData(sourceNode.attr.userSets);
        var cellname = cell.field;
        var setsNodes = sets.getNodes();
        var disabled = '<div class="checkboxOff" disabled="true"></div>'
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
            return disabled
        }
        return false;
    }
};
