<footer>
    <ul>
        <li><a href="./about.php">About</a></li>
        <li><a href="./faq.php">FAQ</a></li>
        <li><a href="./login.php
        <?php
            if(!isset($_SESSION["loggedin"]) || !$_SESSION["loggedin"]){
                echo '">Log In</a></li>';
            } else {
                echo '?logout">Log Out</a></li>';
            }
        ?>
    </ul>
    <ul class="social-row">
        <li><a href="https://github.com/orgs/CryptoAdvantage"><i class="fab fa-github"></i></a></li>
    </ul>
</footer>
