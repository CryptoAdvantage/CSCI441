<?php
class User extends BaseModel{
    private $loggedIn = false;

    public function __construct($db){
        parent::__construct($db);   
    }

    public function exists(){
        return $this->hasData("Select * from user where email=?", array($this->POST("email")));
    }

    public function isLogInAttempt(){
        return $this->hasParams(array("email", "password"));
    }

    public function logIn(){
        if($this->loggedIn) return true;
        if(!$this->exists()) return false;

        $cmd = "Select * from user where email=? and password=?";
        $arr = array($this->POST("email"), $this->POST("password"));
        
        $this->loggedIn = $this->hasData($cmd, $arr);
        return $this->loggedIn;
    }

    public function logOut(){
        $this->loggedIn = false;
    }

    public function register(){
        if($this->exists()) return false;        
        if(!$this->hasParams(array("email", "phone", "password"))) return false;

        $cmd = "Insert into user (`email`, `phone`, `SecurityKey`, `password`) values (?,?,'AutoValue',?)";
        $arr = array($this->POST("email"), $this->convertPhone(),$this->POST("password"));
               
        $this->execute($cmd, $arr);

        return true;
    }

    private function convertPhone(){
        $phone = $this->POST("phone");
        return str_replace("-","", $phone);
    }

    public function resetPassword(){
        // TODO: Implement password reset
        return true;
    }
}