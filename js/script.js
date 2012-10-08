

link = document.getElementById('bookmarklet');
link.href = "javascript:(function(){ _my_script=document.createElement('SCRIPT');_my_script.type='text/javascript';_my_script.src='http://" 
+ location.host + "/js/bookmarklet.js?x='+(Math.random());document.getElementsByTagName('head')[0].appendChild(_my_script);})();"

