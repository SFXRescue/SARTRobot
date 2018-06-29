/*###########################################################
# Created by the Semi Autonomous Rescue Team				#
#															#
# Author: Jack Williams										#
# Contributors: Jack Williams								#
#															#
# Licensed under GNU General Public License 3.0				#
###########################################################*/

//A collection of random scripts that didn't really deserve their own file. If they are expanded upon they should be moved to their own scriptname.js.

var ip = window.location.hostname;

var text2SpeechSocket = new WebSocket("ws://" + ip + ":5554");
var speech2TextSocket = new WebSocket("ws://" + ip + ":5553");

function readAudio() {
	text2SpeechSocket.onmessage = function(event){
	$(".micLogScroller").prepend(event.data + "<br>");
	}
}

function recordAudio() {
	text2SpeechSocket.send("s");
}

function playAudio() {
	var message = document.getElementById("text2speech").value;
	text2SpeechSocket.send(message);
}

function refreshStream() {
	document.getElementById('streamImage').src += '';
}

function refreshSSH() {
	document.getElementById('sshiframe').src += '';
}

//Need to get the IP of the device rather than using a static string
function snapshotStream() {
	$.get("http://" + ip + ":8080/0/action/snapshot");
	
	setTimeout(function()  {
		window.open("/downloadsnapshot.php");
	}, 2000);
}

//Need to get the IP of the device rather than using a static string
function recordStreamEvent() {
	$.get("http://" + ip + ":8080/0/action/makemovie");
}

var streamFlipped = false;

function flipStream() {
	var streamFlipX = document.getElementById("streamImage");
	var streamFlipY = document.getElementById("flipY")
	
	if(streamFlipped == false){
		streamFlipX.style.transform = "rotatex(180deg)";
		streamFlipX.style.transitionDuration = "0.5s"
		streamFlipY.style.transform = "rotatey(180deg)";
		streamFlipY.style.transitionDuration = "0.5s"
		streamFlipped = true;
	}
	else{
		streamFlipX.style.transform = "rotatex(0deg)";
		streamFlipX.style.transitionDuration = "0.5s"
		streamFlipY.style.transform = "rotatex(0deg)";
		streamFlipY.style.transitionDuration = "0.5s"
		streamFlipped = false;
	}
}

DragDrop.bind(sshModal, {
    anchor: sshDrag
});

DragDrop.bind(irModal, {
    anchor: irDrag
});

DragDrop.bind(streamModal, {
    anchor: streamDrag
});

DragDrop.bind(rawdataModal, {
    anchor: rawdataDrag
});

DragDrop.bind(logModal, {
    anchor: logDrag
});

DragDrop.bind(audioModal, {
    anchor: audioDrag
});

$('.top').click(function() {
   $(this).siblings('.top').css('z-index', 10);
   $(this).css('z-index', 11);
});