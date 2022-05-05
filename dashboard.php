<html>

<?php    
    include_once "./models/User.php";
    include_once "./config/Database.php";
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
    $conn = new Database();
    $conn->connect();
    $stmt = $conn->prepare("SELECT `docs` FROM user_account WHERE `user_id`=14 AND `exch_id`=10");
    $stmt->execute();

    // $_SESSION cannot hold objects and will stringify the object so this fails round two.  
    //$tradeHistory = $_SESSION['validatedUser']->getTradeHistory($db);
?>

<body>
    <main>
        <h1>CryptoAdvantage Dashboard</h1>

        <div class = "user center round-corners"> 
            <h3> Your Crypto: </h3>
            <?php
                echo "<table>";
                    echo "<tr>";
                        echo "<th>Cryptocurrency</th>";
                        echo "<th>Available</th>";
                        echo "<th>Locked</th>";
                        echo "<th>Total</th>";
                    echo "</tr>";
                    $arr = json_decode($stmt, true);
                    foreach($arr as $k => $val) {
                        $avail = $val['free'];
                        $lock = $val['locked'];
                        $total = $val['total'];
                        echo "<tr>";
                            echo `<td>${k}:</td>`;
                            echo `<td>${avail}:</td>`;
                            echo `<td>${lock}:</td>`;
                            echo `<td>${total}:</td>`;
                        echo "/tr";
                echo "</table>"
            ?>

            <!-- <div class = "user-label">
                <label> Bitcoin: </label>
                <p> 1.32</p>
            </div> -->
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

