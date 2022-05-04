<?php

function UNIT_TEST_assert_handler($file, $line, $code)
{
    echo "<hr>Assertion Failed:
        File '$file'<br />
        Line '$line'<br />
        Code '$code'<br /><hr />";
}

function UNIT_TEST_RUN_SUITE() {
    //Start assert functionality, disable default warnings due to our own implementation, stop exection on fail, link our assert_handler
    assert_options(ASSERT_ACTIVE, 1);
    assert_options(ASSERT_WARNING, 0);
    assert_options(ASSERT_QUIET_EVAL, 1);
    assert_options(ASSERT_BAIL, 1);
    assert_options(ASSERT_CALLBACK, 'UNIT_TEST_assert_handler');

    UNIT_TEST_Controller();


}

function UNIT_TEST_Controller() {
    $TEST_Controller = new Controller();

    //Run tests on dummy Controller, Controller will call on Authentication, ProfileManager, and DB testing all these classes.
    //Check login works by logging in with test account and checking session is active with that account
    assert('$_SESSION["username"] != "TEST_username"');
    $TEST_Controller->login('TEST_username', 'Test@1234');
    assert('$_SESSION["username"] = "TEST_username"');

    //Check logout works by logging out with test account and checking session is NOT active with that account
    $TEST_Controller->logOut('TEST_username', 'Test@1234');
    assert('$_SESSION["username"] != "TEST_username"');

    //Check Authentication with negative test of non-existent Account
    $TEST_Controller->login('TEST_NOT_REAL_username', 'Test@1234');
    assert('$_SESSION["username"] != "TEST_NOT_REAL_username"');

    //Check Delete function works with negative test
    $TEST_Controller->deleteAccount('TEST_username');
    $TEST_Controller->login('TEST_username', 'Test@1234');
    assert('$_SESSION["username"] != "TEST_username"');

    //Check register function of account by loggin in after creating the account
    $TEST_UserProfile = new UserProfile('Testing', 'Account', 'CryptoAdvantageTestAccount1@gmail.com', 'TEST_username_before_updating','Test@1234');
    $TEST_Controller->register($TEST_UserProfile);
    $TEST_Controller->login('TEST_username_before_updating', 'Test@1234');
    assert('$_SESSION["username"] = "TEST_username_before_updating"');

    //Check update functionality works by setting our test account back to original state
    $TEST_Controller->logOut('TEST_username_before_updating', 'Test@1234');
    assert('$_SESSION["username"] != "TEST_username_before_updating"');
    $TEST_Controller->updateAccount($TEST_UserProfile, array('username'=>'TEST_username'));
    $TEST_Controller->login('TEST_username', 'Test@1234');
    assert('$_SESSION["username"] = "TEST_username"');

    //Check sanitize function is working as expected by simulating a XSS attack, need to visually check
    $TEST_Controller->login('<script>alert("XSS")</script>', '');
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
?>
