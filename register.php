<html>
<?php
   $pageTitle = "CryptoAdvantage | Login";
   include "./templates/header.php";
   include_once "./templates/navbar.php";
?>

<body>
    <main>
        <form action="./newuser.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" id="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$" required>
            </div>
            <div class="input-item">
                <label for="phone">Phone number:</label>
                <input type="tel" id="phone" pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}" required>
                <small>Format: 555-555-5555</small>
            </div>
            <div class="input-item">
                <label for="password">Password (8 char minimum):</label>
                <input type="password" id="password" minlength="8" required>                
            </div>
            <div class="input-item">
                <label for="password2">Password Validation:</label>
                <input type="password" id="password2" minlength="8" required>                
            </div>
            <input type="submit" value="Register">
        </form>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>