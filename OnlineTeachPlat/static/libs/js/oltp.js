
$(document).ready(function(){
	/************************************
	*     渲染选中行 
	*
	**************************************/
	$("tr.list").click(function(e){
  		$(this).children('td').toggleClass("selected")
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
  	// 取数据
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
