<?php

    $senderbank = $_GET['send'];
    $receiverbank = $_GET['receive'];
    $subscription = $_GET['sub'];
    $amount = $_GET['amount'];


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

$accesstoken = substr($response, 41, 202);


$curl = curl_init();
echo $accesstoken;
echo "<br>";

curl_setopt_array($curl, array(
  CURLOPT_URL => "https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/jwssignverifyapi/sign",
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
  CURLOPT_POSTFIELDS => '{
  "debtor": {
    "bankId": "",
    "accountId": "$senderbank"
  },
  "creditor": {
    "bankId": "",
    "accountId": "$receiverbank"
  },
  "transactionAmount": {
    "amount": $amount,
    "currency": "EUR",
    "currencyRate": "string"
  },
  "endToEndId": "string",
  "paymentDetails": "test sandbox ",
  "terminalId": "string",
  "branch": "",
   "executionDate": "",
  "valueDate": ""
}
',
  CURLOPT_HTTPHEADER => array(
    "tppId: singpaymentdata",
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

echo $response;
?>