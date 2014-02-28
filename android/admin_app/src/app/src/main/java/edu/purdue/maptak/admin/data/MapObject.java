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
    List<Object> takList;

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
        takList = new LinkedList<Object>();
        requireKey = true;
        mapID = null;
    }

    /**
     * Receives input from the Tak class and adds that Tak to the Map
     */
    public void addTak( TakID tak ){
        takList.add(tak);
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
    public Object getTak( int key ){
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
     * idk
     */
    public String downloadData(){
        return "The";
    }

}
