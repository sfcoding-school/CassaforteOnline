<?php
class User {
		function __construct($email) {
			$this -> email = $email;
	}
}

session_start();
if (isset($_SESSION['user'])){
	//echo "sei pro!";
	
	try {
		$email = $_SESSION['user'];
		$client = new SoapClient('http://127.0.0.1:7790/?wsdl', array('cache_wsdl' => WSDL_CACHE_NONE));
		$struct = new User($email);
		$soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "User");
		$param = new SoapParam($soapstruct, "User");

			//$result = $client->uploadFile($struct);
		$result = $client->listFile($param);
		$result = $result->listFileResult->File;
		//var_dump($result);

		} catch (SoapFault $e) {
			echo $e;
		}
		#print row['codest']
    	#print row['nome']
    	#print row['dim']
		echo "<table class=fileList>";
		echo "<tr><th>Codice</th><th>Nome</th><th>Dimensione</th></tr>";
		for ($i=0; $i < count($result); $i++) { 
		 	# code...
		 	echo "<tr>";
			echo "<td>".$result[$i]->codest."</td>";
			echo "<td>".$result[$i]->nome."</td>";
			echo "<td>".$result[$i]->dim."</td>";
			echo "</tr>";
		}
		echo "</table>";

}else{
	echo 'zona protetta!';
}
?>