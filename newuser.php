<html>
<?php
    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        //header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE');
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }

    $pageTitle = "CryptoAdvantage | New User";
    include_once "./templates/header.php";
    include_once "./templates/navbar.php";
?>

<body>
    <main>
        <h2>Account Registration</h2>

        <?php
            include_once "./models/User.php";
            $user = new User();
            if($user->register()){
        ?>
            <p class="return-msg">Your new user account was created successfully!</p>
        <?php } else { ?>
            <p class="return-msg">ERROR - The email provided is already in the system.</p>
        <?php } ?>

        <p class="return-msg">
            Please return to the log-in page to access your account.
        </p>

        <div class="other-options">
            <div class="btn">
                <a href="./login.php">Return to Login</a>
            </div>
        </div>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>
