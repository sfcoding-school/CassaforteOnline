<?php
class DimFile {
	function __construct($email, $dim) {
		$this -> email = $email;
		$this -> dim = $dim;
	}

}

if (isset($_POST['email']) && isset($_POST['dim'])){
	try {
		$email = $_POST['email'];
		$dim = $_POST['dim'];
		$client = new SoapClient('http://127.0.0.1:7790/?wsdl', array('cache_wsdl' => WSDL_CACHE_NONE));
		$struct = new DimFile($email, $dim);
		$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "DimFile");
		$param = new SoapParam($soapstruct, "DimFile");

		//var_dump($client->__getFunctions());
		$result = $client->checkFileSpace($param);

		//var_dump($result);
		echo $result->checkFileSpaceResult;

	} catch (SoapFault $e) {
		echo $e;
	}
}else{
	echo false;
}
?>