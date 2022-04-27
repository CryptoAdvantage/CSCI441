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
            <div class = "user-label">
                <label> Bitcoin: </label>
                <p> 1.32</p>
            </div>
            <div class = "user-label">
                <label> Ethereum: </label>
                <p> 0.45</p>
            </div>
            <div class = "user-label">
            <label> Rippple: </label>
            <p> 1.98</p>
            </div>


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
                <p> place holder for trading bot 1 </p>
                <form action="./tradingbot.php">
                    <button type="submit" class="build-bot-btn">Build Bot</button>
                </form>
            </div>
            <div class = "trading-bot2">
                <p> place holder for trading bot 2 </p>
                <form action="./tradingbot.php">
                    <button type="submit" class="build-bot-btn">Build Bot</button>
                </form>
            </div>
            <div class = "trading-bot3">
                <p> Place holder for trading bot 3</p>
                <form action="./tradingbot.php">
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

