$( document ).ready(function() {
    // $("comment-edit-form").hide()
$('.edit-comment-button').on('click', function(e) {
    e.preventDefault();
    console.log("show");
    $(this).parent().parent().parent().find(".comment-edit-form").toggle('display');
});

$('.new-comment-button').on('click', function(e) {
    e.preventDefault();
    console.log("show");
    $(this).parent().parent().parent().find(".new-comment-form").toggle('display');
});


});
