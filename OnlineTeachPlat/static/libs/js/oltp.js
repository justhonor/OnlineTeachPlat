
$(document).ready(function(){
	/************************************
	*     渲染选中行 
	*
	**************************************/
	$("tr.list").click(function(e){
  		$(this).children('td').toggleClass("selected")
  	});

/************************************
*     更改用户
*     admin_index.html --> views.admin
**************************************/
$(function (){ // 注意dialog需要外层function包裹
  //注册对话框
  $("#dialog_update").dialog({
   //设置对话框打开的方式 不是自动打开
   autoOpen:false,
   show:"blind",
   hide:"explode",
   modal:true,
   buttons:[
    {
     text:"更改",
     click:function (){
      update_username = document.getElementById("dialog_update_username").innerText;
      update_status = $("input[id=dialog_update_status]").val();
      update_email = $("input[id=dialog_update_email]").val();
      update_group = $("input[id=dialog_update_group]").val();
      update_password = $("input[id=dialog_update_password]").val();

      if(update_status == "" && update_email == "" && update_group =="" && update_password == ""){
        alert("没有修改")
      }
      else{
            data={
                type:"update",
                username:update_username,
                email:update_email,
                password:update_password,
                group:update_group,
                status:update_status
              }
            
             $.post("/oltp/admin/",data,function(data1,status){
                  // $(this).dialog("close");
                  alert("Data: " + data1 + "\nStatus: " + status);
                  $("td").removeClass("selected");
            })
             $(this).dialog("close");
            
      }
    }

    },{
       text:"取消",
       click:function(){
          $(this).dialog("close");
          $("td").removeClass("selected");
        }
     }
    ],
   closeOnEscape:false, //是否esc
   title:"更改信息", //对话框标题
   position:"center",//对话框弹出的位置 top left right center bottom 默认是center
   width:450, //对话框宽度
   height:330, //对话框高度
   resizable:false, //是否可以改变大小操作  默认true
   }); 
  
  //触发连接的事件 当点击连接打开一个对话
  $("#dialog_button_update").click(function (){
   console.log()
   // alert("ddf")
   // 选择选中元素，构造新的html
   update = document.getElementById("dialog_update")
   select = $('.selected')
   var num=$('.selected').length
   if (num == 4){
      update.innerHTML ='\
        <h3 id="dialog_update_username" align="left">'+select[0].innerText+'</h3> \
        <div class="input-group"> \
          <span class="input-group-addon" id="sizing-addon2">邮箱</span>\
          <input id="dialog_update_email" type="text" class="form-control" placeholder='+select[1].innerText+' aria-describedby="sizing-addon2" >\
          <span class="input-group-addon" id="sizing-addon2">状态</span>\
          <input id="dialog_update_status" type="text" class="form-control" placeholder='+select[2].innerText+' aria-describedby="sizing-addon2">\
        </div>\
        <div class="input-group"> \
          <span class="input-group-addon" id="sizing-addon2">分组</span>\
          <input id="dialog_update_group" type="text" class="form-control" placeholder='+select[3].innerText+' aria-describedby="sizing-addon2" >\
          <span class="input-group-addon" id="sizing-addon2">密码</span>\
          <input id="dialog_update_password" type="text" class="form-control" placeholder=****** aria-describedby="sizing-addon2">\
        </div>';
    // open参数 作用：打开对话框
    $("#dialog_update").dialog("open");
   }
   else{
        alert("请选择一行数据进行修改")
   }
   
  });
 });

/************************************
*     新增用户
*     admin_index.html --> views.admin
**************************************/
$(function (){ // 注意dialog需要外层function包裹
  //注册对话框
  $("#dialog").dialog({
   //设置对话框打开的方式 不是自动打开
   autoOpen:false,
   show:"blind",
   hide:"explode",
   modal:true,
   buttons:[
    {
     text:"添加",
     click:function (){
      
      //获取姓名
      var dia_username=$("input[id=dia_username]").val();
      //获取邮箱
      var dia_email=$("input[id=dia_email]").val();
      //获取密码
      var dia_password=$("input[id=dia_password]").val();
      //获取类型
      var dia_student=$("input[id=dia_student]:checked").val();
      var dia_teacher=$("input[id=dia_teacher]:checked").val();
      //状态
      var status = "True"
	    var group = ""
      if (dia_student)
      {group = "学生"}
  	  else if(dia_teacher)
  	  {group = "老师"}
  	  else{group = "null"}
      
      data={
      	type:"add",
      	username:dia_username,
      	email:dia_email,
      	password:dia_password,
      	group:group
      }

	    $.post("/oltp/admin/",data,function(data1,status){
	    		// $(this).dialog("close");
	   	  		alert("Data: " + data1 + "\nStatus: " + status);
		})

		$(this).dialog("close");
    }

    },{
       text:"取消",
       click:function(){
        $(this).dialog("close");
        }
     }
    ],
   closeOnEscape:false, //是否esc
   title:"添加用户操作界面", //对话框标题
   position:"center",//对话框弹出的位置 top left right center bottom 默认是center
   width:500, //对话框宽度
   height:330, //对话框高度
   resizable:false, //是否可以改变大小操作  默认true
   }); 
  
  //触发连接的事件 当点击连接打开一个对话
  $("#dialog_link").click(function (){
   //open参数 作用：打开对话框
   $("#dialog").dialog("open");
  });
 });

/************************************
*     删除选中的用户
*     admin_index.html --> views.admin
**************************************/

  $("#id_delete").click(function(e){
  	// console.log(e);
  	$('td').nextAll('.selected').parent().hide()

  	var num=$('.selected').length
  	var j=0;

  	var data = {type:"delete"};
  	var str  = ""
  	var sp = ","
  	// 取数据,依赖于每行有4列来取每行首列
  	for (var i=0;i<num;i=i+4)
  	{
  		a = $(".selected:eq("+i+")").text()
  		j = j + 1;
  		num = num - 1;
  		str = str.concat(a).concat(sp)
  		// data[j] = $(".selected:eq("+i+")").text()
  	}
  	data["usernames"] = str

  	// console.log(str)
  	// console.log(data)
	// 后台删
	$.post("/oltp/admin/",data,function(data1,status){
		alert("Data: " + data1 + "\nStatus: " + status);
	})

  });

});
