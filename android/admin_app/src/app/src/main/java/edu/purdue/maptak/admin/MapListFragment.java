package edu.purdue.maptak.admin;

import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.text.Layout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.LinkedList;
import java.util.List;

import edu.purdue.maptak.admin.data.MapObject;
import edu.purdue.maptak.admin.data.MapTakDB;

public class MapListFragment extends Fragment implements AdapterView.OnItemClickListener {

    /** List View that will display the maps currently accessible by the manager/user */
    ListView mapList;

    /** Used to access the MapTakDB class */
    MapTakDB mapTakDB;

    /** List Adapter that will hold the data that populates the list view */
    ListAdapter listAdapter;

    /** Holds the listener which will be called when a map is selected */
    OnMapSelectedListener mapSelectedListener;

    /** Inflates the view for this fragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

        // Create instance of database
        mapTakDB = new MapTakDB(getActivity());

        // Prepare the list adapter
        View v = inflater.inflate(R.layout.fragment_maplist, container, false);
        mapList = (ListView) v.findViewById(R.id.fragment_maplist_listview);
        mapList.setOnItemClickListener(this);
        listAdapter = new MapObjectAdapter<MapObject>(getActivity(), android.R.layout.simple_list_item_1, mapTakDB.getUsersMaps());
        mapList.setAdapter(listAdapter);

        return v;
    }

    /** Custom ListView Adapter */
    private class MapObjectAdapter<MapObject> extends ArrayAdapter {
        private Context mContext;
        private int id;
        private List<MapObject> mMaps;

        public MapObjectAdapter(Context context, int textViewResourceId, List<MapObject> maps){
            super(context, textViewResourceId, maps);
            mContext = context;
            id = textViewResourceId;
            mMaps = maps;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent){
            View row = convertView;
            MapObjectData temp = null;
            if ( row == null ){
                LayoutInflater inflater = getActivity().getLayoutInflater();
                row = inflater.inflate(R.layout.listview_mapobject, parent, false);
                temp = new MapObjectData();
                temp.title = (TextView) row.findViewById(R.id.mapTitle);
                temp.admin = (TextView) row.findViewById(R.id.mapAdmin);
                row.setTag(temp);
            } else {
                temp = (MapObjectData)row.getTag();
            }
            MapObject mapToBeDisplayed = mMaps.get(position); // there is a bug of some sort here
            temp.admin.setText("Admin Name Here");
            temp.title.setText("Map Name Here");
            return row;
        }

        class MapObjectData
        {
            TextView title;
            TextView admin;
        }

    }

    /** Sets the onMapSelectedListener for this fragment, which will initiate a callback once
     *  the user has selected a map. */
    public void setOnMapSelectedListener(OnMapSelectedListener listener) {
        this.mapSelectedListener = listener;
    }

    /** Called when the user selects an item on the listview backing this MapListFragment */
    public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
        MapTakDB db = new MapTakDB(getActivity());

        /** TODO: Make sure that the db will always return this list in the same order every time
         *  otherwise this needs to be changed */
        mapSelectedListener.onMapSelected(db.getUsersMaps().get(i).getID());
    }

}
