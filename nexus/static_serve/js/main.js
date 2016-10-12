// Foundation
$(document).foundation();


$(document).ready(function(){
    // Add hub selectors to each post.
    $(".hub-selector").each(function(){
	$(this).find("#id_hubs").select2({
	    placeholder: "select hubs",
	    allowClear: true,
	    maximumSelectionLength: 3
	})
    });
    $('.reply-editor').hide()

    // Editor
    $('textarea').each(function() {
	simplemde = new SimpleMDE({
	    element: this,
	    toolbar: [],
	    placeholder: "Write something insightful here... \n(can use markdown)",
	});
	simplemde.render();
    });      
    
    // Set reply form action to it's parent's id.
    $(".reply-editor").each(function(){
	var postid = 	$(this).parent().find("article").attr('id');
	// console.log(postid);
	$(this).find("form").attr('action', "/reply/"+postid);
	
    });


    //Open reply editor
    $('.reply').click(function () {
	console.log("reply!");
	$('.reply-editor').hide()
	$(this).parent().parent().parent().parent().parent().find('.reply-editor').toggle();
	// $(this).parent().parent().parent().find('.comment-reply').toggle();a
    });




});
