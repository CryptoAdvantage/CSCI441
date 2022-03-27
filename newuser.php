<html>
<?php

    // header('Access-Control-Allow-Origin: *');
    // header('Content-Type: application/json');

    // $method = $_SERVER['REQUEST_METHOD'];
    // if ($method === 'OPTIONS') {
    //     header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
    //     header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    // }

    include_once "./config/Database.php";
    include_once "./models/User.php";

    $database = new Database();
    $db = $database->connect();
    $user = new User($db);
    
    $pageTitle = "CryptoAdvantage | Login";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";
?>

<body>
    <main>
        <?php
            echo "blah";
        ?>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>