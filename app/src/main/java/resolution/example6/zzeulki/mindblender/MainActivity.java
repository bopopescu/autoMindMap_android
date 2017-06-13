package resolution.example6.zzeulki.mindblender;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private Button recordBtn;
    private TextView speechView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recordBtn = (Button) findViewById(R.id.recordBtn);
        speechView = (TextView) findViewById(R.id.speechView);

        //api 연동
        recordBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){

            }
        });

    }

    /*public void onClickLisenter(View v){

        switch (v.getId()){
            case R.id.recordBtn :
        }

    }*/
}
