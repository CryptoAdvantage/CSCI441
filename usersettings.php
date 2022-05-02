<html>
<?php
    include_once "./models/User.php";
    $user = new User();
    $user->validate();

    if(isset($_GET["update"])){
        $user->resetPassword();
    } elseif(isset($_GET["update"])){
        $user->deleteAccount();
    }

   $pageTitle = "CryptoAdvantage | Settings";
   include_once "./templates/header.php";
   include_once "./templates/navbar_stduser.php";
?>

<body>
    <main>
        <h2>Update Password</h2>
        <form method="POST" class="entry-form" action="./usersettings.php?update">
        <div class="input-item">
                <label for="newPassword">New Password <small>(8 char minimum)</small>:</label>
                <input type="password" id="newPassword" name="newPassword" minlength="8" required>                
            </div>
            <div class="input-item">
                <label for="currentPassword">Current Password:</label>
                <input type="password" id="currentPassword" name="currentPassword" required>                
            </div>
            <div class="input-item">
                <input class="btn" type="submit" value="Reset Password">
            </div>
        </form>
        <br>
        <h2>Delete Account</h2>
        <form method="POST" class="entry-form" action="./usersettings.php?delete">
            <div class="input-item">
                <label for="password">Password <small>(8 char minimum)</small>:</label>
                <input type="password" id="password" name="password" minlength="8" required>                
            </div>
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