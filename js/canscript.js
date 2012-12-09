var canvas;
var ctx;
var jdata;
var xCoor;
var yCoor;
var movePin;
var bool;


function showPinsOnBoard(){
	for(pinID in jdata){
		for(var i = 0; i < jdata.pinboard.length; i++){
			pin = jdata.pinboard[i];
			
			if(pinID == pin){
				pic = document.createElement('img');
				pic.id = 'imgpx';
				pic.src = jdata[pinID][0];
				
				ctx.drawImage(pic,jdata[pinID][3],jdata[pinID][4],200,200);
			}
		}
	}
}


//function clickHandle(e){
//	xCoor =  e.offsetX;
//	yCoor = e.offsetY;
//	bool = false;
//	for(pinID in jdata){
//		if(bool == false)
//			for(var i = 0; i < jdata.pinboard.length; i++){
//				pin = jdata.pinboard[i];
//				
//				if(pinID == pin)
//					if(xCoor > jdata[pinID][3] && xCoor < jdata[pinID][3] + 200)
//						if(yCoor > jdata[pinID][4] && yCoor < jdata[pinID][4] + 200){
//							bool = true;
//							movePin = pinID;
//							i = jdata.pinboard.length +1;
//						}
//			}
//	}
//	if(bool == true){
//		$(document).ready(function(){
//			$('#board').on('mousemove',moveIt);
//		})
//	}
//	
//	
//	
//}
//
//function moveIt(e){
//	jdata[movePin][3] = e.clientX - 20;
//	jdata[movePin][4] = e.clientY - 50;
//
//	ctx.clearRect(0,0,856,482);
//	showPinsOnBoard();
//	
//	
//	$(document).ready(function(){
//		$('#board').live('click', unbind);
//	})
//		
//}
//
//function unbind(e){
//	$(document).ready(function(){
//		$('#board').unbind('mousemove');
//		$('#board').live('click', clickHandle);
//		
//		$.ajax('/canvas/' + boardID, {
//			type: "POST",
//			data: {
//				editPinId: jdata[movePin][2],
//				x: jdata[movePin][3],
//				y: jdata[movePin][4],
//			},
//			success: function(data){
//				console.log('update server');
//			}
//		})
//	})
//
//}

function showData(data){
	jdata = data;
	showPinsOnBoard();
}

function handleClick(e){
	boardID = document.getElementById('boardId').innerText;
	link = '/canvas/' + boardID;
	
	$.ajax(link,{
		type: 'GET',
		data: {
			fmt: 'json'
		},
	
		success: showData
	});
	
}


$(document).ready(function(){
	canvas = $('#board')[0];
	ctx = canvas.getContext('2d');
	handleClick();
	$('#board').on('click', clickHandle);
	
})