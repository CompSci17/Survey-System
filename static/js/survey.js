jQuery(function($){

	var sortme = $( ".sortable" ).parent().parent().parent();

	sortme.sortable({
	  placeholder: "ui-state-highlight",
	  items: "> li"
	});

	sortme.disableSelection();
});

// function submitOrderOfImportance( ){
// 	jQuery(function($){

// 		var selection = $( ".sortable" ).parent().parent().parent();
// 		var questionIDs = {};
// 		var outputString = '';
// 		var lastQuestionId = 0;

// 		selection.find("li").each( function(){
// 			var questionID = $( this ).find( "input" ).attr( "name" ) ;

// 			if( questionID != lastQuestionId ){
// 				outputString = '';
// 			}

// 			outputString = outputString + "," + $( this ).text();
// 			questionIDs[ questionID ] = outputString;

// 			lastQuestionId = questionID;

// 		});

// 		console.log( questionIDs );

// 		$( questionIDs ).each( function(){ 
// 			for ( var questionID in this ){
// 				questionIDs[ questionID ] = questionIDs[ questionID ].replace( /,  /g, ", " );
// 				questionIDs[ questionID ] = questionIDs[ questionID ].substring( 2 );

// 				$( "[name='"+ questionID +"']").val( questionIDs[ questionID ] );
// 			}
// 		});

// 		console.log( questionIDs );


// 	});
// }