package edu.purdue.maptak.admin;
import java.util.*;

public class TakObject {
    private float Latitude;
    private float Longitude;
    private String UUID;
    private HashMap<String, String> Metadata;
    private int CreatedBy;
    private long CreatedOn;

    public void updateLatitude(float lat){
        Latitude = lat;
    }

    public void updateLongitude(float lng){
        Longitude = lng;
    }

    public float getLatitude(){
        return Latitude;
    }

    public float getLongitude(){
        return Longitude;
    }

    public void put(String str1, String str2){

    }

    public String get(String str){

    }

    public List<String> getAllMeta(){

    }
}
