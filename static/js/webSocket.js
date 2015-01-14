var ws = new WebSocket("ws://" + base_url + ":8888/comment/new");

ws.onmessage = function (evt) {
    data = JSON.parse(evt.data);
    var elem = '<article class="timedComment video-comment cf" showAt="' + parseInt(data["timestamp"]) + '" style="display:none;">'+
                    '<p class="video-comment-text">' + data["comment"] + '</p>'+
                    '<h3 class="video-comment-author">' + data["user_name"] + '</h3>'+
                    '<time datetime="' + data["time"] + '" pubdate class="video-comment-time">' +
                        'Posted ' + parseInt(data["timestamp"]) + ' seconds into the video' +
                    '</time>' +
                '</article>';
    $(".video-comments").prepend(elem);
};

function sendCommentData(){
    var commentData = {
        "video_id" : $("#video_id")[0].value,
        "view_id" : viewId,
        "comment" : $(".video-comment-textarea")[0].value,
        "timestamp" : player.getCurrentTime()
    };
    var mainData = JSON.stringify(commentData);
    
    $(".video-comment-textarea").val("");
    ws.send(mainData);
}