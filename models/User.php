<?php

include_once __DIR__ . "/BaseModel.php";
class User extends BaseModel{
    public $id;
    public $email;
    public $phone;
    public $permission;
    public $password;
    
    public function __construct(){
        parent::__construct();
    }

    public function exists($email){
        return $this->hasData("Select * from user where email=?", array($email));
    }

    public function isLogInAttempt(){
        return $this->hasParams(array("email", "password"));
    }

    public function logIn(){     
        if($this->hasParams(array("email", "password"))){
            $pw = $this->POST("password");
            $email = $this->POST("email");

            $_SESSION["password"] = $pw;
            $_SESSION["email"] = $email;
        } else {
            $pw = $this->SESSION("password");
            $email = $this->SESSION("email");
        }

        if($pw == null || $email == null) return false;
        if(!$this->exists($email)) return false;

        $userData = $this->execute("Select * from user where email=?", array($email))->fetchAll()[0];
        if(!password_verify($pw, $userData['Password'])) return false;

        $this->id = $userData['ID'];
        $this->email = $userData['Email'];
        $this->phone = $userData['Phone'];
        $this->permission = $userData['Permission'];
        $this->password = $userData["Password"];

        $_SESSION["loggedin"] = true;

        return true;
    }

    public function validate(){
        if($this->logIn()) return;

        session_destroy();
        header("Location: ./login.php?error");
        exit;
    }

    public function register(){
        if(!$this->hasParams(array("email", "phone", "password"))) return false;
        if($this->exists($this->POST("email"))) return false;
        
        $cmd = "Insert into user (`email`, `phone`, `SecurityKey`, `password`) values (?,?,'AutoValue',?)";
        $arr = array($this->POST("email"), $this->convertPhone(), password_hash($this->POST("password"), PASSWORD_DEFAULT));

        $this->execute($cmd, $arr);

        return true;
    }

    private function convertPhone(){
        $phone = $this->POST("phone");
        return str_replace("-","", $phone);
    }

    public function resetPassword(){
        if(!$this->hasParams(array("newPassword", "currentPassword"))) return false;        
        if(!password_verify($this->POST("currentPassword"), $this->password)) return false;

        $cmd = "Update user set `Password`=? where `Email`=?";
        $arr = array(password_hash($this->POST("newPassword"), PASSWORD_DEFAULT), $this->email);
        
        $this->execute($cmd, $arr);

        session_destroy();
        header("Location: ./login.php?logout");
        exit;
    }

    public function getTradeHistory(){        
        $cmd = "SELECT c1.Ticker, c2.Ticker, e.Name, p.Date, p.Open, t.Action, t.Quantity FROM tradehistory t INNER JOIN tradepair c ON t.PairID = c.ID INNER JOIN cryptocurrency c1 ON c.FirstPairID = c1.ID INNER JOIN cryptocurrency c2 ON c.SecondPairID = c2.ID INNER JOIN exchange e ON t.ExchID = e.ID INNER JOIN pricehistory p ON t.PriceID = p.ID WHERE t.UserID=? ORDER BY p.Date DESC;";
        $arr = array($this->id);
        return $this->execute($cmd, $arr)->fetchAll();
    }

    public function deleteAccount(){
        if(!$this->hasParams(array("password"))) return false;        
        if(!password_verify($this->POST("password"), $this->password)) return false;

        $cmd = "Update user set `Email`=? where `Email`=?";
        // pseudo account removal - changes the address to the former plus hash
        $arr = array($this->email . $this->password, $this->email);        
        $this->execute($cmd, $arr);

        session_destroy();
        header("Location: ./login.php");
        exit;
    }
}
