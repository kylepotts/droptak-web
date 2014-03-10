package edu.purdue.maptak.admin.fragments;

import android.app.Fragment;
import android.content.Context;
import android.location.Location;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.location.LocationManager;
import android.widget.EditText;
//import android.accounts.AccountManager;
//import android.accounts.Account;

import edu.purdue.maptak.admin.MainActivity;
import edu.purdue.maptak.admin.R;
import edu.purdue.maptak.admin.data.MapTakDB;
import edu.purdue.maptak.admin.data.TakID;
import edu.purdue.maptak.admin.data.TakObject;

public class AddTakFragment extends Fragment {


    /** Inflates the view for this fragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_addtak, container, false);

        /** Create the DB in order to add a tak */
        final MapTakDB newDB = new MapTakDB(getActivity());

        final EditText labelText = (EditText) view.findViewById(R.id.labelText);
        final EditText descriptionText = (EditText) view.findViewById(R.id.descriptionText);

        /** Button1 creates a tak at the user's current location */
        Button button = (Button) view.findViewById(R.id.button1);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                LocationManager lm = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
                Location userLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);

                /** Create the tak to add to DB */
                TakObject newTak;

                if(userLocation != null) {
                    double lat = userLocation.getLatitude();
                    double lng = userLocation.getLongitude();

                    newTak = new TakObject(labelText.getText().toString(), lat, lng);
                    newDB.addTak(newTak, MainActivity.currentSelectedMap);
                }
            }
        });
        return view;
    }

}

