


function showData(data){
	pins = data
	body = document.body
	
	
	for(var pin in pins){
		$('#result').html(pin + ' ' + pins[pin]);
		picdiv = document.createElement('div');
		picdiv.id = 'displaybox';
		
		pic = document.createElement('img');
		pic.id = 'imgpx';
		pic.src = pins[pin];
		
		body.appendChild(picdiv);
		picdiv.appendChild(pic);
	}
	
}



function handleClick(e){
	$.ajax('/pin',{
		type: 'GET',
		data: {
			fmt: 'json'
		},
	
		success: showData
	})
	
}


$(document).ready(function(){
	handleClick();
})