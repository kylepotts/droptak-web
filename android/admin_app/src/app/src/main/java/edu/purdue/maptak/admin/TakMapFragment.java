package edu.purdue.maptak.admin;

import android.content.Context;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.LatLng;

public class TakMapFragment extends MapFragment {

    /** I want the camera to do a cool animation ONLY on the first creation of this fragment. */
    boolean isFirst = true;

    /** Super class takes care of creating the view since we're just extending MapFragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Log.i(MainActivity.LOG_TAG, "TakMapFragment.onCreateView() called.");
        return super.onCreateView(inflater, container, savedInstanceState);
    }

    /** Called when the fragment has been fully inflated into the activity */
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);
        Log.i(MainActivity.LOG_TAG, "TakMapFragment.onActivityCreated() called.");

        // Enable the user's location on the map
        getMap().setMyLocationEnabled(true);

        // Get their current location
        LocationManager lm = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
        Location userLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        LatLng userLatLng = new LatLng(userLocation.getLatitude(), userLocation.getLongitude());

        // Center the map to that position
        CameraUpdate moveCam = CameraUpdateFactory.newLatLngZoom(userLatLng, 14.5f);
        if (isFirst) {
            getMap().animateCamera(moveCam);
            isFirst = false;
        } else {
            getMap().moveCamera(moveCam);
        }


    }

}
