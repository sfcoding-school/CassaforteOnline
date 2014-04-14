<?php
 class SayHelloStruct {
    function __construct($name, $times) {
        $this->name = $name;
        $this->times = $times;
    }
}

class File{
    function __construct($content,$name){
        $this->content = $content;
        $this->name = $name;
        
    }
    
}

if ($_FILES["file"]["error"] > 0)
    {
    echo "Return Code: " . $_FILES["file"]["error"] . "<br>";
    }
  else
    {
       
    echo "Upload: " . $_FILES["file"]["name"] . "<br>";
    echo "Type: " . $_FILES["file"]["type"] . "<br>";
    echo "Size: " . ($_FILES["file"]["size"] / 1024) . " kB<br>";
    echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br>";

    $tmpfile = $_FILES["file"]["tmp_name"];   // temp filename
    $filename = $_FILES["file"]["name"];      // Original filename

    $handle = fopen ($tmpfile, "r");                  // Open the temp file
    $contents = fread ($handle, filesize($tmpfile));  // Read the temp file
    fclose($handle);                                 // Close the temp file

    $decodeContent   = base64_encode($contents);
    
    echo "Content" . $decodeContent;
    
try {
    $client = new SoapClient('http://79.55.175.219:7789/?wsdl');
    //echo "dio";
    //echo $gsearch->say_hello('google');
    //for($i=0;$i<5;$i++)
     //   echo $dio[$i];
     
    
    $struct = new File($decodeContent, $filename);
    //$struct = new SayHelloStruct("Dave", 10);
    
    // here "say_hello" is not the method name but the name of the struct
    $soapstruct = new SoapVar($struct, SOAP_ENC_OBJECT, "uploadFile");
    $param = new SoapParam($soapstruct, "uploadFile");

    
    //$result = $client->uploadFile($struct);
    $result = $client->uploadFile($param);
    
    var_dump($result);
    
    
    } catch (SoapFault $e) {
    echo $e;
    }
}


?>
