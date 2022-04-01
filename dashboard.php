<html>
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
        <img class="dashboard" src="./images/dashboard.png" alt="Dashboard placeholder">
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>
