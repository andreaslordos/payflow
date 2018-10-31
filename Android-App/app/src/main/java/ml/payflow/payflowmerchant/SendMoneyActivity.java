package ml.payflow.payflowmerchant;

import android.content.Intent;
import android.provider.Telephony;
import android.support.design.widget.FloatingActionButton;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.ActivityOptionsCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import static java.lang.Math.min;

public class SendMoneyActivity extends AppCompatActivity {
    int amount = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_send_money);
        Button b0 = findViewById(R.id.button_0);
        Button b1 = findViewById(R.id.button_1);
        Button b2 = findViewById(R.id.button_2);
        Button b3 = findViewById(R.id.button_3);
        Button b4 = findViewById(R.id.button_4);
        Button b5 = findViewById(R.id.button_5);
        Button b6 = findViewById(R.id.button_6);
        Button b7 = findViewById(R.id.button_7);
        Button b8 = findViewById(R.id.button_8);
        Button b9 = findViewById(R.id.button_9);
        Button b00 = findViewById(R.id.button_00);
        ImageView bs = findViewById(R.id.backspace);
        FloatingActionButton fab = findViewById(R.id.fab);
        final TextView amountView = findViewById(R.id.moneyView);
        b0.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(0)));
            }
        });
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(1)));
            }
        });
        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(2)));
            }
        });
        b3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(3)));
            }
        });
        b4.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(4)));
            }
        });
        b5.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(5)));
            }
        });
        b6.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(6)));
            }
        });
        b7.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(7)));
            }
        });
        b8.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(8)));
            }
        });
        b9.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amountView.setText(String.valueOf(amountToString(9)));
            }
        });
        bs.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amount = amount/10;
                amountView.setText(String.valueOf(amountToString(-1)));
            }
        });
        bs.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View view) {
                amount = 0;
                amountView.setText(amountToString(-1));
                return false;
            }
        });
        b00.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                amount *=10;
                amountView.setText(amountToString(0));

            }
        });

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendSMS("+35799795260", "Generate code for "+amountToString(-1));
                presentActivity(view);
            }
        });

    }
    String amountToString(int add){
        if(add!=-1) {
            amount *=10;
            amount+=add;
        }
        amount = amount%100000;
        return String.format("%.2f", (amount/100.0));
    }

    public void sendSMS(String phoneNo, String msg) {
        try {
            SmsManager smsManager = SmsManager.getDefault();
            smsManager.sendTextMessage(phoneNo, null, msg, null, null);
//            Toast.makeText(getApplicationContext(), "Message Sent",
//                    Toast.LENGTH_LONG).show();
        } catch (Exception ex) {
            Toast.makeText(getApplicationContext(),ex.getMessage().toString(),
                    Toast.LENGTH_LONG).show();
            ex.printStackTrace();
        }
    }
    public void presentActivity(View view) {
        ActivityOptionsCompat options = ActivityOptionsCompat.
                makeSceneTransitionAnimation(this, view, "transition");
        int revealX = (int) (view.getX() + view.getWidth() / 2);
        int revealY = (int) (view.getY() + view.getHeight() / 2);

        Intent intent = new Intent(getApplicationContext(), ViewTransactionNumberActivity.class);
        intent.putExtra(ViewTransactionNumberActivity.EXTRA_CIRCULAR_REVEAL_X, revealX);
        intent.putExtra(ViewTransactionNumberActivity.EXTRA_CIRCULAR_REVEAL_Y, revealY);

        ActivityCompat.startActivity(this, intent, options.toBundle());
    }

    @Override
    protected void onResume() {
        super.onResume();

        final String myPackageName = getPackageName();
        if (!Telephony.Sms.getDefaultSmsPackage(this).equals(myPackageName)) {
            // App is not default.
            // Show the "not currently set as the default SMS app" interface
            Intent intent =
                    new Intent(Telephony.Sms.Intents.ACTION_CHANGE_DEFAULT);
            intent.putExtra(Telephony.Sms.Intents.EXTRA_PACKAGE_NAME,
                    myPackageName);
            startActivity(intent);
        } else {
            // App is the default.
            // Hide the "not currently set as the default SMS app" interface
        }
    }
}
