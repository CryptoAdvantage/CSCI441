<html>

<?php
    include_once "./models/Leaderboard_Model.php";

    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    $pageTitle = "CryptoAdvantage | Leaderboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar_stduser.php";


?>

<body>
    <main>
        <h1>CryptoAdvantage Leaderboard</h1>

        <div class = "user center round-corners">
            <?php
                $leaderboard = New Leaderboard_Model();
            ?>
            <h3> Your Crypto: </h3>

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
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>
