package resolution.example6.zzeulki.mindblender;

import java.io.File;

/**
 * Created by Zzeulki on 2017. 7. 2..
 */

public class audioSample {

    File audioFile;


    public audioSample(){

    }

    public audioSample(File audioFile){
        this.audioFile = audioFile;
    }

    public void setAudioFile(File audioFile){
        this.audioFile = audioFile;
    }

    public File getAudioFile(){
        return audioFile;
    }


}
