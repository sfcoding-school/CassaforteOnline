<?php
class user {
	function __construct($email, $hashPass) {
		$this -> email = $email;
		$this -> passwd = $hashPass;
	}

}

session_start();

if (isset($_POST['email']) && isset($_POST['password'])){
	$email = $_POST['email'];
	$hashPass = hash('sha512', $_POST['password']);

	try {
		$client = new SoapClient('http://127.0.0.1:7790/?wsdl', array('cache_wsdl' => WSDL_CACHE_NONE));
		$struct = new user($email,$hashPass);
		$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "user");
		$param = new SoapParam($soapstruct, "user");

		//var_dump($client->__getFunctions());
		$result = $client->login($param);

		//var_dump($result);
		$ris = $result->loginResult;

	} catch (SoapFault $e) {
		echo $e;
	}

	

	if($ris==1){
		//utente registrato
		$_SESSION['user'] = $email;
		//echo $_SESSION['user'];
		echo true;
	}else{
		//utente non registrato
		echo false;
	}

}else{
	echo false;
}
?>