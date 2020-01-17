package org.tensorflow.demo;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

public class MainActivity extends Activity implements View.OnClickListener {

    //Declaration Button
    Button btnClickMe;
    //final ListView helloListView = (ListView) findViewById(R.id.list1);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(R.layout.calories);
        //Intialization Button

        btnClickMe = (Button) findViewById(R.id.foodSavingButton);
        btnClickMe.setOnClickListener(this);
        Log.d("11111111111", "11111111111");

        //Here MainActivity.this is a Current Class Reference (context)
    }
    @Override
        public void onClick (View v) {

        // OverlayView test = (OverlayView) findViewById(R.id.test;
        //  test.setText(getTitle()+"      "+calories(getTitle()));
        startActivity(new Intent(this, CaloriesActivity.class));
        setContentView(R.layout.calories);
        //TextView hell = (TextView) findViewById((R.id.txt6));
        String newmsg = getTitle() + "      " + calories(getTitle().toString());
        //hell.setText(newmsg);
        //helloListView.addHeaderView(hell);
    }

    public String calories(String title){
        String cal="";

        if (title.equals( "Apple")){
            cal = "52";
        }
        if (title.equals("Banana")){
            cal = "89";
        }
        if (title.equals("Orange")){
            cal = "47";
        }
        if (title.equals("Peach")){
            cal = "39";
        }
        if (title.equals("Lemon")){
            cal = "29";
        }

        return cal;
    }

}
