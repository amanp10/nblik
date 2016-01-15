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
        console.log(blog_title);
        $.ajax({
    type:"GET",
    url: "/nblik/blog_title/",
    data: {blog_title: blog_title},
    success: function(newData){
      console.log(newData);
        if(newData=="error")
        {
            $('#id_title').val("");
            alert("Blog Already Exists!");
        }
    }
    });
    });

    $('#hide_write').click(function(event){
      event.preventDefault();
      alert("You need to login first!");
    });

    $('#new_discuss_topic').change(function(){
        var discussion_topic=$('#new_discuss_topic').val();
        console.log(discussion_topic);
        $.ajax({
    type:"GET",
    url: "/nblik/discussion_topic/",
    data: {discussion_topic: discussion_topic},
    success: function(newData){
      console.log(newData);
        if(newData=="error")
        {
            $('#new_discuss_topic').val("");
            alert("This Discussion Already Exists!");
        }
    }
    });
    });

    $('#category_like').click(function(){
		var cat_id;
		cat_id = $(this).attr("data-catid");
		$.get('/nblik/like_category/',{category_id: cat_id},function(data){
		    $('#category_like_count').html(data);
		    $('#category_like').hide();
			});
    });

	$('.blog_like').click(function(){
    //console.log("Hello");
		var blog_id;
		blog_id = $(this).attr("data-blogid");
    blog=$(this);
		$.get('/nblik/like_blog/',{blog_id: blog_id},function(data){
		    $('#'+blog_id).html(data);
		    blog.hide();
			});
    });

$(".comment-lyk").click(function(event){
    //console.log("Hello");
    var comment_id;
    comment_id = $(this).attr("data-blogid");
    var ele=$(this);
    $.get('/nblik/like_comment/',{comment_id: comment_id},function(data){
        ele.hide();
        $('#'+comment_id).html(data);
      });
    });

$('#discussion_like').click(function(){
    //console.log("Hello");
    var discussion_id;
    discussion_id = $(this).attr("data-blogid");
    $.get('/nblik/like_discussion/',{discussion_id: discussion_id},function(data){
        //console.log(data);
        $('#discussion_like_count').html(data);
        $('#discussion_like').hide();
      });
    });

$(".discuss-lyk").click(function(event){
    //console.log("Hello");
    var discuss_id;
    discuss_id = $(this).attr("data-blogid");
    var ele=$(this);
    $.get('/nblik/like_discuss/',{discuss_id: discuss_id},function(data){
        //console.log(data);
        $('#'+discuss_id).html(data);
        ele.hide();
      });
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
        console.log(newData);
        $('#search_results').html(newData);
    }
            });
    }
  });

  $('#suggestion_search').blur(function(event){
    $('#search_results').html("");
    $('#suggestion_search').val("");
  });

  $('.follow_user').click(function(event){
		var user_id;
		user_id = $(this).attr("data-userprofileid");
		$.get('/nblik/follow_user/',{user_id: user_id},function(data){
		    $("#"+user_id).hide();
			});
    });

  $('#comment').click(function(){
    var user_id,blog_id;
    user_id = $(this).attr("data-uid");
    blog_id = $(this).attr("data-blogid");
    up_name=$(this).attr("data-uname");
    console.log("up_name");
    comment_text=$('#comment_text').val();
    $.get('/nblik/comment/',{user_id: user_id,blog_id:blog_id,comment_text:comment_text},function(newdata){
      $('<div class="list-group-item"><h4 class="list-group-item-heading" id="new_comment_by" >'+up_name+'</h4><p class="list-group-item-text" id="new_comment_text" >'+comment_text+'</p><br /><p style="color:gray;"><font color="black" id="new_comment_like">'+newdata+'</font> like(s)</p></div>').appendTo("#wrapper");
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
    discuss_text=$('#discuss_text').val();
    $.get('/nblik/discuss/',{user_id:user_id,discussion_id:discussion_id,discuss_text:discuss_text},function(data){
      $('<div class="list-group-item"><h4 class="list-group-item-heading" id="new_discuss_by" > '+up_name+'</h4><p class="list-group-item-text" id="new_discuss_text" >'+discuss_text+'</p><br /><p style="color:gray;"><font color="black" id="new_discuss_like">'+data+'</font> like(s)</p></div>').appendTo('#wrapper');
      /*$('#new_discuss_like').html(data);
      $('#new_discuss_text').html(discuss_text);
      $('#new_discuss_by').html(up_name);
        $('#new_discuss').show();*/
      });
  });

  $('#quick_add_blog').click(function(){
    console.log('Hello');
    var blog_text = $('#quick_blog_text').val();
    console.log(blog_text);
    window.open("/nblik/none/add_blog/","_self");
    console.log('Hello1');
    $('#blog_area').html(blog_text);
  });

  $('#select-category').change(function(){
    var cat_slug = $('#select-category').val();
    console.log('Hello');
    var url= "/nblik/"+ cat_slug + "/add_blog/" ;
    $('#blog_form2').attr("action",url);
  });

  $('.skip').click(function(event){
    var user_id;
    user_id = $(this).attr("data-userprofileid");
    $("#"+user_id).hide();
    });

  $('#profile_edit').click(function() {
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
        console.log(newData);
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
  });
  $('.discuss_topic').click(function(event){
    event.preventDefault();
    alert("You need to log in first!");
  });
});

  $('#edit_language').click(function(event){
      $('#language_id').toggleClass("language1");
      $('#language_id').toggleClass("language2");
      event.stopImmediatePropagation();
    });