package edu.purdue.maptak.admin.data;

import android.content.Context;

import java.util.LinkedList;
import java.util.List;

/** Encapsulates all of the information for a single Map */
public class MapObject {

    /** Context which the mapobject exists in. */
    private Context context;

    /** A label the user has supplied for the map */
    private String label;

    /** A unique ID that can identify each map */
    private MapID mapID;

    /** List of Taks that are related to the map */
    private List<TakObject> takList;

    /** List of Managers */
    private List<String> managerList;

    /** Map created by the backend. MapID is known. */
    public MapObject(Context c, String label, MapID id, List<TakObject> taks) {
        this.context = c;
        this.label = label;
        this.mapID = id;
        this.takList = taks;
        this.managerList = new LinkedList<String>();
    }

    /** Map created from the app/user. mapID is null. privateKey is null. requireKey is idk! */
    public MapObject(Context c, String label, List<TakObject> taks) {
        this(c, label, null, taks);
    }

    /** Returns the label for the map */
    public String getLabel() {
        return this.label;
    }

    /** Returns the ID for the map */
    public MapID getID() {
        return this.mapID;
    }

    /** Returns the TakList backing this map */
    public List<TakObject> getTakList() {
        return this.takList;
    }

    /** Receives input from the Tak class and adds that Tak to the Map */
    public void addTak(TakObject tak) {
        MapTakDB db = new MapTakDB(context);
        db.addTak(tak, this.mapID);
        this.takList = db.getTaks(this.mapID);
    }

    /** Gives the input from Tak class and removes the given Tak */
    public void removeTak(TakID tak) {
        MapTakDB db = new MapTakDB(context);
        db.removeTak(tak, this.mapID);
        this.takList = db.getTaks(this.mapID);
    }

}
