<?php

class File {
	function __construct($uuid, $name, $codest, $dim, $email) {
		$this -> uuid = $uuid;
		$this -> name = $name;
		$this -> codest = $codest;
		$this -> dim = $dim;
		$this -> email = $email;
	}

}

echo "salve ";
$fileName = $argv[1];
$email = $argv[2];
$fileNameTmp = "./upload/".$argv[3];
$fileUuid = uniqid ();
$dim = $argv[4];
$codest = $argv[5];


echo $fileName." ".$email." ".$fileNameTmp." ".$fileUuid;

$connection = ftp_connect("127.0.0.1");
$login = ftp_login($connection, "ftp", "romanelli");
if (!$connection || !$login) { die('Connection attempt failed!');}

$upload = ftp_put($connection, "/".$fileUuid, $fileNameTmp, FTP_BINARY);

if (!$upload){ echo 'FTP upload failed!';}

ftp_close($connection);

try {
		$client = new SoapClient('http://127.0.0.1:7790/?wsdl');
		$struct = new File($fileUuid, $fileName, $codest, $dim, $email);
		$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "File");
		$param = new SoapParam($soapstruct, "File");

 		//$result = $client->uploadFile($struct);
		$result = $client->uploadFile($param);

 		//var_dump($result);
		echo $result->uploadFileResult;

} catch (SoapFault $e) {
		echo $e;
}
?>