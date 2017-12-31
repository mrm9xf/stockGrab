// JAVASCRIPT //

function getData(code){
    $.ajax({'https://www.google.com/search?q=' + code, function(data, status){
	console.log(status);    
    });
}