<?php

$curl = curl_init();

$clientid = "7461dc28-b96e-44de-b898-7f10d0829f8b";
$clientsecret = "jK2fF3vS0qR5aR2aM5yE0hS8dT8eD8rE1sW3jQ2mQ4iK5dB2rN";

curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/oauth2/token",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "client_id=$clientid&client_secret=$clientsecret&grant_type=client_credentials&scope=TPPOAuth2Security",
  CURLOPT_HTTPHEADER => array(
    "accept: application/json",
    "content-type: application/x-www-form-urlencoded"
  ),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
    http_response_code(401);
    die("cURL Error #:" . $err);
}


$curl = curl_init();
$accesstoken = substr($response, 41, 202);
echo $accesstoken;
echo "|";
curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/v1/subscriptions?client_id=$clientid&client_secret=$clientsecret",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "{\"accounts\":{\"transactionHistory\":true,\"balance\":false,\"details\":false,\"checkFundsAvailability\":true},\"payments\":{\"limit\":99999999999,\"currency\":\"EUR\",\"amount\":99999999999}}",
  CURLOPT_HTTPHEADER => array(
    "accept: application/json",
    "app_name: payflow",
    "authorization: Bearer $accesstoken",
    "content-type: application/json",
    "journeyid: abc",
    "lang: en",
    "originuserid: 50520218",
    "timestamp: 0",
    "tppid: singpaymentdata"
  ),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  die("cURL Error #:" . $err);
}
$subid = substr($response, 80, 25);
echo $subid;