
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
function InitTimepicker(double) {
  if (double) {
    $("#datepicker1").datepicker({
      onSelect: function(startDate) {
        var $startDate = $("#datepicker1");
        var $endDate = $('#datepicker2');
        var endDate = $endDate.datepicker('getDate');

        if (endDate < startDate) {
          $endDate.datepicker('setDate', startDate - 3600 * 1000 * 24);
        }
        $endDate.datepicker("option", "minDate", startDate);
      }

    });
    $("#datepicker2").datepicker({
      onSelect: function(startDate) {
        var $startDate = $("#datepicker1");
        var $endDate = $('#datepicker2');
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
//创建datepicker所需的div
function makeDatepicker(radio_name,selectedvalue,divname){
  $("input[name="+radio_name+"]").change(function(){

          var selected = $("input[name="+radio_name+"]:checked").val();//把radiobtn的name命名为Radio，从中选出被checked的
          if (selected==selectedvalue) {
              $(divname).append("<input type='text' class='form-control' name='datepicker1' id='datepicker1' placeholder='起始日期'/>");
              $(divname).append("<input type='text' class='form-control' name='datepicker2' id='datepicker2' placeholder='截止日期'/>");
              InitTimepicker(true)
          }
          else{
            $(divname).empty()
          };
        });
}


$(function() {
  var searchtype="bycampID"
  $("#OnSearch").bind("click", function() {
    if ($("#searchform").valid()){
      $.get($SCRIPT_ROOT + "/_getMyScore", {
      campID: $('input[name="inputcampID"]').val()
    }); //更新总分
    $.get($SCRIPT_ROOT + "/_getStuInfo", {
      campID: $('input[name="inputcampID"]').val(),
      starttime:$("#datepicker1").val(),
      endtime:$("#datepicker2").val(),
      searchtype:searchtype
    }, function(data) {
        $("#score_items thead").empty()
        $("#score_items tbody").empty() //获取#score_items下面的tbody
        $("#student thead").empty()
        $("#student tbody").empty()

      if (data == "无法找到") {
        alert(data)
      } else {

        var tbody_stu="<tr class='active'> <td>学号</td><td>" +data.campID+"</tr>"+"<tr class='active'> <td>姓名</td><td>" +data.name+"</tr>"+"<tr class='active'> <td>年级</td><td>" +data.grade+"</tr>"+"<tr class='active'> <td>总分</td><td>" +data.sum+"</tr>"
        $("#student").append(tbody_stu)


        var thead = "<tr class='info'> <th> 申请号 </th> <th> 所属类别 </th> <th> 加分项目 </th> <th> 分值 </th> <th> 时间 </th> <th> 申请时间 </th><th> 审核状态 </th> </tr> " //不能包含<thead>

        $("#score_items").append(thead)
        var tbBody = ""

        $.each(data.items, function() {
          if(this.status=="未审核"){

          tbBody += "<tr class='default'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)
          }
          else if (this.status=="通过") {
            tbBody += "<tr class='success'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)

          }
          else{
            tbBody += "<tr class='danger'><td>" + this.id + "</td>" + "<td>" + this.catagory + "</td>" + "<td>" + this.item_name + "</td>" + "<td>" + this.add + "</td>" + "<td>" + this.time + "</td>" + "<td>" + this.applytime + "</td>" + "<td>" + this.status + "</td></tr>";
          $("#score_items").append(tbBody)
          }


        });
      }
    });
    }

  });
});

$().ready(function() {
 $("#searchform").validate(
  {
    rules:{
          datepicker1: {
            required:true,
            dateISO:true
          },
          datepicker2:{
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
