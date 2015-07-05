$(function(){
    $('.collapsible').each(function(){
        var heading = $('.collapsible-heading', this);
        var content = $('.collapsible-content', this);
        var icon = $('<span class="collapser glyphicon glyphicon-collapse-up" aria-hidden="true"></span>').appendTo(heading);
        heading.click(function(){
            content.slideToggle();
            icon.toggleClass('glyphicon-collapse-up glyphicon-collapse-down');
            heading.toggleClass('collapsed');
        });
    });
    $('table.row-formset').floatThead({
        scrollContainer: function(table){
            return table.parent();
        }
    });
});
