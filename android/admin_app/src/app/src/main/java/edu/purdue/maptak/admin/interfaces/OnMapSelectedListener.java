package edu.purdue.maptak.admin.interfaces;

import edu.purdue.maptak.admin.data.MapID;

/** Interface which initiates a callback every time a map is selected by the user */
public interface OnMapSelectedListener {

    public void onMapSelected(MapID map);

}
