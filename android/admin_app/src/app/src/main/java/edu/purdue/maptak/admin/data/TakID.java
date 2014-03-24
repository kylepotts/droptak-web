package edu.purdue.maptak.admin.data;

/** Encapsulates all the information related to an ID which describes a single Tak. */
public class TakID {

    /** String representation of the ID */
    private String takID;

    /** Constructor. Pass in ID */
    public TakID(String takID) {
        this.takID = takID;
    }

    /** Equals method */
    public boolean equals(TakID t1) {
        if (takID.equals(t1.getIDStr())) {
            return true;
        }
        return false;
    }

    /** Returns the takid in a string format */
    public String getIDStr() {
        return this.takID;
    }

}
