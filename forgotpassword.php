<html>
<?php
// TODO:  Implement password reset methodology
   $pageTitle = "CryptoAdvantage | Forgot Password";
   include_once "./templates/header.php";
   include_once "./templates/navbar.php";
?>

<body>
    <main>
        <h2>Forgot Password</h2>
        <form method="POST" class="entry-form" action="./login.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" name="email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required>
            </div>        
            <div class="input-item">
                <input class="btn" type="submit" value="Reset Password">              
            </div> 
            <small>(Reset email will arive shortly)</small>
        </form>
        
        
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>