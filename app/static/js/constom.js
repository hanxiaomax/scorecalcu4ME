
//验证年级输入格式
jQuery.validator.addMethod("right_format", function(value, element) {
    var tel = /^20[0-9]{2}[本,硕,博]$/;
    return this.optional(element) || (tel.test(value));
}, "请使用正确的格式，如2013本");



//验证学号必须是6位
jQuery.validator.addMethod("isSixdigit", function(value, element) {
    var tel = /^[0-9]{6}$/;
    return this.optional(element) || (tel.test(value));
}, "请输入6位数学号");




//初始化两个datepick，保证后者可选日期不能早于前者
function InitTimepicker(double,pickername) {
  if (double) {
    $("#"+pickername+"1").datepicker({
      onSelect: function(startDate) {
        var $startDate = $("#"+pickername+"1");
        var $endDate = $("#"+pickername+"2");
        var endDate = $endDate.datepicker('getDate');

        if (endDate < startDate) {
          $endDate.datepicker('setDate', startDate - 3600 * 1000 * 24);
        }
        $endDate.datepicker("option", "minDate", startDate);
      }

    });

    $("#"+pickername+"2").datepicker({
      onSelect: function(startDate) {
        var $startDate = $("#"+pickername+"1");
        var $endDate = $("#"+pickername+"2");
        var endDate = $endDate.datepicker('getDate');
        if (endDate < startDate) {
          $endDate.datepicker('setDate', startDate - 3600 * 1000 * 24);
        }
        $endDate.datepicker("option", "minDate", startDate);
      }
    });
  }
  else{
      $( "#datepicker" ).datepicker();
  }
}
function makeDatepicker(divname,pickername){
    $(divname).append("<input type='text' class='form-control' name="+pickername+"1"+" id="+pickername+"1"+" placeholder='起始日期'/>");
    $(divname).append("<input type='text' class='form-control' name="+pickername+"2"+" id="+pickername+"2"+" placeholder='截止日期'/>");
    InitTimepicker(true,pickername)
};




$(function() {
  var searchtype="bycampID"
  $("#OnSearch").bind("click", function() {
    if ($("#searchform").valid()){
      $.get($SCRIPT_ROOT + "/_getMyScore", {
      campID: $('input[name="inputcampID"]').val()
    }); //更新总分
    $.get($SCRIPT_ROOT + "/_getStuInfo", {
      campID: $('input[name="inputcampID"]').val(),
      starttime:$("#pickeB1").val(),
      endtime:$("#pickeB2").val(),
      searchtype:searchtype
    }, function(data) {
        $("#score_items thead").empty()
        $("#score_items tbody").empty() //获取#score_items下面的tbody
        $("#student thead").empty()
        $("#student tbody").empty()

      if (data == "无法找到") {
        alert(data)
      }
      else {

        var tbody_stu="<tr class='active'> <td>学号</td><td>" +data.campID+"</tr>"+"<tr class='active'> <td>姓名</td><td>" +data.name+"</tr>"+"<tr class='active'> <td>年级</td><td>" +data.grade+"</tr>"+"<tr class='active'> <td>总分</td><td>" +data.sum+"</tr>"
        $("#student").append(tbody_stu)


        var thead = "<tr class='info'> <th> 申请号 </th> <th> 所属类别 </th> <th> 加分项目 </th> <th> 分值 </th> <th> 时间 </th> <th> 申请时间 </th><th> 审核状态 </th> </tr> " //不能包含<thead>

        $("#score_items").append(thead)
        var tbBody = ""

        $.each(data.items, function() {
          if(this.status=="未审核"){

          tbBody = "<tr class='default'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)
          }
          else if (this.status=="通过") {
            tbBody = "<tr class='success'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)

          }
          else{
            tbBody = "<tr class='danger'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)
          }


        });
      }
    });
    }
  });
});

