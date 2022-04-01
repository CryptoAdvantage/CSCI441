<?php
class User extends BaseModel{
    public function __construct(){
        parent::__construct();
    }

    public function exists($db){
        return $this->hasData($db, "Select * from user where email=?", array($this->POST("email")));
    }

    public function isLogInAttempt(){
        return $this->hasParams(array("email", "password"));
    }

    public function logIn($db){
        if(!$this->exists($db)) return array("loggedin"=>false);

        $getPassCmd = "Select * from user where email=?";
        $arr = array($this->POST("email"));
        $userData = $this->execute($db, $getPassCmd, $arr)->fetchAll()[0];
        if(!password_verify($this->POST("password"), $userData['Password'])) return array("loggedin"=>false);

        return array("loggedin"=>true, "Email"=>$userData['Email'], "ID"=>$userData['ID'], "Phone"=>$userData['Phone'], "Permission"=>$userData['Permission']);
    }

    public function register($db){
        if($this->exists($db)) return false;
        if(!$this->hasParams(array("email", "phone", "password"))) return false;

        $cmd = "Insert into user (`email`, `phone`, `SecurityKey`, `password`) values (?,?,'AutoValue',?)";
        $arr = array($this->POST("email"), $this->convertPhone(), password_hash($this->POST("password"), PASSWORD_DEFAULT));

        $this->execute($db, $cmd, $arr);

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
