<?php
if (isset($_GET['logout'])){
    session_start();
    $_SESSION=array();
    session_destroy();
}

if (isset($_GET['page'])){
	switch ($_GET['page']) {
    case 'getPro':
        $page = 'content/getPro.html';
        break;
    case 'about':
        $page = 'content/about.html';
        break;
    case 'contact':
        $page = 'content/contact.html';
        break;
    case 'listFile':
        $page = 'listFile.php';
        break;
	}
}else{
	$page = 'content/index.html';
}
require('style/template.php');
?>