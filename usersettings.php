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

   $pageTitle = "CryptoAdvantage | Settings";
   include_once "./templates/header.php";
   include_once "./templates/navbar_stduser.php";
?>

<body>
    <main>
    <h2>Account Settings</h2>
        <form method="POST" class="entry-form" action="./usersettings.php">
            <div class="input-item">
                <label for="password">New Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <div class="input-item">
                <input class="btn" type="submit" value="Reset Password">
            </div>
        </form>
        <form method="POST" class="entry-form" action="./usersettings.php">
            <div class="input-item">
                <input class="btn" type="submit" value="Delete Account">
            </div>
        </form>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>