<html>
<?php   
    session_start();
   $pageTitle = "CryptoAdvantage | Login";
   include_once "./templates/header.php";
   include_once "./templates/navbar.php";

   if(isset($_SESSION["loggedin"]) && $_SESSION["loggedin"]){
    header("Location: ./dashboard.php");       
    exit;
}
?>

<body>
    <main>
        <h2>Account Log In</h2>
        <form method="POST" class="entry-form" action="./dashboard.php">
            <div class="input-item">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="input-item">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>                
            </div>
            <div class="input-item">
                <input class="btn" type="submit" value="Log in">              
            </div> 
            <?php 
                if(isset($_GET["error"])){
                    echo "<h5>ERROR - Invalid credentials</h5>";
                }
            ?>         
        </form>
        
        <div class="other-options">
            <div class="btn">
                <a href="./register.php">New User</a>
            </div>  
            <div class="btn">
                <a href="./forgotpassword.php">Forgot Password</a>
            </div>           
        </div>       
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>