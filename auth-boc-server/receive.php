<?php

$curl = curl_init();

$clientid = "7461dc28-b96e-44de-b898-7f10d0829f8b";
$clientsecret = "jK2fF3vS0qR5aR2aM5yE0hS8dT8eD8rE1sW3jQ2mQ4iK5dB2rN";
$access1 = $_GET['code'];
$initialaccess = $_COOKIE['oath'];
curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/oauth2/token",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "client_id=$clientid&client_secret=$clientsecret&grant_type=authorization_code&scope=UserOAuth2Security&code=$access1",
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
//echo "<br>";
//echo $response;
//echo "<br>";


$curl = curl_init();
$accesstoken = substr($response, 41, 159);
$subid = $_COOKIE['secret'];
//die();
curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/v1/subscriptions/$subid?client_id=$clientid&client_secret=$clientsecret",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "GET",
  CURLOPT_POSTFIELDS => "",
  CURLOPT_HTTPHEADER => array(
    "Authorization: Bearer $initialaccess",
    "content-type: application/json",
    "journeyId: abc",
    "originUserId: 50520218",
    "timeStamp: 5",
    "tppId: singpaymentdata",
      "APIm-Debug-Trans-Id: true"
  ),
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  die("cURL Error #:" . $err);
}
//$subid = substr($response, 80, 25);

$json = json_decode($response, true);
//echo var_dump($json);
//echo "<br><br><br>";


$curl = curl_init();
$subid = $_COOKIE['secret'];
$phone = $_COOKIE['phone'];
$patchthing = "{" . substr($response, 95);
$patchthing = substr($patchthing, 0, strlen($patchthing)-1);
$bank = $json[0]['selectedAccounts'][0]['accountId'];

echo $bank;
echo "<br><br><br>";
echo $patchthing;

$curl = curl_init();


curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/v1/subscriptions/$subid?client_id=$clientid&client_secret=$clientsecret",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "PATCH",
  CURLOPT_POSTFIELDS => $patchthing,
  CURLOPT_HTTPHEADER => array(
    "accept: application/json",
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

$bank = 1234567;
$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => "http://pepulo.serveo.net/application/",
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => "event='register'&phone='+".substr($phone, 1)."'&bank=$bank&subs=$subid",
));

$response = curl_exec($curl);

//echo "<script>window.location.replace('http://andreasglordos.wixsite.com/payflow');</script>";
