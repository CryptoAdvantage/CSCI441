<html>
<?php
   $pageTitle = "CryptoAdvantage | Login";
   include "./templates/header.php";
   include_once "./templates/navbar.php";
?>

<body>
    <main>
        <form class="entry-form" action="./dashboard.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required>
            </div>
            <div class="input-item">
                <label for="password">Password:</label>
                <input type="password" id="password" minlength="8" required>                
            </div>
            <div class="input-item">
                <input type="submit" value="Log in">              
            </div>
            
        </form>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>