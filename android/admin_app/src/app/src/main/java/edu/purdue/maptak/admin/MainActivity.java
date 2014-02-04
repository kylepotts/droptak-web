package edu.purdue.maptak.admin;

import android.app.Activity;
import android.app.FragmentTransaction;
import android.os.Bundle;

import com.google.android.gms.maps.MapFragment;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_map);

        FragmentTransaction ft = getFragmentManager().beginTransaction();
        ft.replace(R.id.activity_map_main, new MapFragment());
        ft.commit();
    }


}
