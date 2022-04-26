<?php
$botName = "TestBot";
$exchange = "binanceus";
$token1 = "BTC";
$token2 = "USD";
$interval = "1m";
$strategy = "BB";

echo "<h3>Inside of PHP</h3>";
echo "Bot Name within PHP= " . $botName;
echo "<br>";
echo "Exchange within PHP= " . $exchange;
echo "<br>";
echo "Token 1 within PHP= " . $token1;
echo "<br>";
echo "Token 2 within PHP= " . $token2;
echo "<br>";
echo "Interval within PHP= " . $interval;
echo "<br>";
echo "Strategy within PHP= " . $strategy;
echo "<br><br>";

exec("python ./tradingBot/mainTest.py $botName $exchange $token1 $token2 $interval $strategy", $output);

foreach($output as $blah){
    echo $blah;
}