<?php
class validatedUser extends User{
    public function __construct($email, $userID, $phone, $permission){
        parent::__construct();
        $this->email = $email;
        $this->userID = $userID;
        $this->phone = $phone;
        $this->permission = $permission;
    }

    public function getTradeHistory($db)
    {
        $cmd = "SELECT c1.Ticker, c2.Ticker, e.Name, p.Date, p.Open, t.Action, t.Quantity FROM tradehistory t INNER JOIN tradepair c ON t.PairID = c.ID INNER JOIN cryptocurrency c1 ON c.FirstPairID = c1.ID INNER JOIN cryptocurrency c2 ON c.SecondPairID = c2.ID INNER JOIN exchange e ON t.ExchID = e.ID INNER JOIN pricehistory p ON t.PriceID = p.ID WHERE t.UserID=? ORDER BY p.Date DESC;";
        $arr = array($this->userID);
        //$arr = array(5);
        $tradeData = $this->execute($db, $cmd, $arr)->fetchAll();

        return $tradeData;
    }

    public function resetPassword(){
        // TODO: Implement password reset
        return true;
    }
}
