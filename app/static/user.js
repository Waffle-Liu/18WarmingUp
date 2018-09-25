// /**
 // * Created by Ding-YH on 2015/9/29.
 // */
var main = function() {	
	$(".log").hide();
    $(".shengchan").hide();
    $("#tab01").click(function () {
		
        $(".shengchan").hide();
        $(".caigou").show();
        $("#tab02").removeClass(("active"));
        $("#tab01").addClass("active");
    });

    $("#tab02").click(function () {
         $(".caigou").hide();
        $(".shengchan").show();
        $("#tab01").removeClass(("active"));
        $("#tab02").addClass("active");
    });

	//$(".buyamount").keyup(function(){  #键入采购量后会实时显示总价
	//	am = $(this).val();
	//	$(".totalpay").text( {{material_a[game_round]}} );
	//});
	$(".btn-submit").click(function(){
		alert("提交成功");
	});
	$(".bill").click(function(){
		$(".log").toggle();
	});
};

$(document).ready(main);