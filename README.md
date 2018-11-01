![Logo](https://i.imgur.com/jznnJqy.png)

# PayFlow

[Visit our website](http://www.andreasglordos.wixsite.com/payflow)

Forget ATMs. You can now conduct any payment, to anyone, from anywhere at any time using PayFlow.

PayFlow uses SMS to transfer funds from your accounts to the accounts of merchants, family or friends. It's easy to use, easy to set up and will make your life much easier.

In third-world countries, PayFlow can be especially helpful, as many people lack access to Internet access and/or smartphones, and thus are missing out from the convenient world of mobile payments. 

PayFlow removes that barrier of entry by being able to work on any phone, as long as it can send and receive SMS. That way, no matter what phone you have, the network condition you're in and what phone your friend has, you can still transfer money effortlessly.

# Installation

### Note: this has only been tested on Windows.

1. [Install Python 3.5](https://www.python.org/downloads/release/python-350/) if you don't have it already

2. pip install django

3. Download this repository and unzip it.

4. Open up cmd. Navigate to the repository you downloaded and go to the Payflow folder, where you can find manage.py. Execute the command python manage.py runserver

5. A message should appear on the cmd with the IP of your web server. It should look like this: 127.0.0.1:xxxx/ . Note down the four digits at the end.

6. Open an instance of a Git Bash terminal. Type the command ssh -R 80:localhost:xxxx serveo.net, where xxxx are the 4 digits you noted down in Step 5.

7. Note down the URL received from the step above.

8. Go to http://www.telerivet.com and click on "Get Started" on the top right. Sign up and go through the first two steps of their signup process (ignore the 3rd step, "Set up your messaging services or campaigns"). Make sure to download and configure the Android app as explained in the setup process of Telerivet.

9. On the telerivet dashboard, click Services on the left. Click on Webhook API. Go through the set up process. Copy down your Webhook secret, and put the URL you received in step 7 as your Webhook URL.

# Usage

There's two ways to make and receive payments. One way is to text an SMS to the gateway phone (the device you downloaded Telerivet on), and go through the registration process to provide access to the system through the Bank of Cyprus API.

Make sure you register before carrying out the following steps:

## Method 1: Receive money through SMS only

1. Send a text to the gateway phone specifying how much money you would like to receive (e.g. "I would like to receive 20 euros from my friend"). Anything you send will work, as long as you imply you intend to receive money and specify the amount of money you would like to receive.

2. You should receive a text back with a 6 digit pin. Send or show that 6 digit pin to your friend/family who will pay you money.

![FirstImage](https://i.imgur.com/VWWTiEp.png)

3. Your friend or family must send a text message to the gateway phone with the 6 digit pin.

## Method 2: Receive money through the Merchant application

If you're a merchant, it might seem a bit tedious/slow to go through all the steps mentioned above - don't worry, as we created an app that automates the process for you.

1. Launch the Merchant app found in the repository on an Android phone.

2. Type the amount you would like to receive from your customer.

![Image](https://i.imgur.com/N6fOTSt.png)

3. Show the customer the code that appears on your screen. The cusstomer should text the gateway phone the code.

![Image2](https://i.imgur.com/GSDH0Io.png)
