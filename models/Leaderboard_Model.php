<?php

include_once __DIR__ . "/BaseModel.php";
class Leaderboard extends BaseModel{

    public function __construct(){
        parent::__construct();
    }

    public function getLeaderboard() {
        $cmd = "SELECT * FROM ";
        $arr = array($this->POST("email"), $this->convertPhone(), password_hash($this->POST("password"), PASSWORD_DEFAULT));

        $this->execute($cmd, $arr);
    }

}
?>
