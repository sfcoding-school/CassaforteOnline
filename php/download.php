<?php
class FileCode {
	function __construct($codeEst, $email) {
		$this -> code = $codeEst;
		$this -> email = $email;
	}

}
session_start();

if (isset($_GET['code']) && isset($_GET['email'])){
	$codeEst = $_GET['code'];
	$email = $_GET['email'];

	try {
		$client = new SoapClient('http://127.0.0.1:7790/?wsdl', array('cache_wsdl' => WSDL_CACHE_NONE));
		$struct = new FileCode($codeEst, $email);
		$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "FileCode");
		$param = new SoapParam($soapstruct, "FileCode");

		//$result = $client->uploadFile($struct);
		$result = $client->downloadFile($param);

		//var_dump($result);
		$file = $result->downloadFileResult;

	} catch (SoapFault $e) {
		echo -1;
		exit();
	}

	$tmpName = $file->tmpName;
	$tmpNameLocal = uniqid();
	$name = $file->name;

	//echo $tmpName.$tmpNameLocal.$name;
	// set up basic connection
	$conn_id = ftp_connect('127.0.0.1');

	// login with username and password
	$login_result = ftp_login($conn_id, 'ftp', 'romanelli');

	// try to download $server_file and save to $local_file
	if (ftp_get($conn_id, 'upload/'.$tmpNameLocal, $tmpName, FTP_BINARY)) {

    	$_SESSION['fileName'] = $name;
    	
    	echo $tmpNameLocal;

	}else {
    echo -1;
	// close the connection
	ftp_close($conn_id);
	exit();
	}
}


if (isset($_GET['fileUuid']) && isset($_SESSION['fileName'])){
	//echo "post: ".$_POST['fileUuid']." session: ".$_SESSION['fileName'];
	//$file = 'upload/'.$_POST['fileUuid'];
	//$name = $_SESSION['fileName'];
	
	$file = 'upload/'.$_GET['fileUuid'];
	$name = $_SESSION['fileName'];
	$strFile = file_get_contents($file);
	
	//set the headers to force a download
	header("Content-type: application/force-download");
	header("Content-Disposition: attachment; filename=\"".str_replace(" ", "_", $name)."\"");

	//$_SESSION = array();
	//session_destroy();

	//echo the file to thse user
	echo $strFile;
}
?>