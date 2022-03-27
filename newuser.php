<html>
<?php
    header('Access-Control-Allow-Origin: *');
    header('Content-Type: application/json');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    $user = new User(new Database()->connect());
    
    $pageTitle = "CryptoAdvantage | Login";
    include "./templates/header.php";
    include_once "./templates/navbar.php";
?>

<body>
    <main>
        <?php
            
        ?>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>