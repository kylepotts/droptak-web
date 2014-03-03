package edu.purdue.maptak.admin;

import android.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;


public class CreateMapFragment extends Fragment {

    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_createmap, container, false);

        final EditText mapNameText = (EditText) view.findViewById(R.id.mapNameText);

        /** Button1 creates a tak at the user's current location */
        Button button = (Button) view.findViewById(R.id.button1);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                /** I think this is how you are able to get the UUID of the user(gmail) */
                //AccountManager am = (AccountManager) getActivity().getSystemService(Context.ACCOUNT_SERVICE);
                //Account[] accountList = am.getAccounts();

                //MapObject newMap = new MapObject();
                //newMap.setName();
                Log.i("CreateMapFragment", mapNameText.getText().toString());


            }
        });

        return view;
    }
}
