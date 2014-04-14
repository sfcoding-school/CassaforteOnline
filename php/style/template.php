<!DOCTYPE html>
<html>
<head>
  <title>La tua Cassaforte</title>
  <link rel="stylesheet" type="text/css" href="style/cassaforteStyle.css">
  <link rel="stylesheet" type="text/css" href="style/templateStyle.css">
  <link rel="stylesheet" type="text/css" href="style/getProStyle.css">
  <link rel="stylesheet" type="text/css" href="style/listFile.css">
  <link rel="stylesheet" type="text/css" href="style/slide.css">

 	<script src="js/jquery-2.1.0.min.js"></script> 
 	
	<link href="js/uploadFile/css/uploadfile.css" rel="stylesheet">
	<script src="js/uploadFile/js/jquery.uploadfile.min.js"></script>
</head>
<body>
  <script>
      function controllaMail(email){
      var testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
      if (testEmail.test(email)){
        return true;
      }else{
        return false;
      }
    }
  </script>  
  
  <div class="barra">   
      <div class="titolo">La Tua Cassaforte Online</div>   
    <nav class="menu">
      <ul>
        
        <li><a href="/SAED/php">HOME</a></li>
        <li><a href="/SAED/php/?page=about">ABOUT</a></li>
        <li><a href="/SAED/php/?page=contact">CONTACT</a></li>
      </ul>
    </nav> 
  
    <div id="loginDiv">
      <?php
      include('style/loginDiv.php');
      ?>
    </div>
    
  </div>
      
      
  
  <div id="master">
    <?php
      include($page);
    ?>
  </div>

  <footer class='background'>
        <p>copyright 2014</p>
  </footer>

</boby>
</html>
