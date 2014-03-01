package edu.purdue.maptak.admin.data;

/** Encapsulates all the information related to an ID which describes a single Tak. */
public class TakID {

    /** String representation of the ID */
    private String takID;

    /** Constructor. Pass in ID */
    public TakID(String takID) {
        this.takID = takID;
    }

    /** Returns the takid in a string format */
    public String getIDStr() {
        return this.takID;
    }

}
