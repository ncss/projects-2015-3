function onClientLoad() {
    gapi.client.load('youtube', 'v3', onYouTubeApiLoad);
}

// Called automatically when YouTube API interface is loaded
function onYouTubeApiLoad() {
    // This is Willem Hendriks's key
    gapi.client.setApiKey('AIzaSyBJFXpnFUK9dS9x8nBlLHoUvra8U7k_yCo');
    
    var q = $("#search-query").prop("value");
    if ( q != ""){
        search(q);
    }
}

function search(query) {
    // Use the JavaScript client library to create a search.list() API call.
    var request = gapi.client.youtube.search.list({
        q: query,
        part: 'snippet',
        maxResults: 21
    });
    
    // Send the request to the API server,
    // and invoke process() with the response.
    request.execute(process);
}
function process(response){
    var output = '<section>';    
    for (var i = 0; i < response["items"].length; i++) {
        var item = response["items"][i];
        var videoId = item['id']["videoId"];
        var title = item['snippet']['title'];
        var desc = item['snippet']['description'];
        var thumb = item['snippet']['thumbnails']['high']['url'];
        if ((i % 3) == 0){
            output += '<ol class="search-result-white center">';
        }
        if (title.length >= 15){
            title = title.substring(0,15)+' ...';
        }
        output += '<li class="search-result-item video-thumbnail search-result"> <a href=" /view/'+ videoId + '"> <img src="' + thumb + '"><h3>' + title + '</h3></a></li>';
        if ((i + 1) % 3 == 0){
            output += '</ol>';
        }    
    }
    output += '</section>';
    $("#search-results").html(output);
}
$(document).ready(function() {
    
    $("#search-form").on("submit", function(e){
        e.preventDefault();
        search($("#search-query").prop("value"));
    });
 

})