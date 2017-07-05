
$(document).ready(function(){
	/************************************
	*     渲染选中行 
	*
	**************************************/
	$("tr.list").click(function(e){
  		$(this).children('td').toggleClass("selected")
  	});

/************************************
*     课程通过
*     ClassReview.html --> views.review
**************************************/
$("#class_button_pass").click(function(e){
    // console.log(e);

    select = $('.selected')
    var num=$('.selected').length
    if (num>3){
            // $('td').nextAll('.selected').parent().hide()

            var num=$('.selected').length
            var j=0;

            var data = {type:"pass"};
            var str  = ""
            var sp = ","
            // 取数据,依赖于每行有4列来取每行首列
            for (var i=1;i<num;i=i+5)
            {
              a = $(".selected:eq("+i+")").text()
              j = j + 1;
              num = num - 1;
              str = str.concat(a).concat(sp)
              // data[j] = $(".selected:eq("+i+")").text()
            }
            data["class_ids"] = str

          // console.log(str)
          // console.log(data)
          // 后台删
          $.post("/oltp/admin/review/",data,function(data1,status){
            alert("Data: " + data1 + "\nStatus: " + status);
            window.location.reload()
          })
        }
        else{
            alert("请选择至少选择一行数据") 
        }
    });

/************************************
*     课程拒绝
*     ClassReview.html --> views.review
**************************************/
$("#class_button_reject").click(function(e){
    // console.log(e);

    select = $('.selected')
    var num=$('.selected').length
    if (num>3){
            // $('td').nextAll('.selected').parent().hide()

            var num=$('.selected').length
            var j=0;

            var data = {type:"delete"};
            var str  = ""
            var sp = ","
            // 取数据,依赖于每行有4列来取每行首列
            for (var i=1;i<num;i=i+5)
            {
              a = $(".selected:eq("+i+")").text()
              j = j + 1;
              num = num - 1;
              str = str.concat(a).concat(sp)
              // data[j] = $(".selected:eq("+i+")").text()
            }
            data["class_ids"] = str

          // console.log(str)
          // console.log(data)
          // 后台删
          $.post("/oltp/admin/review/",data,function(data1,status){
            alert("Data: " + data1 + "\nStatus: " + status);
            window.location.reload()
          })
        }
        else{
            alert("请选择至少选择一行数据") 
        }
    });

/************************************
*     查找上一页
*     admin_index.html --> views.admin
**************************************/
$("#PreviousPage").click(function(e){
  // alert("nextpage");
  // 找到最后显示的用户名
  FirstUser = $("tr.list:first").children().first().text()
  document.getElementById("id_reference_user").value = FirstUser
  document.getElementById("id_type").value = "previous"
  
  $("#id_postData").submit()

});

/************************************
*     查找下一页
*     admin_index.html --> views.admin
**************************************/
$("#NextPage").click(function(e){
  // alert("nextpage");
  // 找到最后显示的用户名
  LastUser = $("tr.list:last").children().first().text()
  document.getElementById("id_reference_user").value = LastUser
  document.getElementById("id_type").value = "next"
  
  $("#id_postData").submit()

});

/************************************
*     查找用户信息
*     admin_index.html --> views.admin
**************************************/
$("#modal_button_search").click('shown',function(e){
    // 判断是否有输入信息
    search_user = $("input[id=modal_input_search]").val();
    if(search_user == ""){
      alert("请输入用户名！！！")
    }
    else{
      data = {
        type:"search",
        search_name:search_user
      }
      $.post("/oltp/admin/",data,function(data1,status){
          json = JSON.parse(data1)
          if(json.exist == "1"){
              $('#myModal').modal('hide')
              tr = document.getElementsByClassName("list")
              for(var i=1;i<tr.length;i++){
                    tr[i].style.display="none";
              }
              tr[0].children.td_username.innerText = json.username
              tr[0].children.td_email.innerText = json.email
              tr[0].children.td_group.innerText = json.group
              tr[0].children.td_active.innerText = json.status
        }
        else {
            alert("用户不存在");
        }
      })
    }

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
                  alert("Data: " + data1 + "\nStatus: " + status);
            })
            $(this).dialog("close");
          
            // 修改页面显示
            selecte = document.getElementsByClassName("selected")
            if (update_email == ""){
              selecte.td_email.innerText = document.getElementById("dialog_update_email").placeholder
            }
            else{
              selecte.td_email.innerText = update_email
            }
            if (update_status == ""){
              selecte.td_active.innerText = document.getElementById("dialog_update_status").placeholder
            }
            else{
              selecte.td_active.innerText = update_status
            }

            if (update_group == ""){
              selecte.td_group.innerText = document.getElementById("dialog_update_group").placeholder
            }
            else{
              selecte.td_group.innerText = update_group
            }

            $("td").removeClass("selected");  

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
   if (num == 4){ // 控制用户选择行数
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
      // 新增用户显示在第一行
      var ta = document.getElementById("table_list_userInfo");
      var ftr = document.createElement("tr");
      var td_u = document.createElement("td");
      var td_a = document.createElement("td");
      var td_e = document.createElement("td");
      var td_g = document.createElement("td");

      ftr.className = "list"
      var biaotou = document.getElementById("biaotou");
      biaotou.after(ftr)
      
      td_u.dataset.toggle="tooltip"
      td_u.dataset.placement="left"
      td_u.textContent = dia_username;
      ftr.appendChild(td_u)

      td_e.dataset.toggle="tooltip"
      td_e.dataset.placement="left"
      td_e.textContent = dia_email;
      ftr.appendChild(td_e)
      
      td_a.dataset.toggle="tooltip"
      td_a.dataset.placement="left"
      td_a.innerText = "True"
      ftr.appendChild(td_a)

      td_g.dataset.toggle="tooltip"
      td_g.dataset.placement="left"
      td_g.innerText = group
      ftr.appendChild(td_g)
      
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

    select = $('.selected')
    var num=$('.selected').length
    if (num>3){
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
        }
        else{
            alert("请选择至少选择一行数据") 
        }
    });

});
