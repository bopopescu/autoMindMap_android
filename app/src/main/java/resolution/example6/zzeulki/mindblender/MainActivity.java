package resolution.example6.zzeulki.mindblender;


import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.google.cloud.speech.spi.v1.SpeechClient;
import com.google.gson.Gson;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    private Button recordBtn;
    private TextView speechView;
    private String getText;
    private SpeechClient speech;
    //private com.google.cloud.speech.spi.v1beta1.SpeechClient speech;
    private String saveAudioFileName;
    private File saveAudioFile;
    private boolean checkClick = true;

    private static final String LOG_TAG = "AudioRecordTest";
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;

    private MediaRecorder mRecorder = null;
    private static String baseURL = "com.mindBlender.app";


    // Requesting permission to RECORD_AUDIO
    private boolean permissionToRecordAccepted = false;
    private String [] permissions = {android.Manifest.permission.RECORD_AUDIO};

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch (requestCode){
            case REQUEST_RECORD_AUDIO_PERMISSION:
                permissionToRecordAccepted  = grantResults[0] == PackageManager.PERMISSION_GRANTED;
                break;
        }
        if (!permissionToRecordAccepted ) finish();

    }



    private void startRecording() {
        mRecorder = new MediaRecorder();
        mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        mRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        mRecorder.setOutputFile(saveAudioFileName);
        mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);

        try {
            mRecorder.prepare();
        } catch (IOException e) {
            Log.e(LOG_TAG, "prepare() failed");
        }

        mRecorder.start();
    }

    private void stopRecording() {
        mRecorder.stop();
        mRecorder.release();
        mRecorder = null;
    }

    private void onRecord(boolean start) {
        if (start) {
            startRecording();
        } else {
            stopRecording();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);


        recordBtn = (Button) findViewById(R.id.recordBtn);
        speechView = (TextView) findViewById(R.id.speechView);

        //*DB 연동하면 바꿔야하는 부분* : 파일 DB에 저장해야댐
        saveAudioFileName = getExternalCacheDir().getAbsolutePath();
        //saveAudioFileName = "./storage/emulated/0/NPUSH";
        saveAudioFileName += "/audiorecordtest.3gp";


        //api 연동
        recordBtn.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v){

                boolean checkResult = false;


                createAudioFile(checkClick);

                if(checkClick!=true) {
                    if (speechToText(checkResult)) {
                        speechView.setText(getText);
                    }
                    checkClick = true;
                }
                checkClick = false;
            }
        });

    }

    public void createAudioFile(boolean check){

        boolean mStartRecording = check;

        onRecord(mStartRecording);
        if (mStartRecording) {
            Log.i("CHECK","Start");
            recordBtn.setText("Stop recording");
        } else {
            Log.i("CHECK","Stop");
            recordBtn.setText("Start recording");

            //녹음 확인
            /*MediaPlayer mPlayer = new MediaPlayer();
            try {
                mPlayer.setDataSource(saveAudioFileName);
                mPlayer.prepare();
                mPlayer.start();
            } catch (IOException e) {
                Log.e(LOG_TAG, "prepare() failed");
            }*/
        }
    }

    public boolean speechToText(boolean checkResult){

        String callUrl = baseURL+"getAudiofile";

        HttpURLConnection conn = null;
        OutputStream os = null;
        InputStream is = null;
        ByteArrayOutputStream baos = null;
        URL url = null;
        String result ="Fail";

        saveAudioFile = new File(saveAudioFileName);


        try {
            url = new URL(callUrl);
            conn = (HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(2500 * 1000);
            conn.setReadTimeout(200 * 1000);
            conn.setRequestMethod("POST");

            conn.setRequestProperty("Cache-Control", "no-cache");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setRequestProperty("Accept", "application/json");
            conn.setDoOutput(true);
            conn.setDoInput(true);

            Gson gson = new Gson();

            JSONObject job = null;

            job = new JSONObject(gson.toJson(saveAudioFile));


            os = conn.getOutputStream();
            os.write(job.toString().getBytes());
            os.flush();

            int responseCode = conn.getResponseCode();


            switch (responseCode) {
                case 200:
                case 201:
                    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line + "\n");
                    }
                    br.close();

                    result = sb.toString();
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (ProtocolException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            e.printStackTrace();
        }

        if(result.equals("Success")){
            checkResult = true;
        }else{
            checkResult = false;
        }
        return checkResult;

    }

    @Override
    public void onStop() {
        super.onStop();
        if (mRecorder != null) {
            mRecorder.release();
            mRecorder = null;
        }
    }
}
