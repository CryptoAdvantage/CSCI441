<?php
include_once "../models/User.php";

function UNIT_TEST_assert_handler($file, $line, $code)
{
    echo "<hr>Assertion Failed:
        File '$file'<br />
        Line '$line'<br />
        Code '$code'<br /><hr />";
}

function UNIT_TEST_RUN_SUITE() {
    //Start assert functionality, disable default warnings due to our own implementation, stop exection on fail, link our assert_handler
    assert_options(ASSERT_ACTIVE, true);
    assert_options(ASSERT_WARNING, false);
    assert_options(ASSERT_BAIL, true);
    assert_options(ASSERT_CALLBACK, 'UNIT_TEST_assert_handler');

    UNIT_TEST_User();
    UNIT_TEST_TradingBot();

}

function UNIT_TEST_User() {
    //Disable warning messages as we will be calling variables which shouldnt exist as part of negative testing.
    //Will be enalbed again after function finishes
    error_reporting(E_ERROR | E_PARSE);
    session_destroy();
	session_start();
    $TEST_User = new User();
	$_POST["email"] = "test1@cryptoadvantage.com";
    $_POST["password"] = "Test@1234";
	$_POST["phone"] = "555-555-5555";

    //Check login works by logging in with test account and checking session is active with that account
    $TEST_register = $TEST_User->register();
    assert($TEST_register = true);

    assert($_SESSION["loggedin"] != true);
    $may = $TEST_User->logIn();

    assert($_SESSION["loggedin"] = true);
    echo "Login User Test Passed! <br>";

    //Check logout works by logging out with test account and checking session is NOT active with that account
	session_destroy();
	session_start();
	assert($_SESSION["loggedin"] != true);
    echo "Logout User Test Passed! <br>";

    //Check Authentication with negative test of non-existent Account
	$_POST["email"] = "testFAKE1@cryptoadvantage.com";
	$_POST["password"] = "Test@1234";
    $TEST_User->login();
    assert($_SESSION["loggedin"] != true);
	session_destroy();
	session_start();
    echo "Negative Login User Test Passed! <br>";

    //Check update functionality works by setting our test account back to original state
	$_POST["email"] = "test1@cryptoadvantage.com";
	$_POST["password"] = "Test@1234";
	$_POST["currentPassword"] = "Test@1234";
	$_POST["newPassword"] = "Test@12345";
	$TEST_User->resetPassword(true);
    session_destroy();
    session_start();
	$_POST["password"] = "Test@12345";
    $TEST_User->login();
    assert($_SESSION["loggedin"] = true);
	session_destroy();
	session_start();
    echo "Update User Test Passed! <br>";

	//Check Delete function works with negative test
	$_POST["email"] = "test1@cryptoadvantage.com";
	$_POST["password"] = "Test@12345";
    $TEST_User->deleteAccount(true);
    session_destroy();
    session_start();
    $TEST_User->login();
    assert($_SESSION["loggedin"] != true);
	session_destroy();
	session_start();
    echo "Delete User Test Passed! <br>";

    //Check sanitize function is working as expected by simulating a XSS attack, need to visually check
	$_POST["email"] = '<script>alert("XSS")</script>';
	$_POST["password"] = "test@1234";
	$TEST_User->login();
	session_destroy();
	session_start();
    echo "Auth Sanitization Test Passed! <br>";

	echo "All User Tests Passed! <br>";
    error_reporting(E_ALL);

}

function UNIT_TEST_TradingBot() {
    echo "Testing Trading Bot";
    $email = "zach@cryptoadvantage.com";
    $posted = (array_key_exists("bot", $_POST)) ? "true" : "false";
    $botName = (array_key_exists("bot", $_POST)) ? $_POST["bot"] : "Test1";
    $exchange = (array_key_exists("exchange", $_POST)) ? $_POST["exchange"] : "Binanceus";
    $token1 = (array_key_exists("token1", $_POST)) ? $_POST["token1"] : "BTC";
    $token2 = (array_key_exists("token2", $_POST)) ? $_POST["token2"] : "USD";
    $interval = (array_key_exists("interval", $_POST)) ? $_POST["interval"] : "1h";
    $strategy = (array_key_exists("strategy", $_POST)) ? $_POST["strategy"] : "bb";
    exec("python ../tradingBot/mainTest.py $botName $exchange $token1 $token2 $interval $strategy $posted $email", $output);
    foreach($output as $blah){
        echo $blah;
    }
}

UNIT_TEST_RUN_SUITE();
?>
