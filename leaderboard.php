<html>

<?php
    include_once "./models/Leaderboard_Model.php";

    header('Access-Control-Allow-Origin: *');

    $method = $_SERVER['REQUEST_METHOD'];
    if ($method === 'OPTIONS') {
        header('Access-Control-Allow-Headers: Origin, Accept, Content-Type, X-Requested-With');
    }
    error_reporting(E_ERROR | E_PARSE);
    $pageTitle = "CryptoAdvantage | Leaderboard";
    include_once "./templates/header.php";
    include_once "./templates/navbar_stduser.php";


?>

<body>
    <main>
        <h1>CryptoAdvantage Leaderboard</h1>

        <div class = "user center round-corners">
            <h3>Weekly Leaderboard: </h3>
            <table id='table_Leaderboard'>
             <tr>
                <th>User</th>
                <th>Amount Earned</th>
            </tr>

            <?php
                $leaderboard = New Leaderboard_Model();

                foreach ($leaderboard->getLeaderboard() as $user => $amount) {
                    echo "<tr>";
                    echo "<td>{$user}</td>";
                    echo "<td>{$amount}</td>";
                    echo "</tr>";
                }
            ?>

        </table>
        </div>

        <div class = "user center round-corners">
            <h3>Monthly Leaderboard: </h3>
            <table id='table_Leaderboard'>
             <tr>
                <th>User</th>
                <th>Amount Earned</th>
            </tr>

            <?php
                foreach ($leaderboard->getLeaderboard('MONTH') as $user => $amount) {
                    echo "<tr>";
                    echo "<td>{$user}</td>";
                    echo "<td>{$amount}</td>";
                    echo "</tr>";
                }
            ?>

        </table>
        </div>

        <div class = "trade-history">
            <table>

            </table>
        </div>
    </main>
</body>

<?php
   include_once "./templates/footer.php"
?>
</html>
