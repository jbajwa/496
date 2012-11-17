<?php

// Connect database
$db_host		= 'mysql11.000webhost.com';
$db_user		= 'a9789333_login01';
$db_pass		= 'Shilpa1';
$db_database	= 'a9789333_login'; 
 
/* End config */
 
 
 
$link = mysql_connect($db_host,$db_user,$db_pass) or die('Unable to establish a DB connection');
 
mysql_select_db($db_database,$link);
 
// Its always good to initialize arrays
$output = array();
$q=mysql_query("SELECT * FROM Events WHERE eid >'".$_POST['ID']."'");


// JSON version
// This while loop takes in each row of the mysql query,
// and appends it to the $output array
while($e=mysql_fetch_assoc($q))
{
    $output[]=$e;
}

// Encode this array in JSON format
print(json_encode($output));
 
mysql_close();
?>