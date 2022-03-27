<html>
<?php
   $pageTitle = "CryptoAdvantage | Login";
   include_once "./templates/header.php";
   include_once "./templates/navbar.php";
?>

<body>
    <main>
        <h2>Account Log In</h2>
        <form method="post" class="entry-form" action="./dashboard.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required>
            </div>
            <div class="input-item">
                <label for="password">Password:</label>
                <input type="password" id="password" minlength="8" required>                
            </div>
            <div class="input-item">
                <input class="btn" type="submit" value="Log in">              
            </div>           
        </form>
        
        <div class="other-options">
            <div class="btn">
                <a href="./register.php">New User</a>
            </div>  
            <div class="btn">
                <a href="">Forgot Password</a>
            </div>           
        </div>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>