<html>
<link id="primary-css" rel="stylesheet" href="./styles/_dashboard.scss">
<?php
    session_start();
    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    include_once "./models/BaseModel.php";
    include_once "./config/Database.php";
    include_once "./models/User.php";
    include_once "./models/validatedUser.php";

    $pageTitle = "CryptoAdvantage | Dashboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar_stduser.php";

    $database = new Database();
    $db = $database->connect();
    $user = new User();
    $exchange = "binanceus";

    if($user->isLogInAttempt()) {
        $attemptedUser = $user->logIn($db);
        $_SESSION["loggedin"] = $attemptedUser['loggedin'];
        if(!$_SESSION["loggedin"]){
            header("Location: ./login.php?error");
            exit;
        }
        $_SESSION['validatedUser'] = new validatedUser($attemptedUser['Email'], $attemptedUser['ID'], $attemptedUser['Phone'], $attemptedUser['Permission']);
    }

    if(!isset($_SESSION["loggedin"]) || !$_SESSION["loggedin"]){
        header("Location: ./login.php?error");
        exit;
    }

    $tradeHistory = $_SESSION['validatedUser']->getTradeHistory($db);

    // can use this statment to see trade history: print_r($tradeHistory);
?>

<body>
    <main>
        <h1>CryptoAdvantage Dashboard</h1>

        <div class = "user"> 
            <?php
            //This is where we will put the how much of each cryptocurrency the user has. We should store this in a database so that way we can pull it and keep it updated.
            ?>
            <h3> Your Crypto: </h3>
            <!-- <div class = "user-label">
                <label> Bitcoin: </label>
                <p> 1.32</p>
            </div> -->
            <!-- <div class = "user-label">
                <label> Ethereum: </label>
                <p> 0.45</p>
            </div> -->
            <!-- <div class = "user-label">
            <label> Rippple: </label>
            <p> 1.98</p>
            </div> -->

            <!-- 
                I only put this in temporarily just to get a return for the user account from the exchange, 
                This will be where we return the account holdings from the database, and we can use this file
                to update the current account holdings in the database when clicked to update.
            -->
            <?php
                exec("python ./tradingBot/accountData.py $exchange", $output);
                foreach($output as $blah){
                echo $blah;
                }
            ?>
        </div>

        <div class = "trade-history">
            <table>
            <?php 
            print_r($tradeHistory);
            //This should print the trade history for the user. 
            ?>
            </table>
        </div>
        <div class = "trading-bots">
            <div class = "trading-bot1">
                <p> View Your Trading Bots </p>
                <img src="./images/viewBot.jpg" alt="View Bot">
                <form action="./TradingBot.php">
                    <button type="submit" class="view-bot-btn">View Bot</button>
                </form>
            </div>
            <div class = "trading-bot2">
                <p> Build a New Trading Bot </p>
                <img src="./images/build-Bot.png" alt="Build Bot">
                <form action="./buildTradingBot.php">
                    <button type="submit" class="build-bot-btn">Build Bot</button>
                </form>
            </div>
        </div>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>

