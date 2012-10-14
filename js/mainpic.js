console.log('Loaded mainpic.js');

function handleClick(e){	
	cap = document.createElement('input')
	cap.type = 'text'
	captionline.innerText = ""
	holder.appendChild(cap)
	
	$(document).keypress(function(e2){
		if(e2.which == 13) {		
			var caption = cap.value;
			var idvalue = id.innerText;
			var direction = '/pin/' + idvalue;
			captionline.innerText = caption;
			holder.removeChild(cap);
			
			$.ajax(direction, {
				type: 'POST',
				data: {
					caption: caption
				}
			});
		}
	})	
	
}


function otherClick(e){
	var idvalue = id.innerText;
	var direction = '/pin/' + idvalue;	
	if(pinprivateval.innerText == "on")
		privateval = "";
	else
		privateval = "on";
	
	$.ajax(direction, {
		type: 'POST',
		data: {
			pinprivate: privateval
		}
	});	
	

	
}




$(document).ready(function(){
	$('#captionline').click(handleClick);
	$('#pinprivate').click(otherClick);
	
})
