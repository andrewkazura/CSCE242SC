var jdata;
var num;

function deleteButtonFunction(){
	console.log("remove me " + pinID);
	boardID = document.getElementById('boardId').innerText;
	link = '/board/' + boardID;	
	$.ajax(link,{
		type: 'POST',
		data: {
			deletepin: pinID
		}
	});	
}

function showPinsOnBoard(){
	mainholder = document.getElementById('mainholder');
	for(pinID in jdata){
		for(var i = 0; i < jdata.pinboard.length; i++){
			pin = jdata.pinboard[i];
			if(pinID == pin){
				background = document.createElement('div');
				background.id = 'displaybox';
				
				picid = document.createElement('div');
				picid.innerText = jdata[pinID][2];
				
				pic = document.createElement('img');
				pic.id = 'imgpx';
				pic.src = jdata[pinID][0];
				
				piccap = document.createElement('div');
				piccap.innerText = jdata[pinID][1];
				
				deleteButton = document.createElement('button');
				deleteButton.appendChild(document.createTextNode('Remove' + i));
				deleteButton.i = i;
				deleteButton.innerHTML = "Remove";
				deleteButton.onclick = deleteButtonFunction;
			
				
//				deleteButton.onclick = function(){
//					console.log("remove me " + pinID);
//					boardID = document.getElementById('boardId').innerText;
//					link = '/board/' + boardID;	
//					$.ajax(link,{
//						type: 'POST',
//						data: {
//							deletepin: pinID
//						}
//					});	
//				}
				
				mainholder.appendChild(background);
				background.appendChild(pic);
				background.appendChild(piccap);
				background.appendChild(deleteButton);
			}
		}
	}
}




function showPinsOffBoard(){
	box = document.createElement('div');
	box.style.border = '1px solid black';
	offholder = document.getElementById('offholder');
	
	for(pinID in jdata){
		if(pinID != "pinboard"){
			for(var i = 0; i < jdata.pinboard.length; i++){
				pin = jdata.pinboard[i];
				if(pinID == pin){
					i = jdata.pinboard.length;
				}
				else if(i == jdata.pinboard.length-1){
					
					picid = document.createElement('div');
					picid.innerText = jdata[pinID][2];
					
					pic = document.createElement('img');
					pic.id = 'imgpx2';
					pic.src = jdata[pinID][0];
					
					piccap = document.createElement('div');
					piccap.innerText = jdata[pinID][1];
					
					
					addButton = document.createElement('button');
					addButton.innerHTML = "Add";
					addButton.id = "addButton";
					if (addButton.onclick){
						addButton.onclick = addButtonFunction
						num = jdata[pinID][2];
					}
						
					
//						function addButtonFunction(){
//						console.log("add me");
//						
//						boardID = document.getElementById('boardId').innerText;
//						link = '/board/' + boardID;	
//						$.ajax(link,{
//							type: 'POST',
//							data: {
//								addpin: pinID
//							}
//						});	
//					}
					
					offholder.appendChild(box);
					box.appendChild(pic);
					box.appendChild(piccap);
					box.appendChild(addButton);
				}
			}
		}
		else
			break;
	}	
}

function addButtonFunction(e){
	console.log("add me " + num);
	
	boardID = document.getElementById('boardId').innerText;
	link = '/board/' + boardID;	
	$.ajax(link,{
		type: 'POST',
		data: {
			addpin: num
		}
	});	

}


function showData(data){
	jdata = data;
	showPinsOnBoard();
	showPinsOffBoard();
}



function handleClick(e){
	boardID = document.getElementById('boardId').innerText;
	link = '/board/' + boardID;
	
	$.ajax(link,{
		type: 'GET',
		data: {
			fmt: 'json'
		},
	
		success: showData
	});
	
}


$(document).ready(function(){
	handleClick();
	$('#addButton').live('click', addButtonFunction)
})
