$(document).ready(function(){
    $('#blog_area').attr({ cols:"75",rows:"15"});
    $('#new_comment').hide();
    $('#new_discuss').hide();
    $('#id_title').attr({size:"50",placeholder:"Title"});
    $('#id_blog_content').attr({ cols:"75",rows:"15",placeholder:"Write"});

    $('#edit_lang').click(function(event){
      var language=$('input[name="language"]:checked').val();
      $.ajax({
      type: "GET",
      url: "/nblik/edit_language/",
      data: {language: language},
      success: function(data){
        if(data=='Done')
        {
          alert('Done!');
        }
      }
    });
    event.stopImmediatePropagation();
    });

    $('#id_title').change(function(){
        var blog_title=$('#id_title').val();
        $.ajax({
    type:"GET",
    url: "/nblik/blog_title/",
    data: {blog_title: blog_title},
    success: function(newData){
        if(newData=="error")
        {
            $('#id_title').val("");
            alert("Blog Already Exists!");
        }
    }
    });
    });

    $('#new_discuss_topic').change(function(){
        var discussion_topic=$('#new_discuss_topic').val();
        $.ajax({
    type:"GET",
    url: "/nblik/discussion_topic/",
    data: {discussion_topic: discussion_topic},
    success: function(newData){
        if(newData=="error")
        {
            $('#new_discuss_topic').val("");
            alert("This Discussion Already Exists!");
        }
    }
    });
    });

    $('#category_like').click(function(event){
      $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
		var cat_id;
		cat_id = $(this).attr("data-catid");
    liked=$(this).attr('liked');
    ele=$(this);
    if(liked=='no')
    {
		$.get('/nblik/like_category/',{category_id: cat_id},function(data){
		    $('#category_like_count').html(data);
		    ele.attr('liked','yes');
        ele.html('Unlike');
        console.log('yo yo');
			});
    }
    else
    {
      $.get('/nblik/unlike_category/',{category_id: cat_id},function(data){
        $('#category_like_count').html(data);
        ele.attr("liked","no");
        ele.html('<span class="glyphicon glyphicon-thumbs-up"> </span> Like');
        console.log('yo');
      });
    }
    event.stopImmediatePropagation();
    });

	$('.blog_like').click(function(event){
    //console.log("Hello");
    $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
		var blog_id;
		blog_id = $(this).attr("data-blogid");
    blog_liked=$(this).attr("liked");
    blog=$(this);
    if(blog_liked=='no')
    {
		$.get('/nblik/like_blog/',{blog_id: blog_id},function(data){
		    $('#'+blog_id).html(data);
		    blog.html("Unlike");
        blog.attr("liked","yes");
        //console.log('yo');
			});
    }
    else
    {
      $.get('/nblik/unlike_blog/',{blog_id: blog_id},function(data){
        $('#'+blog_id).html(data);
        blog.html('<span class="glyphicon glyphicon-thumbs-up"> </span> Like');
        blog.attr("liked","no");
        //console.log('yo yo');
      });
    }
    event.stopImmediatePropagation();
    });

$(".comment-lyk").click(function(event){
  $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
    //console.log("Hello");
    var comment_id;
    comment_id = $(this).attr("data-blogid");
    liked=$(this).attr('liked');
    var ele=$(this);
    if(liked=='no')
    {
    $.get('/nblik/like_comment/',{comment_id: comment_id},function(data){
        ele.attr("liked","yes");
        ele.html("Unlike");
        $('#'+comment_id).html(data);
      });
    }
    else
    {
      $.get('/nblik/unlike_comment/',{comment_id: comment_id},function(data){
        ele.attr("liked","no");
        ele.html('<span class="glyphicon glyphicon-thumbs-up"> </span> Like');
        $('#'+comment_id).html(data);
      });
    }
    event.stopImmediatePropagation();
    });

$('#discussion_like').click(function(event){
  $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
    //console.log("Hello");
    var discussion_id;
    discussion_id = $(this).attr("data-blogid");
    liked=$(this).attr("liked");
    discussion=$(this);
    if(liked=='no')
    {
    $.get('/nblik/like_discussion/',{discussion_id: discussion_id},function(data){
        //console.log(data);
        $('#discussion_like_count').html(data);
        discussion.html('Unlike');
        discussion.attr("liked","yes");
      });
    }
    else
    {
      $.get('/nblik/unlike_discussion/',{discussion_id: discussion_id},function(data){
        //console.log(data);
        $('#discussion_like_count').html(data);
        discussion.html('<span class="glyphicon glyphicon-thumbs-up"> </span> Like');
        discussion.attr("liked","no");
    });
    }
    event.stopImmediatePropagation();
    });

$(".discuss-lyk").click(function(event){
  $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
    //console.log("Hello");
    var discuss_id;
    discuss_id = $(this).attr("data-blogid");
    liked=$(this).attr('liked');
    var ele=$(this);
    if(liked=='no')
    {
    $.get('/nblik/like_discuss/',{discuss_id: discuss_id},function(data){
        ele.attr("liked","yes");
        ele.html("Unlike");
        $('#'+discuss_id).html(data);
      });
    }
    else
    {
      $.get('/nblik/unlike_discuss/',{discuss_id: discuss_id},function(data){
        ele.attr("liked","no");
        ele.html('<span class="glyphicon glyphicon-thumbs-up"> </span> Like');
        $('#'+discuss_id).html(data);
      });
    }
    event.stopImmediatePropagation();
    });

	$('#suggestion_id').keyup(function(){
    //console.log("Hello");
		var startswith;
		startswith = $(this).val();
		$.get('/nblik/suggest_category/',{query_string: startswith},function(data){
		    $('#cats').html(data);
		});
	});

  $('#suggestion_search').keyup(function(event){
    //alert('Hello');
    var search_term;
    search_term=$(this).val();
    if(search_term=="")
    {
      $('#search_results').html("");
    }
    else
    { $.ajax({
    type:"GET",
    url: "/nblik/search_top/",
    data: {query_string: search_term},
    success: function(newData){
        $('#search_results').html(newData);
    }
            });
    }
  });

  /*$('#search_results').focusout(function(event){
    $('#search_results').html("");
    $('#suggestion_search').val("");
  });*/

  $("#delete_dialog").click(function(event){
        $("#delete").toggleClass("show");
        });
        $('#no').click(function(event){
            event.preventDefault();
            $('#delete').toggleClass("show");
        });


  $('#comment').click(function(){
    var user_id,blog_id;
    user_id = $(this).attr("data-uid");
    blog_id = $(this).attr("data-blogid");
    up_name=$(this).attr("data-uname");
    comment_text=$('#comment_text').val().replace(/\r\n|\r|\n/g,"<br />");
    $.get('/nblik/comment/',{user_id: user_id,blog_id:blog_id,comment_text:comment_text},function(newdata){
      $('<div class="list-group-item" style="width:75%"><h4 class="list-group-item-heading" id="new_comment_by" >'+up_name+'</h4><p class="list-group-item-text" id="new_comment_text" >'+comment_text+'</p><br /><p style="color:gray;"><font color="black" id="new_comment_like">'+newdata+'</font> like(s)</p></div>').appendTo("#wrapper");
      /*$('#new_comment_like').html(data);
      $('#new_comment_text').html(comment_text);
      $('#new_comment_by').html(up_name);
      $('#new_comment').show();*/
      });
  });

  $('#discuss').click(function(){
    var user_id,blog_id;
    up_name=$(this).attr('data-upname');
    user_id = $(this).attr("data-upid");
    discussion_id = $(this).attr("data-discussionid");
    discuss_text=$('#discuss_text').val().replace(/\r\n|\r|\n/g,"<br />");
    $.get('/nblik/discuss/',{user_id:user_id,discussion_id:discussion_id,discuss_text:discuss_text},function(data){
      $('<div class="list-group-item" style="width:75%;"><h4 class="list-group-item-heading" id="new_discuss_by" > '+up_name+'</h4><p class="list-group-item-text" id="new_discuss_text" >'+discuss_text+'</p><br /><p style="color:gray;"><font color="black" id="new_discuss_like">'+data+'</font> like(s)</p></div>').appendTo('#wrapper');
      /*$('#new_discuss_like').html(data);
      $('#new_discuss_text').html(discuss_text);
      $('#new_discuss_by').html(up_name);
        $('#new_discuss').show();*/
      });
  });

  $('#quick_add_blog').click(function(){
    var blog_text = $('#quick_blog_text').val();
    window.open("/nblik/none/add_blog/","_self");
    $('#blog_area').html(blog_text);
  });

  $('#select-category').change(function(){
    var cat_slug = $('#select-category').val();
    var url= "/nblik/"+ cat_slug + "/add_blog/" ;
    $('#blog_form2').attr("action",url);
  });

  $('#profile_edit').click(function(event) {
  	event.preventDefault();
    var all_div=$('div');
    all_div.css("opacity",".7");
    all_div.click(function(event){event.preventDefault();});
    all_div.keydown(function(event){event.preventDefault();});
    $('#profile_data').css({"opacity":"1","height":"480px","z-index":"5"});
    $.ajax({
    type:"GET",
    url: "/nblik/add_propic/",
    data: {},
    success: function(newData){
        $('#profile_data').html(newData);
    }
    });
  	});

  $('li[data-id]').click(function()
  {
    var data_id=$(this).attr("data-id");
    $('div[id^="d"]').css({"z-index":"-2","visibility":"hidden"});
    $("#d"+data_id).css({"z-index":"6","visibility":"visible"});
    $('li[data-id').css({"color":"white","background":"rgb(70,94,170)"});
    $(this).css({"color":"rgb(28,56,110)","background":"white"});
  });
  $('.text_div').click(function(event)
  {
    $(this).toggleClass('active_text');
    blog_id=$(this).attr("data-blogid");
    $.get('/nblik/viewed/',{blog_id: blog_id},function(data){
        $('#'+blog_id+'_views').html(data);
      });
    event.stopImmediatePropagation();
  });


  $('#edit_language').click(function(event){
      $('#language_id').toggleClass("language1");
      $('#language_id').toggleClass("language2");
      event.stopImmediatePropagation();
    });
});

  $('.unfollow_user').click(function(event){
    $(this).html('<span class="glyphicon glyphicon-time" style="margin-left:7px;margin-right:7px;" aria-hidden="true"></span>');
    var user_id;
    user_id = $(this).attr("data-userid");
    ele=$(this);
    $.get('/nblik/unfollow_user/',{user_id: user_id},function(data){
        ele.hide();
        $('#follow_data').html("Following ("+data+")");
        $("#follow_"+user_id).hide();
      });
    event.stopImmediatePropagation();
    });