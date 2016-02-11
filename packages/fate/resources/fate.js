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
    skillPickerHandler: function(skills,_node, _triggerpars,_reason){
        console.log('PICKER HANDLER','skills:',skills, 'node:',_node, 'trigpars:',_triggerpars,'reason:', _reason);
    },
    renderSkillsPyramid: function(skills, skill_cap){
        console.log('skills',skills,'cap',skill_cap);
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
    }
};
