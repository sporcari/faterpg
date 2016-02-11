var Fate = {
    aspectTemplates: {
        BASE:"<div class='aspectLabel'>$type_label</div><div class='aspect_phrase'>$phrase</div><div class='aspect_description'>$description</div>"   
    },
    renderAspectRow: function(row){
        var tpl = this.aspectTemplates[row.aspect_type] || this.aspectTemplates['BASE'];
        return dataTemplate('<div class="aspect_'+row.aspect_type+'">'+tpl+'</div>',row);
    },
    skillDict: function(code,field){
        return genro.getData('main.game_skills.'+code+'.'+field);
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
