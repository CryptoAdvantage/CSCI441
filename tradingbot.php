<html>
<?php
    //session_start();
    $pageTitle = "CryptoAdvantage | Bot Creator";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";

    $botName = (array_key_exists("bot", $_POST)) ? $_POST["bot"] : "";
    $exchange = (array_key_exists("exchange", $_POST)) ? $_POST["exchange"] : "";
    $token1 = (array_key_exists("token1", $_POST)) ? $_POST["token1"] : "";
    $token2 = (array_key_exists("token2", $_POST)) ? $_POST["token2"] : "";
    $interval = (array_key_exists("interval", $_POST)) ? $_POST["interval"] : "";
    $strategy = (array_key_exists("strategy", $_POST)) ? $_POST["strategy"] : "";
    // Function to print out objects / arrays
    function PrintObj ($o) { echo "<pre>"; print_r($o); echo "</pre>"; }

    // Load the POST.
    $klines = file_get_contents("php://input");

    // ...and decode it into a PHP array.
    $klines = json_decode($klines); 

    // Do whatever with the array. 
    PrintObj($klines);
    exec("python ./tradingBot/bot_api.py $token1 $token2 $interval")
   ?>
   
   <body>
       <main>
            <h2>Trading Bot Placeholder</h2>
            <div id="chart"></div>
            <div id="trades"></div>
            <h3>Settings</h3>
            <div id="settings">
                <label for="rsi">RSI:</label>
                <input type="text" id="rsi_length" name="rsi_length" placeholder="14">
                <label for="rsi_overbought">Overbought:</label>
                <input type="text" id="rsi_overbought" name="rsi_overbought" placeholder="70">
                <label for="rsi_oversold">Oversold:</label>
                <input type="text" id="rsi_oversold" name="rsi_oversold" placeholder="30">
            </div>
            <div>
                
            </div>
       </main>
       <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
       <script src="./js/charts.js"></script>
   </body>
</html>