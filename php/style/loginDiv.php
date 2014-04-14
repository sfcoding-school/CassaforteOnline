<script>
$(document).ready(function() {
      $("#accediButton").click(function(){
        //alert($("#contenitore").children().length);
        if ($("#contenitore").children().length > 0){
          $("#contenitore").empty();
          //$("#accediButton").removeAttr('style');
          $("#accediButton").toggleClass('buttonLoginDivClick');
        }else{
          $("#contenitore").load("content/login.html");
          //$("#accediButton").css('background','#E8E8E8');
          $("#accediButton").toggleClass('buttonLoginDivClick');
        }
      });

      $("#userEmail").click(function(){
        if ($("#contenitore").children().length > 0){
          $("#contenitore").empty();
          $("#userEmail").toggleClass('buttonLoginDivClick');
        }else{
          $("#contenitore").load("content/userMenu.html");
          $("#userEmail").toggleClass('buttonLoginDivClick');
        }
      });
      
      $("#registratiButton").click(function() {
        window.location.href = "/SAED/php/?page=getPro";
        });
    
    });
</script>
<?php
	session_start();
	if (isset($_SESSION['user'])){
		//echo 'funziona';
		echo 
			"
				<div id='userEmail' class='buttonLoginDiv'>".$_SESSION['user']."</div>
			";
	
	}else{
		echo
			"
				<span id='accediButton' class='buttonLoginDiv'>Accedi</span> | <span id='registratiButton' class='buttonLoginDiv'>Registrati</span>
      			
			";	
	}
?>
<div id='contenitore'></div>