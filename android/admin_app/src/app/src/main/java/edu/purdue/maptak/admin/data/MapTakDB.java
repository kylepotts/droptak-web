package edu.purdue.maptak.admin.data;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.List;

public class MapTakDB extends SQLiteOpenHelper {

    /** Database name and version */
    public static final String DB_NAME = "database_cached_taks";
    public static final int DB_VERSION = 1;

    /** Tables */
    public static final String TABLE_MAPS = "t_maps";
    public static final String TABLE_TAKS = "t_taks";

    /** Columns - TABLE_MAPS */
    public static final String MAP_ID = "_id";
    public static final String MAP_LABEL = "map_label";

    /** Columns - TABLE_TAKS */
    public static final String TAK_ID = "_id";
    public static final String TAK_MAP_ID = "map_id";
    public static final String TAK_LABEL = "tak_label";
    public static final String TAK_LAT = "tak_lat";
    public static final String TAK_LNG = "tak_lng";

    /** Default constructor */
    public MapTakDB(Context context) {
        super(context, DB_NAME, null, DB_VERSION);
    }

    /** Called when the database is first created. */
    public void onCreate(SQLiteDatabase sqLiteDatabase) {

        // Strings which create tables

        String create_table_maps = "CREATE TABLE " + TABLE_MAPS + " (" +
                MAP_ID + " TEXT, " +
                MAP_LABEL + " TEXT );";

        String create_table_taks = "CREATE TABLE " + TABLE_TAKS + " ( " +
                TAK_ID + " TEXT, " +
                TAK_MAP_ID + " INTEGER, " +
                TAK_LABEL + " TEXT, " +
                TAK_LAT + " DOUBLE, " +
                TAK_LNG + " DOUBLE );";

        // Create the sqlite database

        sqLiteDatabase.execSQL(create_table_maps);
        sqLiteDatabase.execSQL(create_table_taks);

    }

    /** Called when the database is upgraded from one DB_VERSION to the next */
    public void onUpgrade(SQLiteDatabase sqLiteDatabase, int i, int i2) {

    }

    /** Refreshes the database with information from the server */
    public void refresh() {
        // Implement in sprint 2
    }

    /** Pushes a new map for the user to the remote database then refreshes the local cache */
    public void addMap(String map) {

    }

    /** Pushes a new tak for a given map to the remote database then refreshes the local cache */
    public void addTak(String tak, String map) {

    }

    /** Returns a list of the maps the user is authorized to access. */
    public List<String> getUsersMaps() {
        return null;
    }

    /** Returns a list of taks associated with a given map */
    public List<String> getTaks(String map) {
        return null;
    }




}
