var jdata;
var privateboard;
var sameOwner;

function deleteButtonHandler(e){
	console.log($(this).attr('id'));
	boardID = document.getElementById('boardId').innerText;
	link = '/board/' + boardID;	
	$.ajax(link,{
		type: 'POST',
		data: {
			deletepin: $(this).attr('id')
		}
	});	
	
	offholder.appendChild(document.getElementById($(this).attr('id')));
	$(this)[0].innerHTML = "Add";
}

function showPinsOnBoard(){
	mainholder = document.getElementById('mainholder');
	for(pinID in jdata){
		for(var i = 0; i < jdata.pinboard.length; i++){
			pin = jdata.pinboard[i];
			if(pinID == pin){
				background = document.createElement('div');
				background.id = pinID;
				
				background.style.marginLeft = 'auto';
				background.style.marginRight = 'auto';
				background.style.width = '285px';
				background.style.backgroundColor = '#fee';
				background.style.padding = '10px';
				
				picid = document.createElement('div');
				picid.innerText = jdata[pinID][2];
				
				pic = document.createElement('img');
				pic.id = 'imgpx';
				pic.src = jdata[pinID][0];
				
				piccap = document.createElement('div');
				piccap.innerText = jdata[pinID][1];
				
				deleteButton = document.createElement('button');
				deleteButton.innerHTML = "Remove";
				deleteButton.id = jdata[pinID][2];
			
				
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
				if(pinID == pin || pinID == "pinboard"){
					i = jdata.pinboard.length;
				}
				else if(i == jdata.pinboard.length-1){
					background = document.createElement('div');
					background.id = pinID;
					
					background.style.marginLeft = 'auto';
					background.style.marginRight = 'auto';
					background.style.width = '285px';
					background.style.backgroundColor = '#fee';
					background.style.padding = '10px';
						
					
					picid = document.createElement('div');
					picid.innerText = jdata[pinID][2];
					
					pic = document.createElement('img');
					pic.id = 'imgpx';
					pic.src = jdata[pinID][0];
					
					piccap = document.createElement('div');
					piccap.innerText = jdata[pinID][1];
					

					addButton = document.createElement('button');
					addButton.innerHTML = "Add";
					addButton.id = jdata[pinID][2];
					addButton.imgsrc = jdata[pinID][0];
					addButton.cap = jdata[pinID][1];
					
					offholder.appendChild(background);
					background.appendChild(pic);
					background.appendChild(piccap);
					background.appendChild(addButton);
				
				}
			}
		}
		else
			break;
	}	
	if(jdata.pinboard.length == 0){
		for(pinID in jdata){
			if(pinID != "pinboard"){
				background = document.createElement('div');
				background.id = pinID;
				
				background.style.marginLeft = 'auto';
				background.style.marginRight = 'auto';
				background.style.width = '285px';
				background.style.backgroundColor = '#fee';
				background.style.padding = '10px';
					
				
				picid = document.createElement('div');
				picid.innerText = jdata[pinID][2];
				
				pic = document.createElement('img');
				pic.id = 'imgpx';
				pic.src = jdata[pinID][0];
				
				piccap = document.createElement('div');
				piccap.innerText = jdata[pinID][1];
				

				addButton = document.createElement('button');
				addButton.innerHTML = "Add";
				addButton.id = jdata[pinID][2];
				addButton.imgsrc = jdata[pinID][0];
				addButton.cap = jdata[pinID][1];
				
				offholder.appendChild(background);
				background.appendChild(pic);
				background.appendChild(piccap);
				background.appendChild(addButton);
			}
			else
				break;
		}
		
	}
		
}

function addButtonHandler(e){
	
	boardID = document.getElementById('boardId').innerText;
	link = '/board/' + boardID;	
	$.ajax(link,{
		type: 'POST',
		data: {
			addpin: $(this).attr('id')
		}
	});	
		
	mainholder.appendChild(document.getElementById($(this).attr('id')));
	$(this)[0].innerHTML = "Remove";
	

}

function showPrivateButton(){
	middle = document.getElementById('middle');
	
	text = document.createElement('text');
	text.innerText = "Private ";
	
	privButton = document.createElement('button');
	privButton.value = privateboard;
	if(privButton.value == "on")
		privButton.innerText = "on";
	else
		privButton.innerText = "off";	
	
	middle.appendChild(text);
	middle.appendChild(privButton);
}


function privateButtonHandler(e){
	if(privateboard == "")
		privateboard = "on";
	else
		privateboard = "";

	privButton.value = privateboard;
	if(privButton.value == "on")
		privButton.innerText = "on";
	else
		privButton.innerText = "off";	
	
	
	link = '/board/' + boardID;	
	$.ajax(link,{
		type: 'POST',
		data: {
			boardprivate: privateboard
		}
	});	
}


function showData(data){
	jdata = data;
	privateboard = jdata.boardprivate;
	showPrivateButton();
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
	$('#offholder').on('click', 'button', addButtonHandler)
	$('#mainholder').on('click', 'button', deleteButtonHandler)
	$('#middle').on('click', 'button', privateButtonHandler)
})
