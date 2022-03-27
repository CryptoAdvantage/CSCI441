<html>
<?php
    session_start();
    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        //header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    include_once "./models/BaseModel.php";
    include_once "./config/Database.php";
    include_once "./models/User.php";    

    $pageTitle = "CryptoAdvantage | Dashboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";

    if(!isset($_SESSION["loggedin"])){     
        $database = new Database();
        $db = $database->connect(); 

        $user = new User($db);     
        $_SESSION["loggedin"] = $user->logIn();
        $_SESSION["useremail"] = $user->POST("email");
    } 

    if(!$_SESSION["loggedin"]){
        header("Location: ./login.php?error");       
        exit;
    }
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