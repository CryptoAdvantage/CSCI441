<html>
<?php
   $pageTitle = "CryptoAdvantage | Login";
   include_once "./templates/header.php";
   include_once "./templates/navbar.php";
?>

<body>
    <main>
        <h2>Create New Account</h2>
        <form method="post" class="entry-form" action="./newuser.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required>
            </div>
            <div class="input-item">
                <label for="phone">Phone number <small>(ex 555-555-5555)</small>:</label>
                <input type="tel" id="phone" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" required>                
            </div>
            <div class="input-item">
                <label for="password">Password <small>(8 char minimum)</small>:</label>
                <input type="password" id="password" minlength="8" required>                
            </div>
            <div class="input-item">
                <input class="btn" type="submit" value="Register">              
            </div> 
        </form>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>