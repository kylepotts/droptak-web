package edu.purdue.maptak.admin;

import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;

import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.model.LatLng;

public class TakMapFragment extends MapFragment {


    /** Called when the fragment has been fully inflated into the activity */
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        // Enable the user's location on the map
        getMap().setMyLocationEnabled(true);

        // Get their current location
        LocationManager lm = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
        Location userLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        LatLng userLatLng = new LatLng(userLocation.getLatitude(), userLocation.getLongitude());

        // Center the map to that position
        CameraUpdate moveCam = CameraUpdateFactory.newLatLngZoom(userLatLng, 14.5f);
        getMap().animateCamera(moveCam);

    }

}
