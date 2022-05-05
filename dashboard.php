<html>

<?php    
    include_once "./models/User.php";
    $user = new User();
    $user->validate();
    exec("python ./tradingBot/accountData.py");

    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    $pageTitle = "CryptoAdvantage | Dashboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar_stduser.php";

    $exchange = "binanceus";
?>

<body>
    <main>
        <h1>CryptoAdvantage Dashboard</h1>

        <div class = "user center round-corners"> 
            <h2> Your Crypto: </h2>
            <?php
                echo "<table id='table_dashboard'";
                    echo "<tr>";
                        echo "<th>Crypto</th>";
                        echo "<th>Avail</th>";
                        echo "<th>Locked</th>";
                        echo "<th>Total</th>";
                    echo "</tr>";
                    $result = $user->getAccount();
                    $arr = json_decode($result[0]['docs'], true);

                    foreach($arr as $k => $val) {
                        $avail = round($val['free'],1);
                        $lock = round($val['locked'],1);
                        $total = round($val['total'],1);
                        echo "<tr>";
                              echo "<td>{$k}</td>";
                              echo "<td>{$avail}</td>";
                              echo "<td>{$lock}</td>";
                              echo "<td>{$total}</td>";
                         echo "</tr>";
                    }
                echo "</table>";
            ?>
            
        </div>
        <div class = "trading-bots">
            <div class = "trading-bot1 round-corners center">
                <p class="center"> View Your Trading Bots </p>
                <img src="./images/viewBot.png" alt="View Bot" width="400px" height="auto">
                <form action="./tradingbot.php">
                    <button type="submit" class="button center">View Bot</button>
                </form>
            </div>
            <div class = "trading-bot2 round-corners center">
                <p class="center"> Build a New Trading Bot </p>
                <img class="img-build" src="./images/buildBot.png" alt="Build Bot" width="400px" height="auto">
                <form action="./buildTradingBot.php">
                    <button type="submit" class="button center">Build Bot</button>
                </form>
            </div>
        </div>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>