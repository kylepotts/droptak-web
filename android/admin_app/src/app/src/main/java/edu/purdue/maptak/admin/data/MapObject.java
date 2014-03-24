package edu.purdue.maptak.admin.data;

import android.content.Context;

import java.util.LinkedList;
import java.util.List;
import java.util.UUID;

/** Encapsulates all of the information for a single Map
 *  MapObjects are immutable, which means they cannot be edited once they are created.
 *
 *      CREATING A BRAND NEW MAP
 *      1) Create your MapObject m = new MapObject(...).
 *         you don't have to pass in a MapID, as it isn't known at this point.
 *      2) Get a MapTakDB object and call db.addMap(). Pass in the map you just created.
 *
 *      ADDING TAKS TO A MAP
 *      1) Create an appropriate Tak object
 *      2) Get a MapTakDB object and call db.addTak(). Pass in the tak and the mapID in this class.
 *      3) Call db.getMap(). Pass in the mapID you want. It will give you a new MapObject with the
 *          Tak you just added.
 */

public class MapObject {

    /** A label the user has supplied for the map */
    private String label;

    /** A unique ID that can identify each map */
    private MapID mapID;

    /** List of Taks that are related to the map */
    private List<TakObject> takList;

    /** List of Managers */
    private List<String> managerList;

    /** Map created by the backend. MapID is known. */
    public MapObject(String label, MapID id, List<TakObject> taks) {
        this.label = label;
        this.mapID = id;
        this.takList = taks;
        this.managerList = new LinkedList<String>();
    }

    /** Map created from the app/user. mapID is generated randomly until a sync with the server. */
    public MapObject(String label, List<TakObject> taks) {
        this(label, new MapID(UUID.randomUUID().toString().substring(0,12)), taks);
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

}
