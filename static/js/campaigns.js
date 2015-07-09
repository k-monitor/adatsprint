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
    $('#pdfviewer').resizable({handles: 's'});
    $('.mp-form-expenses').resizable({handles: 's', alsoResize: '.expense-table-outer'});
    $('table.row-formset').floatThead({
        scrollContainer: function(table){
            return table.parent();
        }
    });
    $('tr.formset-empty-row').each(function(){
        // Add the ability to add a new row to the formset
        // Our formset always include a bonus extra row that we detach from
        // the DOM and clone it to add more and more row.
        // When we clone it, we also need to take care of updating the management
        // form and the name and ids of the input contained in the row.
        // For now, we make the easy assumption that our row only contains
        // <input> elements.
        var emptyRow = $(this);
        var table = emptyRow.parents('table');
        var prefix = emptyRow.attr('data-formset-prefix');
        var totalFormsInput = $('input[id=id_'+prefix+'-TOTAL_FORMS]');
        var currentTotalForms = parseInt(totalFormsInput.val(), 10);
        var icon = $('<a class="btn btn-default"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span>Add row</a>').insertAfter(table);

        emptyRow.detach();
        currentTotalForms -= 1;
        icon.click(function(){
            var newRow = emptyRow.clone();
            newRow.removeClass('formset-empty-row');
            currentTotalForms += 1;
            totalFormsInput.val(currentTotalForms);
            $('input', newRow).each(function() {
                // Update the value of the management form and rewrite the name/id attributes
                var input = $(this);
                var idRegexp = new RegExp('^id_'+prefix+'-(\\d+)-(.+)$');
                var nameRegexp = new RegExp('^'+prefix+'-(\\d+)-(.+)$');
                var matchId = input.attr('id').match(idRegexp);
                var matchName = input.attr('name').match(nameRegexp);
                var newId = 'id_' + prefix + '-' + (currentTotalForms-1) + '-' + matchId[2];
                var newName = prefix + '-' + (currentTotalForms-1) + '-' + matchId[2];
                input.attr('id', newId).attr('name', newName);
            });
            newRow.appendTo(table);
        });
    });
    // prevent form submission when pressing Enter
    $('.mp-form input').keypress(function(event){
        if(event.keyCode == 13) { // Enter key
            event.preventDefault();
            console.log('Event prevented');
        }
    });
});
