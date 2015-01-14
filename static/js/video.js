// All Comments are pretty much by google :P
// This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
var player;
var url = window.location.href;
url = url.split('/');
var viewId = url[url.length-1];

function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
		height: '390',
		width: '640',
		videoId: videoId,
		playerVars: {
			controls : 0
		},
		events: {
			'onReady': onPlayerReady
		}
	});
}

// The API will call this function when the video player is ready.
function onPlayerReady(event) {
	event.target.playVideo();
	// Functions that will run every second to check for the video state
	commentSniffer();
	videoSniffer();
	// Function to start the pulse
	videoIdRetrieve(viewId);
}

var revealInterval = 6;
// Separate Function for the javascripts to run every 1 second excluding the function to show comments.
function videoSniffer(){
    // Automatic Que Play. Basic function that loops every 1 second to check for queued videos (videos that are not streamed) and forces the video to be streamed
	if(player.getPlayerState() == 5){
		player.playVideo();
	}

    $("#timestamp")[0].value = player.getCurrentTime();
    $("#view_id")[0].value = viewId;
    setTimeout(videoSniffer,1000);
}

// Comments handler, loops every 1 second to handle the comments and show them when they appear
function commentSniffer(){
	var commentList = $(".timedComment");
	for (var i = 0; i < commentList.length; i++) {
		commentHandler(commentList[i]);
	}
    if(player.getPlayerState() != 0){
        setTimeout(commentSniffer,1000);
    }
}

function commentHandler(commentElement){
	comment = $(commentElement)
	intTime = parseInt(commentElement.getAttribute("showat"))
    if(Math.floor(player.getCurrentTime()) >= intTime && Math.floor(player.getCurrentTime()) <= (intTime + revealInterval)){
		if(commentElement.style.display == "none" && commentElement.style.opacity == ""){
			comment.fadeIn();
		}
	}
    /*
	else{
		if(commentElement.style.display == "" && commentElement.style.opacity == ""){
			comment.fadeOut();
		}
	}
    */
}

// Change video handler in which the function takes in a string, either containing the youtube url or the direct id of the video
// It then parses the string and load the video with the given.extracted id
function changeVideoHandler(url){
	if(url != ""){
		if(url.indexOf('v=') > -1){
			var video_id = url.split('v=')[1];
			player.cueVideoById(video_id);
		}
		else{
			player.cueVideoById(url);
		}
	}
}

function _TEMP_callVideoChange(){
	givenUrl = document.getElementById("inputUrl");
	changeVideoHandler(givenUrl.value)
}

var videoSweetSpot = 3;

// Retrieve video id
function videoIdRetrieve(){
	$.ajax({
		url : "/pulse/" + viewId + "/" + player.getCurrentTime(),
		success: function(data, status, jqXHR){
            data = $.parseJSON(data);
			if(data['status'] == 'client'){
                if (Math.abs(player.getCurrentTime() - data['elapsed']) > videoSweetSpot){
                    player.seekTo(data['elapsed']);
                }
            }
		}
	});
    if(player.getPlayerState() != 0){
        setTimeout(videoIdRetrieve,1000);
    }
}