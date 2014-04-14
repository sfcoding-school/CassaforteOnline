<?php

if (isset($_FILES["myfile"])) {

	if($error = $_FILES["myfile"]["error"]>0){
		echo "errore caricamento file: ".$_FILES["myfile"]["error"];
	}else{
	//You need to handle  both cases
	//If Any browser does not support serializing of multiple files using FormData()

	$fileName = $_FILES["myfile"]["name"];
	$email = $_POST["email"];
	$fileNameTmp = $_FILES["myfile"]["tmp_name"];
	$fileUuid = uniqid();
	$fileDim = $_FILES["myfile"]["size"];

	//echo $fileName." ".$email." ".$fileUuid." ".$fileDim;

	$ris = move_uploaded_file($fileNameTmp, "./upload/".$fileUuid);
	$code = shell_exec("python codeGenerator.py");

	shell_exec("php -f uploadFileAsync.php $fileName $email $fileUuid $fileDim $code &");
	
	//shell_exec("php uploadFileAsync.php diosd.s asd@sd.sd asd8789sdsd asdsa7678sdsd 123123123 > upload/log 2>&1 &");

	echo $code;
	//$ret = $_POST["email"];

	}
}else{
	echo "niente da fare ";
}
?>