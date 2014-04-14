<?php
/*
*
* Create Download Link
* Jaocb Wyke
* jacob@frozensheep.com
*
*/

//connect to the DB
$resDB = mysql_connect("localhost", "username", "thisismypassword");
mysql_select_db("database", $resDB);

function createKey(){
	//create a random key
	$strKey = md5(microtime());
	
	//check to make sure this key isnt already in use
	$resCheck = mysql_query("SELECT count(*) FROM downloads WHERE downloadkey = '{$strKey}' LIMIT 1");
	$arrCheck = mysql_fetch_assoc($resCheck);
	if($arrCheck['count(*)']){
		//key already in use
		return createKey();
	}else{
		//key is OK
		return $strKey;
	}
}

//get a unique download key
$strKey = createKey();

//insert the download record into the database
mysql_query("INSERT INTO downloads (downloadkey, file, expires) VALUES ('{$strKey}', 'onetimedownload.zip', '".(time()+(60*60*24*7))."')");

?>

<html>
	<head>
		<title>One Time Download Example</title>
	</head>
	<h1>One Time Download Example</h1>
	<p>Your unique download URL is:</p>
	<strong><a href="download.php?key=<?=$strKey;?>">download.php?key=<?=$strKey;?></a></strong>
	<p>This link will allow you to download the source code a single time within the next 7 days.</p>
</html>