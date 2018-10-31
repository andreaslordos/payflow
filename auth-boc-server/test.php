<?php

$curl = curl_init();

echo "<br><br><br><br>";
echo $patchthing;
echo "<br><br><br><br>";

curl_setopt_array($curl, array(
  CURLOPT_URL => "http://1b3e33fa.ngrok.io/application/",
  CURLOPT_ENCODING => "",
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 30000,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => "POST",
));

$response = curl_exec($curl);
$err = curl_error($curl);

curl_close($curl);

if ($err) {
  echo "cURL Error #:" . $err;
} else {
  echo $response;
}



?>