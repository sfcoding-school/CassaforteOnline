<?php
/*
 $page = "content/upload.html";
 require('style/template.php');
 */

class SayHelloStruct {
	function __construct($name, $times) {
		$this -> name = $name;
		$this -> times = $times;
	}

}

class File {
	function __construct($content, $name, $email) {
		$this -> content = $content;
		$this -> name = $name;
		$this -> email = $email;

	}

}

if (isset($_FILES["myfile"])) {

	$error = $_FILES["myfile"]["error"];
	//You need to handle  both cases
	//If Any browser does not support serializing of multiple files using FormData()

	$fileName = $_FILES["myfile"]["name"];
	$email = $_POST["email"];
	//move_uploaded_file($_FILES["myfile"]["tmp_name"], "upload/" . $fileName);
	//$ret = $_POST["email"];
	
	$content = file_get_contents($_FILES["myfile"]["tmp_name"]);
	$content = base64_encode($content);

/*
 if ($_FILES["myfile"]["error"] > 0) {
 echo "Return Code: " . $_FILES["file"]["error"] . "<br>";
 } else {

 echo "Upload: " . $_FILES["file"]["name"] . "<br>";
 echo "Type: " . $_FILES["file"]["type"] . "<br>";
 echo "Size: " . ($_FILES["file"]["size"] / 1024) . " kB<br>";
 echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br>";

 $tmpfile = $_FILES["file"]["tmp_name"];
 // temp filename
 $filename = $_FILES["file"]["name"];
 // Original filename

 $handle = fopen($tmpfile, "r");
 // Open the temp file
 $contents = fread($handle, filesize($tmpfile));
 // Read the temp file
 fclose($handle);
 // Close the temp file

 */

 try {
 $client = new SoapClient('http://127.0.0.1:7790/?wsdl');
 //echo "dio";
 //echo $gsearch->say_hello('google');
 //for($i=0;$i<5;$i++)
 //   echo $dio[$i];

 $struct = new File($content, $fileName, $email);
 //$struct = new SayHelloStruct("Dave", 10);

 // here "say_hello" is not the method name but the name of the struct
 $soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "uploadFile");
 $param = new SoapParam($soapstruct, "uploadFile");

 //$result = $client->uploadFile($struct);
 $result = $client->uploadFile($param);

 //var_dump($result);
 echo $result->uploadFileResult;

} catch (SoapFault $e) {
	
 echo $e;
 }
 

/*
 $page = "pagine/upload.html";
 require('template.php');
 */
}
?>