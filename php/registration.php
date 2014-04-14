<?php
class User {
	function __construct($email, $pass) {
		$this -> email = $email;
		$this -> passwd = $pass;
	}

}

if (isset($_POST['email'])){
try {
	$email = $_POST['email'];
	$hashPass = hash('sha512', $_POST['password']);
	//echo "PHP ".$email." ".$pass;
	$client = new SoapClient('http://127.0.0.1:7790/?wsdl', array('cache_wsdl' => WSDL_CACHE_NONE));
	$struct = new User($email, $hashPass);
	$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "User");
	$param = new SoapParam($soapstruct, "User");

		//$result = $client->uploadFile($struct);
	$result = $client->registraUtente($param);

	//var_dump($result);
	echo $result->registraUtenteResult;

} catch (SoapFault $e) {
		echo $e;
}
}
?>