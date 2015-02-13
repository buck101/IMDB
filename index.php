<?php
    header("Content-Type: text/html;charset=utf-8"); 
    $con = mysql_connect("localhost", "root", "");
    if (!$con)
    {
        die('Could not connect: ' . mysql_error());
    }
    mysql_select_db("movies", $con);
    mysql_query("set names utf8");
    
    $result = mysql_query("select * from xlh_fileid2show_name");
    
    while ($row = mysql_fetch_array($result))
    {
       echo "<a href='xunleihao/".$row['fileid']."'>";
       echo $row['show_name'];
       echo  "<br /></a>"; 
    }
?>
