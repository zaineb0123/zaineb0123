$('#likes').click(function(){
    var postId;
    console.log("Ajax is running");
    postId = $(this).attr("data-postId");
    $.get('/like_post/', {post_id : postId}, function(data){
        $('#like_count').html(data);
        $('#likes').hide();
    });
});