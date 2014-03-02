package edu.purdue.maptak.admin;

import android.app.Fragment;
import android.content.Context;
import android.os.Bundle;
import android.text.Layout;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.LinkedList;
import java.util.List;

import edu.purdue.maptak.admin.data.MapObject;
import edu.purdue.maptak.admin.data.MapTakDB;

public class MapListFragment extends Fragment {

    /** List View that will display the maps currently accessible by the manager/user */
    ListView mapList;

    /** Used to access the MapTakDB class */
    MapTakDB mapTakDB = new MapTakDB(getActivity());

    /** List Adapter that will hold the data that populates the list view */
    ListAdapter listAdapter;

    /** Inflates the view for this fragment. */
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        mapList = (ListView) getActivity().findViewById(R.id.fragment_maplist_listview);
        listAdapter = new MapObjectAdapter<MapObject>(getActivity(), android.R.layout.simple_list_item_1, mapTakDB.getUsersMaps());
        mapList.setAdapter(listAdapter);
        return inflater.inflate(R.layout.fragment_maplist, container, false);
    }

    /** Custom ListView Adapter */
    public class MapObjectAdapter<MapObject> extends ArrayAdapter {
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
                temp.title = (TextView) row.findViewById(R.id.mapData);
                row.setTag(temp);
            } else {
                temp = (MapObjectData)row.getTag();
            }
            MapObject mapToBeDisplayed = mMaps.get(position); // there is a bug of some sort here
            temp.title.setText("This");
            return row;
        }

        class MapObjectData
        {
            TextView title;
        }

    }




}
