<?php
class User extends BaseModel{
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
        if(!$this->exists()) return array("loggedin"=>false);

        $getPassCmd = "Select password from user where email=?";
        $arr = array($this->POST("email"));
        $pass = $this->execute($getPassCmd, $arr)->fetchAll()[0]['password'];

        if(!password_verify($this->POST("password"), $pass)) return array("loggedin"=>false);

        return array("loggedin"=>true, "email"=>$this->POST("email"));
    }

    public function register(){
        if($this->exists()) return false;
        if(!$this->hasParams(array("email", "phone", "password"))) return false;

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
        // TODO: Implement password reset
        return true;
    }
}
