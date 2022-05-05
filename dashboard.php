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

/*     $servername = "localhost";
    $username = "username";
    $password = "password";
    $dbname = "myDBPDO"; */

/*     try {
        $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $stmt = $conn->prepare("SELECT `docs` FROM user_account WHERE `user_id`=14 AND `exch_id`=10");
        $stmt->execute();

        // set the resulting array to associative
        $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
        foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k=>$v) {
            echo $v;
        }
    } catch(PDOException $e) {
    echo "Error: " . $e->getMessage();
    }
    $conn = null; */


    // $_SESSION cannot hold objects and will stringify the object so this fails round two.  
    //$tradeHistory = $_SESSION['validatedUser']->getTradeHistory($db);
?>

<body>
    <main>
        <h1>CryptoAdvantage Dashboard</h1>

        <div class = "user center round-corners"> 
            <h3> Your Crypto: </h3>
            <?php
                echo "<table style='border: solid 1px black;'>";
                echo "<tr><th>Id</th><th>Firstname</th><th>Lastname</th></tr>";

                class TableRows extends RecursiveIteratorIterator {
                    function __construct($it) {
                        parent::__construct($it, self::LEAVES_ONLY);
                    }

                    function current() {
                        return "<td style='width: 150px; border: 1px solid black;'>" . parent::current(). "</td>";
                    }

                    function beginChildren() {
                        echo "<tr>";
                    }

                    function endChildren() {
                        echo "</tr>" . "\n";
                    }
                }

                $servername = "localhost";
                $username = "username";
                $password = "password";
                $dbname = "myDBPDO";

                try {
                    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
                    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                    $stmt = $conn->prepare("SELECT id, firstname, lastname FROM MyGuests");
                    $stmt->execute();

                    // set the resulting array to associative
                    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);

                    foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k=>$v) {
                        echo $v;
                    }
                }
                catch(PDOException $e) {
                    echo "Error: " . $e->getMessage();
                }
                $conn = null;
                echo "</table>";
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

