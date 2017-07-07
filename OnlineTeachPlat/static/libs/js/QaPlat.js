$(document).ready(function(){
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
	   	
	   	
	})
});

});

});