$(function() {
  $("#OnSearchgrade").bind("click", function() {
    var searchtype="bygrade"
    if ($("#searchgradeform").valid()){

    $.get($SCRIPT_ROOT + "/_getStuInfo", {
      grade:$('input[name="gradeinput"]').val(),
      starttime:$("#pickeD1").val(),
      endtime:$("#pickeD2").val(),
      searchtype:searchtype
    }, function(data) {
        $("#students thead").empty()
        $("#students tbody").empty()


      if (data == "无法找到") {
        alert(data)
      }
      else {
        var thead = "<tr class='info'> <th> 学号 </th> <th> 姓名 </th> <th> 年级 </th> <th> 分值 </th> </tr> " //不能包含<thead>

        $("#students").append(thead)

        $.each(data.GradeSumary, function() {
          var tbBody = ""
            tbBody += "<tr class='default'><td>" + this.campID + "</td>" + "<td>" + this.name + "</td>" + "<td>" + this.grade + "</td>" + "<td>" + this.sum + "</td>" + "</tr>";
          $("#students").append(tbBody)
        });
      }
    });
    }

  });
});



//验证按学号搜索
$().ready(function() {
 $("#searchform").validate(
  {
    rules:{
          pickeB1: {
            required:true,
            dateISO:true
          },
          pickeB2:{
            required:true,
            dateISO:true
          },
          inputcampID: {
            required:true,
            isSixdigit:true
          },
        },
    wrapper: "p"

  });
});

//验证按年级搜索
$().ready(function() {
 $("#searchgradeform").validate(
  {
    rules: {
          pickeD1: {
            required:true,
            dateISO:true
          },
          pickeD2:{
            required:true,
            dateISO:true
          },
          gradeinput:{
            required:true,
            right_format:true,
          },
        },
    wrapper: "p"
  });
});


function add_excel_list(role) {
  $("#exceltable thead").empty()
  $("#exceltable tbody").empty()
  $.get($SCRIPT_ROOT + "/_makepublic", {
      pic: "111"
    },
    function(data) {
      var thead = "<tr><th style='display:none;'>ID</th><th>标题</th><th>年级</th><th>公示区间</th><th>创建时间</th><th>创建人</th><th>操作/状态</th></tr>" //不能包含<thead>
      $("#exceltable").append(thead)
      var tbody = ""
      if (role=="student") {
        $.each(data.excellist, function() {
        var tbBody = ""
          if (this.status=="正在公示") {
              tbBody += "<tr ><td style='display:none;'>" + this.id + "</td>" + "<td>" + this.Excelname + "</td>"+"<td>" + this.grade + "</td>"+"<td>" + this.time + "</td>" + "<td>" + this.creater_time + "</td>" + "<td>" + this.creater + "</td>" + "<td>" + "<input type='button' class='btn btn-info btn-xs' value='下载' onclick='view(this)'/></td></tr>";
          }
        $("#exceltable").append(tbBody)
      });
      }else{
        $.each(data.excellist, function() {
        var tbBody = ""

          var btnstyle
          if (this.status=="正在公示") {
             btnstyle="btn-success"
          }
          else
          {
             btnstyle="btn-warning"
          }

        tbBody = "<tr ><td style='display:none;'>" + this.id + "</td>" + "<td>" + this.Excelname + "</td>"+"<td>" + this.grade + "</td>"+"<td>" + this.time + "</td>" + "<td>" + this.creater_time + "</td>" + "<td>" + this.creater + "</td>" + "<td>" + "<input type='button' class='btn btn-info btn-xs' value='下载' onclick='view(this)'/><span> </span><input type='button' value='删除' class='btn btn-danger btn-xs' onclick='del(this)' /> <span>/</span> <input type='button' value='"+this.status+"' id='ing' class='btn "+btnstyle+" btn-xs' onclick='status(this)' />" + "</td></tr>";

        $("#exceltable").append(tbBody)
      });
      }

    });
}
