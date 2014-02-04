package edu.purdue.maptak.admin;

import android.app.ActionBar;
import android.app.Activity;
import android.app.FragmentTransaction;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

public class MainActivity extends Activity {

    /** Log tag for debugging logcat output */
    public static final String LOG_TAG = "maptak";

    /** Save the mapfragment as a class variable so it can be inflated quicker and remember the last location the user was at */
    TakMapFragment mapFragment;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(LOG_TAG, "MapActivity.onCreate() called.");
        setContentView(R.layout.activity_map);

        // Create a new map fragment for the screen
        mapFragment = new TakMapFragment();

        FragmentTransaction ft = getFragmentManager().beginTransaction();
        ft.replace(R.id.activity_map_mapview, mapFragment);
        ft.commit();
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:

                // Re-inflate the map
                getFragmentManager().beginTransaction().replace(R.id.activity_map_mapview, mapFragment).commit();

                // Disable the back button
                setUpEnabled(false);
                break;

            case R.id.menu_taklist:

                // Set the main view to a map list fragment
                FragmentTransaction ft = getFragmentManager().beginTransaction();
                ft.replace(R.id.activity_map_mapview, new MapListFragment());
                ft.commit();

                // Enable the back button on the action bar
                setUpEnabled(true);
                break;

            case R.id.menu_settings:

                break;
        }

        return super.onOptionsItemSelected(item);
    }

    private void setUpEnabled(boolean enabled) {
        ActionBar ab = getActionBar();
        if (ab != null) {
            ab.setDisplayHomeAsUpEnabled(enabled);
        }
    }
}
