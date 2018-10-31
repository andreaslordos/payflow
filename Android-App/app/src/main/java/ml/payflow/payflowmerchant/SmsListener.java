package ml.payflow.payflowmerchant;


import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.provider.Telephony;
import android.support.annotation.RequiresApi;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.ActivityOptionsCompat;
import android.telephony.SmsMessage;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

public class SmsListener extends BroadcastReceiver {

    private static final String SMS_RECEIVED = "android.provider.Telephony.SMS_RECEIVED";

    @Override
    public void onReceive(Context context, Intent intent) {

        Log.d("ON ","RECEIVE");
        Bundle bundle = intent.getExtras();
        Object[] messages = (Object[]) bundle.get("pdus");
        SmsMessage[] sms = new SmsMessage[messages.length];
        // Create messages for each incoming PDU
        for (int n = 0; n < messages.length; n++) {
            sms[n] = SmsMessage.createFromPdu((byte[]) messages[n]);
        }
        for (SmsMessage msg : sms) {
            if(msg.getOriginatingAddress().contains("99795260")){
                if(msg.getMessageBody().startsWith("To get ")){
                    String code = msg.getMessageBody().split(" ")[13];
                    ViewTransactionNumberActivity.code.setText(code);
                    ViewTransactionNumberActivity.code.setVisibility(View.VISIBLE);
                    ViewTransactionNumberActivity.progressBar.setVisibility(View.INVISIBLE);
                    ViewTransactionNumberActivity.done.setVisibility(View.INVISIBLE);
                    ViewTransactionNumberActivity.hint.setText("To get money from your friend, they should send this code to +35799795260");
                }
                else if(msg.getMessageBody().startsWith("Transfer from ")){
                    ViewTransactionNumberActivity.code.setVisibility(View.INVISIBLE);
                    ViewTransactionNumberActivity.progressBar.setVisibility(View.INVISIBLE);
                    ViewTransactionNumberActivity.done.setVisibility(View.VISIBLE);
                    ViewTransactionNumberActivity.hint.setText(msg.getMessageBody());

                }
            }
            Log.e("RECEIVED MSG",":"+msg.getMessageBody());
            // Verify if the message came from our known sender

        }
        }
    public void presentActivity(View view) {
        ActivityOptionsCompat options = ActivityOptionsCompat.
                makeSceneTransitionAnimation(ViewTransactionNumberActivity.context, view, "transition");
        int revealX = (int) (view.getX() + view.getWidth() / 2);
        int revealY = (int) (view.getY() + view.getHeight() / 2);

        Intent intent = new Intent(ViewTransactionNumberActivity.context, DoneActivity.class);
        intent.putExtra(ViewTransactionNumberActivity.EXTRA_CIRCULAR_REVEAL_X, revealX);
        intent.putExtra(ViewTransactionNumberActivity.EXTRA_CIRCULAR_REVEAL_Y, revealY);

        ActivityCompat.startActivity(ViewTransactionNumberActivity.context, intent, options.toBundle());
    }
}