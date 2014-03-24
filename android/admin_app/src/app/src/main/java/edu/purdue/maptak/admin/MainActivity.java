package edu.purdue.maptak.admin;

import android.app.ActionBar;
import android.app.Activity;
import android.app.FragmentTransaction;
import android.content.Context;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.inputmethod.InputMethodManager;
import android.widget.Toast;

import java.util.Random;

import edu.purdue.maptak.admin.data.MapID;
import edu.purdue.maptak.admin.data.MapTakDB;
import edu.purdue.maptak.admin.fragments.AddTakFragment;
import edu.purdue.maptak.admin.fragments.CreateMapFragment;
import edu.purdue.maptak.admin.fragments.MapListFragment;
import edu.purdue.maptak.admin.fragments.TakListFragment;
import edu.purdue.maptak.admin.fragments.TakMapFragment;
import edu.purdue.maptak.admin.interfaces.OnGMapLoadedListener;
import edu.purdue.maptak.admin.interfaces.OnMapSelectedListener;
import edu.purdue.maptak.admin.test.DummyData;

public class MainActivity extends Activity implements OnMapSelectedListener {

    /** Log tag for debugging logcat output */
    public static final String LOG_TAG = "maptak";

    /** Save the menu object so it can be changed dynamically later */
    private Menu menu;

    /** MapFragment currently inflated to the screen */
    private TakMapFragment mapFragment = null;

    /** Store the current map the user has displayed as a static variable.
     *  This way, fragments can access it as necessary when adding new taks to the current map. */
    public static MapID currentSelectedMap = null;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.i(LOG_TAG, "MapActivity.onCreate() called.");
        setContentView(R.layout.activity_main);

        // Create a new map fragment for the screen
        mapFragment = new TakMapFragment();
        FragmentTransaction ft = getFragmentManager().beginTransaction();
        ft.replace(R.id.activity_map_mapview, mapFragment);
        ft.commit();

        /* TODO: Adding some sample Maps to the database for testing purposes */

        MapTakDB db = new MapTakDB(this);

        // 50% of the time, clear out the database completely
        Random r = new Random();
        if (r.nextInt(100) <= 50) {
            db.destroy();
            Toast.makeText(this, "DEBUG: Clearing database.", Toast.LENGTH_LONG).show();
        }

        db.addMap(DummyData.createDummyMapObject());

        /* TODO: End testing code */
    }

    public boolean onCreateOptionsMenu(Menu menu) {
        this.menu = menu;
        getMenuInflater().inflate(R.menu.main_normal, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:

                // Re-inflate the map
                getFragmentManager()
                        .beginTransaction()
                        .replace(R.id.activity_map_mapview, mapFragment)
                        .commit();

                // Change the menu bar back to normal
                menu.clear();
                if (currentSelectedMap == null) {
                    getMenuInflater().inflate(R.menu.main_normal, menu);
                } else {
                    getMenuInflater().inflate(R.menu.main_mapselected, menu);
                }

                // Disable the back button
                setUpEnabled(false);

                // Set the keyboard collapsed
                InputMethodManager imm = (InputMethodManager)getSystemService(
                        Context.INPUT_METHOD_SERVICE);
                imm.toggleSoftInput(InputMethodManager.HIDE_IMPLICIT_ONLY, 0);

                break;

            case R.id.menu_maplist:

                // Set the main_normal view to a map list fragment
                MapListFragment mlFrag = new MapListFragment();
                mlFrag.setOnMapSelectedListener(this);
                getFragmentManager()
                        .beginTransaction()
                        .replace(R.id.activity_map_mapview, mlFrag)
                        .commit();

                // Change the menu bar
                menu.clear();
                getMenuInflater().inflate(R.menu.maplist, menu);

                // Enable the back button on the action bar
                setUpEnabled(true);

                break;

            case R.id.menu_createmap:

                // Set the main view to the create map fragment
                getFragmentManager()
                        .beginTransaction()
                        .replace(R.id.activity_map_mapview, new CreateMapFragment())
                        .commit();

                // Change the menu bar
                menu.clear();

                // Enable the back button on the action bar
                setUpEnabled(true);

                break;

            case R.id.menu_addtak:

                // Set the main view to the create map fragment
                getFragmentManager()
                        .beginTransaction()
                        .replace(R.id.activity_map_mapview, new AddTakFragment())
                        .commit();

                // Clear the menu bar
                menu.clear();

                // Set up enabled
                setUpEnabled(true);

                break;

            case R.id.menu_taklist:

                // Set the main view to create the map fragment.
                getFragmentManager()
                        .beginTransaction()
                        .replace(R.id.activity_map_mapview, new TakListFragment())
                        .commit();

                // Clear the menu
                menu.clear();

                // Set up enabled
                setUpEnabled(true);

                break;

            case R.id.menu_settings:

                break;
        }

        return super.onOptionsItemSelected(item);
    }

    /** Enabled the "up" button on the action bar app icon, which will take the user back to
     *  the map screen. */
    private void setUpEnabled(boolean enabled) {
        ActionBar ab = getActionBar();
        if (ab != null) {
            ab.setDisplayHomeAsUpEnabled(enabled);
        }
    }

    /** Overrides the back button. Currently does nothing, but will be used later. */
    public void onBackPressed() {
        super.onBackPressed();
    }

    /** Called when a map is selected in MapListFragment */
    public void onMapSelected(MapID selectedMapID) {
        // Reset the state of the action bar
        menu.clear();
        getMenuInflater().inflate(R.menu.main_mapselected, menu);
        setUpEnabled(false);

        // Set the global currently selected map
        currentSelectedMap = selectedMapID;

        // Re-inflate the main view
        getFragmentManager()
                .beginTransaction()
                .replace(R.id.activity_map_mapview, mapFragment)
                .commit();
        mapFragment.setOnGMapLoadedListener(new OnGMapLoadedListener() {
            public void onGMapLoaded() {
                // Get the map the user selected and display the taks
                MapTakDB db = new MapTakDB(MainActivity.this);
                mapFragment.addTaksToGMap(db.getMap(currentSelectedMap));
            }
        });

    }

}
