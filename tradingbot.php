<html>
<?php
     session_start();
     $pageTitle = "CryptoAdvantage | Bot Creator";
     include_once "./templates/header.php";
     include_once "./templates/navbar.php";
    
    $botName = $token1 = $token2 = $tradePair = $interval = $strategy = "";
    // Websocket for Binance API but in Javascipt at the moment
    // $kline_ws = new WebSocket(`wss://stream.binance.us:9443/ws/${trading_pair}@kline_${interval}`);

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $botName = test_input($_POST["bot name"]);
        $token1 = test_input($_POST["token 1"]);
        $token2 = test_input($_POST["token 2"]);
        $interval = test_input($_POST["interval"]);
        $strategy = test_input($_POST["strategy"]);
        $tradePair = $token1 + $token2;
        $url = `wss://stream.binance.us:9443/ws/${trading_pair}@kline_${interval}`;
       }
   
       function test_input($data) {
           $data = trim($data);
           $data = stripslashes($data);
           $data = htmlspecialchars($data);
           return $data;
       }
   ?>
   
   <body>
       <main>
           <h2>Trading Bot Creator</h2>
           <form method="post" class="entry-form" action="./dashboard.php">  
               <div class="input-item">
                   <label for="bot">Bot Name:</label>
                   <input type="text" id="bot" name="bot" required>
               </div>
               <div class="input-item">
                   <label for="token1">Token 1:</label>
                   <select id="token1" name="token1">
                       <option value="btc">Bitcoin</option>
                       <option value="eth">Ethereum</option>
                       <option value="ada">Cardana</option>
                       <option value="sol">Solana</option>
                   </select>
               </div>
               <div class="input-item">
                   <label for="token2">Token 2:</label>
                   <select id="token2" name="token2">
                       <option value="usd">USD</option>
                       <option value="usdt">USDT</option>
                       <option value="busd">BUSD</option>
                       <option value="usdc">USDC</option>
                   </select>
               </div>
               <div class="input-item">
                   <label for="interval">Time Interval:</label>
                   <select id="interval" name="interval">
                       <option value="1m">1 Minute</option>
                       <option value="3m">3 Minute</option>
                       <option value="5m">5 Minute</option>
                       <option value="15m">15 Minute</option>
                       <option value="30m">30 Minute</option>
                       <option value="1h">1 Hour</option>
                       <option value="2h">2 Hour</option>
                       <option value="4h">4 Hour</option>
                       <option value="6h">6 Hour</option>
                       <option value="8h">8 Hour</option>
                       <option value="12h">12 Hour</option>
                       <option value="4d">1 Day</option>
                       <option value="6d">3 Day</option>
                       <option value="8w">1 Week</option>
                       <option value="1M">1 Month</option>
                   </select>
               </div>
               <div class="input-item">
                   <label for="strategy">Strategy:</label>
                   <select id="strategy" name="strategy">
                       <option value="bb">Bollinger Bands</option>
                       <option value="bbdd">BB Double Dip</option>
                       <option value="ml">Machine Learning</option>
                       <option value="custom">Custom</option>
                   </select>
               </div>
               <div class="input-item">
                   <input class="btn" type="submit" value="Submit">
               </div>
           </form>
       </main>
   </body>
<?php
   include_once "./templates/footer.php"
?>
</html>