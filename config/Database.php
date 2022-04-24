<?php
    class Database{
        private $conn;
    
        private $hostname;
        private $username;
        private $password;
        private $database;


        public function __construct(){   
            ///////////////////////////////////////////////////   
            ////    CODE for when the database is hosted   ////
            ///////////////////////////////////////////////////   

            $url = getenv('JAWSDB_URL');
            $dbparts = parse_url($url);
            $this->hostname = $dbparts['host'];
            $this->username = $dbparts['user'];
            $this->password = $dbparts['pass'];
            $this->database = ltrim($dbparts['path'],'/');   
            
            //////////////////////////////////////////////
            ////    Local Dev Code -- Delete Later    ////
            //////////////////////////////////////////////
            //$this->hostname = "localhost";
            // $this->username = "root";
            // $this->password = "";
            // $this->database = "cryptoadvantage";
        }

        public function connect(){          
            try {
                $this->conn = new PDO("mysql:host=" . $this->hostname . ";dbname=" . $this->database, $this->username, $this->password);

                $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                return $this->conn;
            }
            catch(PDOException $e)
            {
                echo "Connection failed: " . $e->getMessage();
            }            
        }
    }