<?php

include_once __DIR__ . "/BaseModel.php";
class Leaderboard_Model extends BaseModel{

    public function __construct(){
        parent::__construct();
    }

    public function getLeaderboard($time = 'WEEK') {
        $cmd = "SELECT t.UserID, c1.Ticker, c2.Ticker as 'Ticker2', p.Date, p.USD_Price, t.Action, t.Quantity FROM tradehistory t INNER JOIN tradepair c ON t.PairID = c.ID INNER JOIN cryptocurrency c1 ON c.FirstPairID = c1.ID INNER JOIN cryptocurrency c2 ON c.SecondPairID = c2.ID INNER JOIN exchange e ON t.ExchID = e.ID INNER JOIN pricehistory p ON t.PriceID = p.ID WHERE p.Date between date_sub(now(),INTERVAL 1 " . $time .") and now() ORDER BY t.UserID DESC;";
        //$cmd = "SELECT t.UserID, c2.Ticker, p.Date, p.USD_Price, t.Action, t.Quantity FROM tradehistory t INNER JOIN tradepair c ON t.PairID = c.ID INNER JOIN cryptocurrency c1 ON c.FirstPairID = c1.ID INNER JOIN cryptocurrency c2 ON c.SecondPairID = c2.ID INNER JOIN exchange e ON t.ExchID = e.ID INNER JOIN pricehistory p ON t.PriceID = p.ID ORDER BY t.UserID DESC;";

        $DBData = $this->execute($cmd)->fetchAll();
        $users = array();
        $leaderboard = array();
        foreach ($DBData as $row) {
            $users[$row['UserID']] = array();
        }
        foreach ($DBData as $row) {
            if ($row['Action'] == 0 ) {
                if (array_key_exists($row['Ticker'], $users[$row['UserID']])) {
                    $users[$row['UserID']][$row['Ticker']]['Quantity'] += $row['Quantity'];
                    $users[$row['UserID']][$row['Ticker']]['purchasePrice'] += $row['Quantity'] * ($row['USD_Price'] ?? 0);

                } else {
                    $users[$row['UserID']][$row['Ticker']]['Quantity'] = $row['Quantity'];
                    $users[$row['UserID']][$row['Ticker']]['purchasePrice'] = $row['Quantity'] * ($row['USD_Price'] ?? 0);
                }
            } else {
                if (array_key_exists($row['Ticker'], $users[$row['UserID']])) {
                    $users[$row['UserID']][$row['Ticker']]['Quantity'] -= $row['Quantity'];
                    if (isset($users[$row['UserID']][$row['Ticker']]['sellPrice'])) {
                        $users[$row['UserID']][$row['Ticker']]['sellPrice'] += $row['Quantity'] * ($row['USD_Price'] ?? 0);
                    } else {
                        $users[$row['UserID']][$row['Ticker']]['sellPrice'] = $row['Quantity'] * ($row['USD_Price'] ?? 0);

                    }

                } else {
                    echo "somethings up";
                }
            }

        }

        //curl setup to pull current ticker prices
        $curl = curl_init();
        curl_setopt($curl, CURLOPT_URL, "https://api.binance.com/api/v3/ticker/price");
        curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'GET' );
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, TRUE);
        $result = curl_exec($curl);

        //parse the json
        $binanceData = array();
        $json_result = json_decode($result, true);
        foreach ($json_result as $key => $value) {
                $binanceData[$value['symbol']] = $value['price'];
        }

        //find current exchange price and compare against purchase price
        foreach ($users as $userID => $cryptoArray) {
            $users[$userID]['priceDifference'] = 0;

            foreach ($users[$userID] as $cID => $cValue) {
                if ($users[$userID][$cID]['Quantity'] > 0) {
                    if (array_key_exists($cID . 'USDT', $binanceData)) {
                        $users[$userID][$cID]['currentPrice'] = $users[$userID][$cID]['Quantity'] * $binanceData[$cID . 'USDT'];
                        $users[$userID]['priceDifference'] += ($users[$userID][$cID]['currentPrice'] - $users[$userID][$cID]['purchasePrice']);
                    } elseif (array_key_exists($cID . 'BTC', $binanceData)) {
                        $users[$userID][$cID]['currentPrice'] = $users[$userID][$cID]['Quantity'] * $binanceData[$cID . 'BTC'] * $binanceData['BTCUSDT'];
                        $users[$userID]['priceDifference'] += ($users[$userID][$cID]['currentPrice'] - $users[$userID][$cID]['purchasePrice']);

                    } elseif (array_key_exists($cID . 'ETH', $binanceData)) {
                        $users[$userID][$cID]['currentPrice'] = $users[$userID][$cID]['Quantity'] * $binanceData[$cID . 'ETH'] * $binanceData['ETHUSDT'];
                        $users[$userID]['priceDifference'] += ($users[$userID][$cID]['currentPrice'] - $users[$userID][$cID]['purchasePrice']);
                    }
                }
                if (isset($users[$userID][$cID]['sellPrice'])) {
                    $users[$userID]['priceDifference'] += $users[$userID][$cID]['sellPrice'];
                }
            }
            $leaderboard[$userID] = $users[$userID]['priceDifference'];
        }
        //Show users by email on leaderboard.
        foreach ($leaderboard as $key => $value) {
            $userEmail = $this->execute("Select email from user where ID=?", array($key))->fetch();
            $newkey = $userEmail['email'];
            $leaderboard[$newkey] = $leaderboard[$key];
            unset($leaderboard[$key]);
        }
        arsort($leaderboard);
        return $leaderboard;
    }

}
?>
