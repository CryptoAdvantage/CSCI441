<?php
include_once dirname(__DIR__, 1) . "/config/Database.php";
if(session_id() == "") session_start();

class BaseModel{
    private $db;

    public function __construct(){
        $x = new Database();
        $this->db = $x->connect();
    }

    public function GET($label){
        return isset($_GET[$label]) ? htmlspecialchars(strip_tags($_GET[$label])) : null;
    }

    public function POST($label){
        return isset($_POST[$label]) ? htmlspecialchars(strip_tags($_POST[$label])) : null;
    }

    public function SESSION($label){
        return isset($_SESSION[$label]) ? htmlspecialchars(strip_tags($_SESSION[$label])) : null;
    }

    public function hasParams($params){
        for($i = 0; $i < count($params); $i++){
            if($this->GET($params[$i])== null && $this->POST($params[$i])== null) return false;
        }

        return true;
    }

    public function execute($query, $params = array()){
        $stmt = $this->db->prepare($query);
        for($i = 1; $i <= count($params); $i++){
            $stmt->bindParam($i, $params[$i-1]);
        }
        $stmt->execute();
        return $stmt;
    }

    public function executeString($query, $params = array()){
        $stmt = $this->db->prepare($query);
        foreach($params as $id => $param){
            $stmt->bindValue($id, $param, PDO::PARAM_STR);
        }
        $stmt->execute();
        return $stmt;
    }

    public function hasData($query, $params = array()){
        return $this->execute($query, $params)->rowCount() > 0;
    }

    public function getInsertId(){
        return $this->db->lastInsertId();
    }
}
