$(document).ready(function(){
	$("form").submit(function(){
		$("#animation").show();
		$(".results").hide();
	});

	// going to make this file do double duty
	$("#show").click(function(){
		$(".debug").slideToggle();
		if($("#show").text() == "Show"){
			$("#show").text("Hide");
		}else{
			$("#show").text("Show");
		}
	});
});