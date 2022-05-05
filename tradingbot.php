<html>
<?php
    include_once "./models/User.php";
    $user = new User();
    $user->validate();
    
    $pageTitle = "CryptoAdvantage | Bot Creator";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";

    $email = "hmhamdi@mail.fhsu.edu";
    $posted = (array_key_exists("bot", $_POST)) ? "true" : "false";
    $botName = (array_key_exists("bot", $_POST)) ? $_POST["bot"] : "Testing1";
    $exchange = (array_key_exists("exchange", $_POST)) ? $_POST["exchange"] : "Binanceus";
    $token1 = (array_key_exists("token1", $_POST)) ? $_POST["token1"] : "BTC";
    $token2 = (array_key_exists("token2", $_POST)) ? $_POST["token2"] : "USD";
    $interval = (array_key_exists("interval", $_POST)) ? $_POST["interval"] : "1h";
    $strategy = (array_key_exists("strategy", $_POST)) ? $_POST["strategy"] : "bb";
   ?>
   
   <body>
       <main>
            <h2>Trading Bot Dashboard</h2>
            <h3>Bitcoin Price Chart</h3>
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
                <?php 
                    exec("python ./tradingBot/bot_api.py $botName $exchange $token1 $token2 $interval $strategy $posted $email", $output);
                    foreach($output as $blah){
                    echo $blah;
                    }
                ?>
            </div>
       </main>
       <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
       <script src="./js/charts.js"></script>
   </body>
</html>