package edu.purdue.maptak.admin.data;

import java.util.LinkedList;
import java.util.List;

/**
 * Created by tylorgarrett on 2/20/14.
 */

public class MapObject {

    /**
     * List of Managers
     */
    List<String> managerList;

    /**
     * List of Taks that are related to the map
     */
    List<TakObject> takList;

    /**
     *
     */
    boolean requireKey;

    /**
     * A unique ID that can identify each map
     */
    MapID mapID;
    TakID takID;
    /**
     * Map created from the app/user. mapID is null. privateKey is null.
     * requireKey is idk!
     */
    public MapObject(){
        managerList = new LinkedList<String>();
        takList = new LinkedList<TakObject>();
        requireKey = true;
        mapID = null;
    }

    /**
     * Receives input from the Tak class and adds that Tak to the Map
     */
    public void addTak( TakID tak ){
        //takList.add();
    }

    /**
     * Gives the input from Tak class and removes the given Tak
     */
    public void removeTak( TakID tak ){
        if ( takList.contains(tak) ){
            takList.remove(tak);
        } else {
            // display error? Tak Not Found
        }
    }

    /**
     * key needs to be the index of the Tak in the list, getTak returns the corresponding Tak
     */
    public TakObject getTakByKey( int key ){
        // return the page that will display details about the Tak
        return takList.get(key);
    }

    /**
     * Receives input from the Manager
     */
    public void addManagers( String manager ){
        managerList.add(manager);
    }

    /**
     * Returns a list of the Managers of the current Map
     */
    public List<String> getManagers(){
        // go to a new view that will show the list of managers
        return managerList;
    }

    /**
    Return a list of Taks for to the ______ View
     */
    public List<TakObject> getTakList() { return takList; }

    /**
     * idk
     */
    public String downloadData(){
        return "The";
    }

}
