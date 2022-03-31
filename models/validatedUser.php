<?php
class validatedUser extends User{
    public function __construct($db, $email){
        parent::__construct($db);
        $this->email = $email;
    }

    public function resetPassword(){
        // TODO: Implement password reset
        return true;
    }
}
