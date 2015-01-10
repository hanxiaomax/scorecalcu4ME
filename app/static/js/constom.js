
//验证年级输入格式
jQuery.validator.addMethod("right_format", function(value, element) {
    var tel = /^20[0-9]{2}[本,硕,博]$/;
    return this.optional(element) || (tel.test(value));
}, "请使用正确的格式，如2013本");

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
