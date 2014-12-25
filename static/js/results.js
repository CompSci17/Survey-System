jQuery( function($){
	$('.importance tr').each(function() {
	    var $tds = $(this).children('td'),
	        max = null,
	        maxIndex = null;

	    $tds.each(function() {
	        var value = +$(this).text().substr(1);
	        if(!isNaN(value)) {
	            if(!max || value > max) {
	                max = value;
	                maxIndex = $(this).index();
	            }
	        }
	    });
	    if(maxIndex !== null) {
	        $tds.eq(maxIndex).addClass('highest');
	    }
	});
});

