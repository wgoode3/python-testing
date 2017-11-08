$(document).ready(function(){
	$("form").submit(function(){
		$("#animation").show();
		$(".code").hide();
		$(".tests").hide();
	});

	// going to make this file do double duty
	$("#debug").click(function(){
		$(".debug").slideToggle();
		if($("#debug").text() == "Debug"){
			$("#debug").text("Close");
		}else{
			$("#debug").text("Debug");	
		}
	})
});