package edu.purdue.maptak.admin.fragments;

import android.content.Context;
import android.graphics.Point;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;

import edu.purdue.maptak.admin.data.MapID;
import edu.purdue.maptak.admin.data.MapObject;
import edu.purdue.maptak.admin.data.MapTakDB;
import edu.purdue.maptak.admin.data.TakObject;
import edu.purdue.maptak.admin.interfaces.OnGMapLoadedListener;

public class TakMapFragment extends MapFragment {

    /** Listener for when the gmap has been fully loaded to the screen */
    private OnGMapLoadedListener loadedListener;

    /** Bundle key for boolean which says whether the gmap has a map on it currently */
    private MapObject loadedMap = null;

    /** First method that is called, before View or Activity is created */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setRetainInstance(true);
    }

    /** Super class takes care of creating the view since we're just extending Google's MapFragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return super.onCreateView(inflater, container, savedInstanceState);
    }

    /** Called when the fragment has been fully inflated into the activity */
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        // Center the camera on the user
        centerCameraOnUser();

        // Alert listeners that the gmap is loaded
        if (loadedListener != null) {
            loadedListener.onGMapLoaded();
        }
    }

    /** Centers the map's camera on the user */
    public void centerCameraOnUser() {
        // Enable the user's location on the map
        getMap().setMyLocationEnabled(true);

        // Get their current location
        LocationManager lm = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
        Location userLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);

        if (userLocation != null) {
            double lat = userLocation.getLatitude();
            double lng = userLocation.getLongitude();
            LatLng userLatLng = new LatLng(userLocation.getLatitude(), userLocation.getLongitude());

            // Center the map to that position
            CameraUpdate moveCam = CameraUpdateFactory.newLatLngZoom(userLatLng, 14.5f);
            getMap().moveCamera(moveCam);
        }
    }

    /** Clears all of the current pins off this fragments google map, adds all the pins for a
     *  given MapObject, then zooms the camera to encompass all of these points. This is done
     *  without any database transactions. */
    public void addTaksToGMap(MapObject map) {
        // Get the gmap on which we will draw the points
        loadedMap = map;
        GoogleMap gmap = getMap();
        gmap.clear();

        // If the map has no points (brand new) then just return
        if (map.getTakList().size() == 0) {
            return;
        }

        // Get all the latlng points for the map and add them
        LatLngBounds.Builder builder = LatLngBounds.builder();
        for (TakObject t : map.getTakList()) {
            LatLng l = new LatLng(t.getLatitude(), t.getLongitude());
            builder.include(l);
            gmap.addMarker(new MarkerOptions()
                    .title(t.getLabel())
                    .position(l));
        }

        // Animate the camera to include the points we added
        Point p = new Point();
        getActivity().getWindowManager().getDefaultDisplay().getSize(p);
        gmap.animateCamera(CameraUpdateFactory.newLatLngBounds(builder.build(), p.x, p.y, 200));
    }

    /** Sets the fragments onGmapLoadedListener for when the googlemap is fully loaded */
    public void setOnGMapLoadedListener(OnGMapLoadedListener listener) {
        this.loadedListener = listener;
    }

}
