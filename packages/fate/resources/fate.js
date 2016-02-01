var Fate = {
    aspectTemplates: {
        BASE:"<div class='aspectLabel'>$type_label</div><div class='aspect_phrase'>$phrase</div><div class='aspect_description'>$description</div>"   
    },
    renderAspectRow: function(row){
        var tpl = this.aspectTemplates[row.aspect_type] || this.aspectTemplates['BASE'];
        return dataTemplate('<div class="aspect_'+row.aspect_type+'">'+tpl+'</div>',row);
    }
};
