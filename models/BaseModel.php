<?php
class BaseModel{
    private $conn;

    public function __construct($db){
        $this->conn = $db;       
    }

    public function GET($label){
        return isset($_GET[$label]) ? htmlspecialchars(strip_tags($_GET[$label])) : null;
    }

    public function POST($label){
        return isset($_POST[$label]) ? htmlspecialchars(strip_tags($_POST[$label])) : null;
    }

    public function hasParams($params){
        for($i = 0; $i < count($params); $i++){
            if($this->GET($params[$i])== null && $this->POST($params[$i])== null) return false;
        }

        return true;
    }

    public function execute($query, $params = array()){        
        $stmt = $this->conn->prepare($query);
        for($i = 1; $i <= count($params); $i++){
            $stmt->bindParam($i, $params[$i-1]);
        }
        $stmt->execute();
        return $stmt;  
    }

    public function hasData($query, $params = array()){
        return $this->execute($query, $params)->rowCount() > 0;
    }

    private function convertToArray($result){
        $arr = array();
        $keys = null;

        while($row = $result->fetch(PDO::FETCH_ASSOC)){
            if($keys == null){$keys = array_keys($row);}

            $item;
            for($i = 0; $i < count($row); $i++){
                $item[$keys[$i]] = $row[$keys[$i]];
            }

            array_push($arr, $item);
        }

        return $arr;
    }

    public function getInsertId(){
        return $this->conn->lastInsertId();
    }
}