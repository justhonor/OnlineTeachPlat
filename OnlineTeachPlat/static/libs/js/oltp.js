
$(document).ready(function(){
  $("tr.list").click(function(e){
  	$(this).children('td').toggleClass("selected")
  });

  $("#id_delete").click(function(e){
  	console.log(e);
  	$('td').nextAll('.selected').parent().hide()

  	var num=$('.selected').length
  	var users=new Array();
  	var j=0;

  	var data = [];
  	// 取数据
  	for (var i=0;i<num;i=i+4)
  	{
  		users[j]=$(".selected:eq("+i+")").text()
  		j = j + 1;
  		num = num - 1;
  	}

  	json=JSON.stringify(users)
  	console.log(users)
  	console.log(json)
	// 后台删
	$.post("/oltp/admin/",json,function(data1,status){
		alert("Data: " + data1 + "\nStatus: " + status);
	})

  });

});
