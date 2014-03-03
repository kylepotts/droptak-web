package edu.purdue.maptak.admin;

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

public class TakMapFragment extends MapFragment {

    /** Bundle strings for accessing keys in the args bundle */
    private static String BUNDLE_MAP_TO_DISPLAY = "map_to_display";

    /** Static fragment generator. Use this if you don't want to display anything on this map */
    public static TakMapFragment newInstanceOf() {
        return new TakMapFragment();
    }

    /** Static fragment generator. Use this instead of `new` to create an instance of this fragment */
    public static TakMapFragment newInstanceOf(MapID toDisplay) {
        TakMapFragment frag = new TakMapFragment();
        Bundle args = new Bundle();
        args.putString(BUNDLE_MAP_TO_DISPLAY, toDisplay.getIDStr());
        frag.setArguments(args);
        return frag;
    }

    /** Super class takes care of creating the view since we're just extending Google's MapFragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return super.onCreateView(inflater, container, savedInstanceState);
    }

    /** Called when the fragment has been fully inflated into the activity */
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

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

        // If a map should be loaded, load it
        Bundle args = getArguments();
        if (args != null) {

            String mapIDStr = args.getString(BUNDLE_MAP_TO_DISPLAY);
            Log.d(MainActivity.LOG_TAG, "TakMapFragment.onActivityCreated() -> Creating map with mapID " + mapIDStr);

            // Get the map object which should be loaded
            MapTakDB db = new MapTakDB(getActivity());
            MapID mapID = new MapID(mapIDStr);
            MapObject mapToLoad = db.getMap(mapID);

            // Get the gmap on which we will draw the points
            GoogleMap gmap = getMap();
            gmap.clear();

            // Get all the latlng points for the map and add them
            LatLngBounds.Builder builder = LatLngBounds.builder();
            for (TakObject t : mapToLoad.getTakList()) {
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

        } else {
            Log.d(MainActivity.LOG_TAG, "TakMapFragment.onActivityCreated() -> No arguments set. Creating blank map.");
        }

    }

}
