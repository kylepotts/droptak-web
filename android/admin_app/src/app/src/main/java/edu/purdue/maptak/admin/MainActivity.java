package edu.purdue.maptak.admin;

import android.app.Activity;
import android.app.FragmentTransaction;
import android.os.Bundle;
import android.util.Log;

public class MainActivity extends Activity {

    public static final String LOG_TAG = "maptak";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(LOG_TAG, "MapActivity.onCreate() called.");

        setContentView(R.layout.activity_map);

        FragmentTransaction ft = getFragmentManager().beginTransaction();
        ft.replace(R.id.activity_map_main, new TakMapFragment());
        ft.commit();
    }


}
