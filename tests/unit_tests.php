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


}

function UNIT_TEST_User() {
    $TEST_User = new User();
	$_POST["email"] = "test1@cryptoadvantage.com";
	$_POST["password"] = "Test@1234";
    //Run tests on dummy Controller, Controller will call on Authentication, ProfileManager, and DB testing all these classes.
    //Check login works by logging in with test account and checking session is active with that account
    assert($_SESSION["loggedin"] != true);
    $TEST_User->logIn();
    assert($_SESSION["loggedin"] = true);

    //Check logout works by logging out with test account and checking session is NOT active with that account
	session_destroy();
	session_start();
	assert($_SESSION["loggedin"] != true);


    //Check Authentication with negative test of non-existent Account
	$_POST["email"] = "testFAKE1@cryptoadvantage.com";
	$_POST["password"] = "Test@1234";
    $TEST_User->login();
    assert($_SESSION["loggedin"] != true);
	session_destroy();
	session_start();


    //Check update functionality works by setting our test account back to original state
	$_POST["email"] = "test1@cryptoadvantage.com";
	$_POST["password"] = "Test@1234";
	$_POST["currentPassword"] = "Test@1234";
	$_POST["newPassword"] = "Test@12345";
	$TEST_User->resetPassword();
	$_POST["password"] = "Test@12345";
    $TEST_User->login();
    assert($_SESSION["loggedin"] = true);
	session_destroy();
	session_start();

	//Check Delete function works with negative test
	$_POST["email"] = "test1@cryptoadvantage.com";
	$_POST["password"] = "Test@12345";
    $TEST_User->deleteAccount(true);
    $TEST_User->login();
    assert($_SESSION["loggedin"] != true);
	session_destroy();
	session_start();
	
    //Check sanitize function is working as expected by simulating a XSS attack, need to visually check
	$_POST["email"] = '<script>alert("XSS")</script>';
	$_POST["password"] = "test@1234";
	$TEST_User->login();
	session_destroy();
	session_start();

	echo "All User Tests Passed!";
}

function UNIT_TEST_ExchangeManager() {
    $TEST_ExchangeManager = new ExchangeManager();
    $TEST_FakeBTC = new CryptoCurrency('TEST_FakeBTC');
    $TEST_FakeETH = new CryptoCurrency('TEST_FakeETH');
    $TEST_FakeUSD = new Currency('TEST_FakeUSD');
    $TEST_TradingPair = new TradingPair($TEST_FakeBTC, $TEST_FakeETH);
    $TEST_Exchange = new Exchange($TEST_FakeUSD, 'TEST_Exchange');
    $TEST_ExchangePair = new ExchangePair($TEST_TradingPair, $TEST_Exchange);

    $TEST_NEGATIVE_FakeDOGE = new CryptoCurrency('TEST_NEGATIVE_FakeDOGE');
    $TEST_NEGATIVE_TradingPair = new TradingPair($TEST_FakeBTC, $TEST_NEGATIVE_FakeDOGE);

    //Run tests on a dummy ExchangeManager, which in turn will test a dummy TradingPair, CryptoCurrency, Exchange, ExchangePair, and Currency

    //Check add pair fucntionality of ExchangeManager
    $TEST_ExchangeManager->addCryptoPair($TEST_TradingPair, $TEST_Exchange);
    assert('$TEST_ExchangeManager->getCryptoPair($TEST_TradingPair, $TEST_Exchange) = $TEST_ExchangePair');

    //Check exists fucntionality of ExchangeManager with positive and negative test
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_TradingPair) = true');
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_NEGATIVE_TradingPair) = false');

    //Check remove pair functionality
    $TEST_ExchangeManager->removeCryptoPair($TEST_ExchangePair);
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_TradingPair) = false');
}

function UNIT_TEST_TradeManager() {
    $TEST_ExchangeManager = new ExchangeManager();
    $TEST_FakeBTC = new CryptoCurrency('TEST_FakeBTC');
    $TEST_FakeETH = new CryptoCurrency('TEST_FakeETH');
    $TEST_FakeUSD = new Currency('TEST_FakeUSD');
    $TEST_TradingPair = new TradingPair($TEST_FakeBTC, $TEST_FakeETH);
    $TEST_Exchange = new Exchange($TEST_FakeUSD, 'TEST_Exchange');
    $TEST_ExchangePair = new ExchangePair($TEST_TradingPair, $TEST_Exchange);

    $TEST_NEGATIVE_FakeDOGE = new CryptoCurrency('TEST_NEGATIVE_FakeDOGE');
    $TEST_NEGATIVE_TradingPair = new TradingPair($TEST_FakeBTC, $TEST_NEGATIVE_FakeDOGE);

    //Run tests on a dummy ExchangeManager, which in turn will test a dummy TradingPair, CryptoCurrency, Exchange, ExchangePair, and Currency

    //Check add pair fucntionality of ExchangeManager
    $TEST_ExchangeManager->addCryptoPair($TEST_TradingPair, $TEST_Exchange);
    assert('$TEST_ExchangeManager->getCryptoPair($TEST_TradingPair, $TEST_Exchange) = $TEST_ExchangePair');

    //Check exists fucntionality of ExchangeManager with positive and negative test
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_TradingPair) = true');
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_NEGATIVE_TradingPair) = false');

    //Check remove pair functionality
    $TEST_ExchangeManager->removeCryptoPair($TEST_ExchangePair);
    assert('$TEST_ExchangeManager->exists($TEST_Exchange, $TEST_TradingPair) = false');
}

UNIT_TEST_RUN_SUITE()
?>
