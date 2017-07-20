$(document).ready(function(){
/************************************
*     显示关注列表/粉丝列表
**************************************/
// 粉丝列表
$("#profile_follower_b").click(function(e){
	console.log(e)
	$(this).addClass("selected")
	$("#profile_follower").removeClass("hidden")


	$("#profile_followee_b").removeClass("selected")
	$("#profile_followee").addClass("hidden")

})

// 关注列表
$("#profile_followee_b").click(function(e){
	console.log(e)
	$(this).addClass("selected")
	$("#profile_followee").removeClass("hidden")

	$("#profile_follower_b").removeClass("selected")
	$("#profile_follower").addClass("hidden")

})


/************************************
*     关注功能
*     person.html --> views.foolowS
*     oneQa.html --> views.followS
*     profile.html --> views.unfollowS
**************************************/
$("#person_follow").click(function(e){
	console.log(e)
	entity_id = document.getElementById("person_userId").innerText
	entity_type = "3"

	data = {
		entity_type : entity_type,
		entity_id : entity_id,
	}

	$.post("/QaPlat/followS/",data,function(data1,status){
		// dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	window.location.reload()
	});

})

$("#person_unFollow").click(function(e){
	console.log(e)
	entity_id = document.getElementById("person_userId").innerText
	entity_type = "3"

	data = {
		entity_type : entity_type,
		entity_id : entity_id,
	}

	$.post("/QaPlat/unfollowS/",data,function(data1,status){
		// dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	window.location.reload()
	});

})

$("#followId").click(function(e){
	console.log(e)
	entity_id = $("#qId_input")[0].value
	entity_type = $("#qType_input")[0].value

	data = {
		entity_type : entity_type,
		entity_id : entity_id,
	}

	$.post("/QaPlat/followS/",data,function(data1,status){
		// dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	window.location.reload()
	});

})
$("#unfollowId").click(function(e){
	console.log(e)
	entity_id = $("#qId_input")[0].value
	entity_type = $("#qType_input")[0].value

	data = {
		entity_type : entity_type,
		entity_id : entity_id,
	}

	$.post("/QaPlat/unfollowS/",data,function(data1,status){
		// dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	window.location.reload()
	});

})

// profile.html --> button
$(".unfollowP").click(function(e){
	console.log(e)
	entity_id = $(this).parent().prevAll()[1].children[2].innerText
	entity_type = $(this).parent().prevAll()[1].children[1].innerText

	data = {
		entity_type : entity_type,
		entity_id : entity_id,
	}

	$.post("/QaPlat/unfollowS/",data,function(data1,status){
		// dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	window.location.reload()
	});

})

/************************************
*     赞踩功能
*     message.html --> views.message
*     qa.html      --> views.
**************************************/
$(".dislike").click(function(e){
	console.log(e)
	// $(this).addClass("selected")
	like = "-1"
	entity_id = $(this).nextAll()[0].value
	entity_type = $(this).nextAll()[1].value

	data = {
		like : like,
		entity_type : entity_type,
		entity_id : entity_id,
	}

	dislikeE = $(this)

	$.post("/QaPlat/like/",data,function(data1,status){
		dislikeE.prevAll()[0].innerText = data1
	// alert("评论:" + data1)
	// window.history.back(-1)
	// window.location.reload()
	});
});

$(".like").click(function(e){
	console.log(e)
	// $(this).addClass("selected")
	like = "1"
	entity_id = $(this).nextAll()[2].value
	entity_type = $(this).nextAll()[3].value

	data = {
		like : like,
		entity_type : entity_type,
		entity_id : entity_id,
	}

	likeE = $(this)
	$.post("/QaPlat/like/",data,function(data1,status){
	// alert("评论:" + data1)
	likeE.next()[0].innerText = data1
	// window.history.back(-1)
	// window.location.reload()

	});
});

/************************************
*     展现用户会话信息
*     message.html --> views.message
**************************************/
$(".friendId_sub").click(function(e){
	console.log(e)
	var f = "#" + this.parentElement.id
	$(f).submit()
	// $(this).submit()
	// $("#id_friendId").submit()
});

/************************************
*     站内信
*     message.html --> views.message
**************************************/
$(function (){ // 注意dialog需要外层function包裹
  //注册对话框
  $("#dialogSendMessage").dialog({
   //设置对话框打开的方式 不是自动打开
   autoOpen:false,
   show:"blind",
   hide:"explode",
   modal:true,
   buttons:[
    {
     text:"发送",
     click:function (){
     	friendName = document.getElementById("friendName").value
     	message = document.getElementById("messageArea").value
     	data ={
     		friendName:friendName,
     		content:message,
     		type:"sendM"
     	}

     	$.post("/QaPlat/message/",data,function(data1,status){
     		alert(data1)
     		// $(this).dialog("close");
     		window.location.reload()

     	})

     }

    },{
       text:"取消",
       click:function(){
  			$(this).dialog("close");
        }
     }
    ],
   closeOnEscape:false, //是否esc
   title:"发私信", //对话框标题
   position: {
　　　　　　my: "center",
　　　　　　at: "center",
　　　　　　of: window,
　　　　　　collision: "fit",
　　　　　　// Ensure the titlebar is always visible
　　　　　　using: function( pos ) {
　　　　　　　　var topOffset = $( this ).css( pos ).offset().top;
　　　　　　　　if ( topOffset < 0 ) {
　　　　　　　　　　$( this ).css( "top", pos.top - topOffset );
　　　　　　　　}
　　　　　　}
　　　　},//对话框弹出的位置 top left right center bottom 默认是center
   width:500, //对话框宽度
   height:330, //对话框高度
   resizable:false, //是否可以改变大小操作  默认true
   }); 
  
  //触发连接的事件 当点击连接打开一个对话
  $("#sendMessage").click(function (){
   //open参数 作用：打开对话框
   $("#dialogSendMessage").dialog("open");
  });
 });


/************************************
*  提交评论 
*  oneQa.html --> QaPlat.commentSubmit
**************************************/
$("#buttonComment").click(function(e){
	entity_type = 1
	entity_id = document.getElementById("qId_input").value
	comment = $("#summernote_comment").summernote('code')

	data = {
		entity_id:entity_id,
		entity_type:entity_type,
		comment:comment,
	}
	if(comment=="<p><br></p>"){
		alert("请输入评论内容!")
	}
	else{
		$.post("/QaPlat/commentSubmit/",data,function(data1,status){
			alert("评论:" + data1)
			// window.history.back(-1)
			window.location.reload()

		});
	}
})

$('#summernote_comment').summernote({

   		height: 120,         // set editor height
  		minHeight: null,             // set minimum height of editor
  		maxHeight: null,             // set maximum height of editor
  		focus: true,                  // set focus to editable area after initializing summernote
  		placeholder: "评论内容",
  		align:"left",

});

/************************************
*  发送quetionID用于显示改问题的详细信息 
*  qa.html --> QaPlat.oneQuestion
**************************************/
$(".questionTilte").click(function(e){
	console.log(e)
	qaId = $(this).parent().next().val()
	title = this.innerText
	content = $(this).parent().parent().parent().next().text()
	user_date = $(this).parent().parent().parent().prev().contents().text()
	var o = "#"+qaId
	$(o).submit()
	// $(o).submit(function(e){
	// 	success:function(data){
	// 		getElementById("user_date").innerText=user_date
	// 	    getElementById("one_questions_title").innerText=title
	// 	    getElementById("one_questions_uid").innerText=qaId
	// 	    getElementById("one_questions_content").innerText=content
	// 	}
	// })

	data = {
		"questionId":qaId,
	}

	// $.post("/QaPlat/oneQuestion/",data,function(data1,status){
 //            alert("Data: " + data1 + "\nStatus: " + status);
 //            // window.location.reload()
 //            getElementById("user_date").innerText=user_date
 //            getElementById("one_questions_title").innerText=title
 //            getElementById("one_questions_uid").innerText=qaId
 //            getElementById("one_questions_content").innerText=content
 //    })
});

/************************************
*  question 内容的html标签内容被转义
*  现将转移内容重新改写成html标签
**************************************/
update_content()
function update_content(){
	// alert("in update_content")
	content = document.getElementsByClassName("new_questions_content")
	for(i=0;i<content.length;i++){
		text = content[i].innerText
		content[i].innerHTML = text	
	}
}
/************************************
*     渲染选中行 
*     仅选中渲染
**************************************/
	$(".list-group-item").click(function(e){
		$(this).prevAll().removeClass("active")
		$(this).nextAll().removeClass("active")
		$(this).addClass("active")

		// 选择显示的内容
		if ($(this).attr("id")=="item-gonggao") {
			show=$("#list-item-gonggao")
		}
		if ($(this).attr("id")=="item-biaozhun") {
			show=$("#list-item-biaozhun")
		}
		if ($(this).attr("id")=="item-kejian") {
			show=$("#list-item-kejian")
		}
		if ($(this).attr("id")=="item-zuoye") {
			show=$("#list-item-zuoye")
		}
		if ($(this).attr("id")=="item-taolun") {
			show=$("#list-item-taolun")
		}
		show.removeClass("hidden")
		show.nextAll().addClass("hidden")
		show.prevAll().addClass("hidden")
	});
/************************************
*     发布问题
*     publicQ.html --> views.publicQ
**************************************/
$(function (){ 
   $('#summernote').summernote({

   		height: 300,         // set editor height
  		minHeight: null,             // set minimum height of editor
  		maxHeight: null,             // set maximum height of editor
  		focus: true,                  // set focus to editable area after initializing summernote
  		placeholder: "问题内容",

   });

$('#buttonPublic').click(function(e){

	title = document.getElementById("titlePublic").value
	content=$('#summernote').summernote('code')

	data={
		type:'public',
		title:title,
		content:content,
	}
	// data = JSON.parse(data)
	$.post("/QaPlat/publicQ/",data,function(data1,status){
	    // $(this).dialog("close");
	    if (data1=="success"){
	    	alert("发布成功");
	    	window.history.back(-1)
	    }
	    else{
	    	alert("发布失败");
	    }	
	});

});

});

});
