<html>

<?php    
    include_once "./models/User.php";
    $user = new User();
    if(!$user->logIn()){
        session_destroy();
        header("Location: ./login.php?error");
        exit;
    }

    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    $pageTitle = "CryptoAdvantage | Dashboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar_stduser.php";

    $exchange = "binanceus";

    // $_SESSION cannot hold objects and will stringify the object so this fails round two.  
    //$tradeHistory = $_SESSION['validatedUser']->getTradeHistory($db);
?>

<body>
    <main>
        <h1>CryptoAdvantage Dashboard</h1>

        <div class = "user center round-corners"> 
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
            print_r($user->getTradeHistory());
            //This should print the trade history for the user. 
            ?>
            </table>
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

