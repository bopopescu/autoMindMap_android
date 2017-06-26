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
import com.google.cloud.speech.v1.RecognitionAudio;
import com.google.cloud.speech.v1.RecognitionConfig;
import com.google.cloud.speech.v1.RecognizeResponse;
import com.google.cloud.speech.v1.SpeechRecognitionAlternative;
import com.google.cloud.speech.v1.SpeechRecognitionResult;
import com.google.common.io.Files;
import com.google.protobuf.ByteString;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private Button recordBtn;
    private TextView speechView;
    private String getText;
    private SpeechClient speech;
    private String saveAudioFileName;
    private File saveAudioFile;
    private boolean checkClick = true;

    private static final String LOG_TAG = "AudioRecordTest";
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;

    private MediaRecorder mRecorder = null;


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

        //speech to text
        try {
            speech = SpeechClient.create();
        } catch (IOException e) {

            Log.i("Error","speech create");
            e.printStackTrace();
        }

        saveAudioFile = new File(saveAudioFileName);

        // Reads the audio file into memory
        byte[] data = new byte[0];
        try {
            data = Files.toByteArray(saveAudioFile);
        } catch (IOException e) {
            Log.i("Error","File to byte Array");
            e.printStackTrace();
        }
        ByteString audioBytes = ByteString.copyFrom(data);

        // Builds the sync recognize request
        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setEncoding(RecognitionConfig.AudioEncoding.LINEAR16)
                .setSampleRateHertz(16000)
                .setLanguageCode("ko-KR")
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder()
                .setContent(audioBytes)
                .build();

        // Performs speech recognition on the audio file
        RecognizeResponse response = speech.recognize(config, audio);
        List<SpeechRecognitionResult> results = response.getResultsList();

        for (SpeechRecognitionResult result: results) {
            List<SpeechRecognitionAlternative> alternatives = result.getAlternativesList();
            for (SpeechRecognitionAlternative alternative: alternatives) {
                //System.out.printf("Transcription: %s%n", alternative.getTranscript());
                getText = alternative.getTranscript();
            }
        }
        try {
            speech.close();
            checkResult = true;
        } catch (Exception e) {
            Log.i("Error", "Speech close");
            e.printStackTrace();
        }

        return checkResult;
    }

    /*public void onClickLisenter(View v){

        switch (v.getId()){
            case R.id.recordBtn :
        }

    }*/

    @Override
    public void onStop() {
        super.onStop();
        if (mRecorder != null) {
            mRecorder.release();
            mRecorder = null;
        }
    }
}
