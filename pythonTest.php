<?php
$var1 = "TestVariable1";
$var2 = 900;

echo "<h3>Inside of PHP</h3>";
echo "Var1 within PHP= " . $var1;
echo "<br>";
echo "Var2 within PHP= " . $var2;
echo "<br><br>";

exec("python3 ./tradingBot/testing.py $var1 $var2", $output);

foreach($output as $blah){
    echo $blah;
}