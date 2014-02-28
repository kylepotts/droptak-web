package edu.purdue.maptak.admin;

import android.app.Fragment;
import android.content.Context;
import android.location.Location;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.location.LocationManager;
import android.widget.EditText;
//import android.accounts.AccountManager;
//import android.accounts.Account;

import edu.purdue.maptak.admin.data.TakObject;

public class AddTakFragment extends Fragment {

    /** Inflates the view for this fragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_addtak, container, false);

        EditText labelText = (EditText) view.findViewById(R.id.labelText);
        EditText descriptionText = (EditText) view.findViewById(R.id.descriptionText);

        /** Button1 creates a tak at the user's current location */
        Button button = (Button) view.findViewById(R.id.button1);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                LocationManager lm = (LocationManager) getActivity().getSystemService(Context.LOCATION_SERVICE);
                Location userLocation = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);

                /** I think this is how you are able to get the UUID of the user(gmail) */
                //AccountManager am = (AccountManager) getActivity().getSystemService(Context.ACCOUNT_SERVICE);
                //Account[] accountList = am.getAccounts();

                double lat = userLocation.getLatitude();
                double lng = userLocation.getLongitude();

                TakObject newTak = new TakObject(lat, lng);


                //Add UUID to tak(?)

                //Send the tak to the server

            }
        });
        return view;
    }

}

