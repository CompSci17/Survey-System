jQuery(function($){

	var sortme = $( ".sortable" ).parent().parent().parent();

	sortme.sortable({
	  placeholder: "ui-state-highlight",
	  items: "> li"
	});

	sortme.disableSelection();
});
