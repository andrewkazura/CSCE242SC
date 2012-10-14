var images=new Array();

function getImages(){
	var links = new Array();
	var img;
	images = document.getElementsByTagName('img');
	
	for(var i=0; i<images.length; i++){
		img = images[i];
		if(img.getAttribute('src').indexOf("http") != -1)
		{
			links[i] = img.getAttribute('src');
		}
		else
		{
			links[i] = "http://" + location.host + img.getAttribute('src');
		}
		
	}
	
	return links;
}


images = getImages();

document.body.innerHTML = '';
document.head.innerHTML = '';

var body = document.createElement("body");
document.body = body;

var header = document.createElement('h1');
header.innerText = "Pinboard";
body.appendChild(header);


var information = document.createElement('l1');
information.innerText = "Pick which one of these images you want to add:"
body.appendChild(information);


br = document.createElement('br');
body.appendChild(br);


	for(j=0; j<images.length; j++){

		var picdiv = document.createElement('div');
		picdiv.style.border = '3px solid black';
		picdiv.style.width = '220px';
		picdiv.style.height = '180px';
		picdiv.style.padding = '20px';
		var picform = document.createElement('form');
		document.forms = picform;
		
		var i = document.createElement('img');
		i.src = images[j];
		i.style.width = '200px';
		i.style.height = '120px';
		body.appendChild(i);		

		
		chosenpic = document.createElement('input');
		chosenpic.value = "This One";
		chosenpic.type = "submit";
		caption = document.createElement('input');
		caption.type = "text";
		caption.name = "caption";
		imgUrl = document.createElement('input');
		imgUrl.type = "text";
		imgUrl.value = images[j];
		imgUrl.name = "imgUrl";
		imgUrl.hidden = "true";
		

		br = document.createElement('br');
		picdiv.appendChild(br);
		picdiv.appendChild(i);
		body.appendChild(picdiv);
		
		captionWord = document.createElement('l1');
		captionWord.innerText = "Caption: ";
		picform.appendChild(captionWord);
		picform.appendChild(caption);
		picform.appendChild(chosenpic);
		picform.appendChild(imgUrl);
		picdiv.appendChild(picform);
	

		picform.action = "http://csce242helloworld.appspot.com/";
		picform.method = "post";	
		
		body.appendChild(br);
		
	}


