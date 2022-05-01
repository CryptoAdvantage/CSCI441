<html>
<?php
    include_once "./models/User.php";
    $user = new User();
    if(!$user->logIn()){
        session_destroy();
        header("Location: ./login.php?error");
        exit;
    }
    
    $pageTitle = "CryptoAdvantage | Bot Creator";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";

    $botName = (array_key_exists("bot", $_POST)) ? $_POST["bot"] : "";
    $exchange = (array_key_exists("exchange", $_POST)) ? $_POST["exchange"] : "";
    $token1 = (array_key_exists("token1", $_POST)) ? $_POST["token1"] : "";
    $token2 = (array_key_exists("token2", $_POST)) ? $_POST["token2"] : "";
    $interval = (array_key_exists("interval", $_POST)) ? $_POST["interval"] : "";
    $strategy = (array_key_exists("strategy", $_POST)) ? $_POST["strategy"] : "";
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
                <?php 
                    echo "<h3>Inside of PHP</h3>";
                    echo "<br>";
                    echo "Bot within PHP= " . $botName;
                    echo "<br>";
                    echo "Exchange within PHP= " . $exchange;
                    echo "<br><br>";
                    exec("python ./tradingBot/bot_api.py $botName $exchange $token1 $token2 $interval $strategy", $output);
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