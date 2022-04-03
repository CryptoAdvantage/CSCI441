<html>
<?php
    session_start();
    $pageTitle = "CryptoAdvantage | Bot Creator";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";

    
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
       </main>
       <script src="https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"></script>
       <script src="./js/charts.js"></script>
   </body>
<?php
   include_once "./templates/footer.php"
?>
</html>