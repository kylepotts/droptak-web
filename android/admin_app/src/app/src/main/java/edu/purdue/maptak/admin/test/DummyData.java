package edu.purdue.maptak.admin.test;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.UUID;

import edu.purdue.maptak.admin.data.MapID;
import edu.purdue.maptak.admin.data.MapObject;
import edu.purdue.maptak.admin.data.TakID;
import edu.purdue.maptak.admin.data.TakObject;

/** Statically generates dummy data which can be used for testing elsewhere in the app */
public class DummyData {

    /** Creates a random map object with an ID */
    public static MapObject createDummyMapObject() {
        Random r = new Random();

        String name = UUID.randomUUID().toString().substring(0,12);
        String id = UUID.randomUUID().toString();

        List<TakObject> taks = new ArrayList<TakObject>();
        for (int i = 0; i < 25; i++) {
            taks.add(createDummyTakObject());
        }

        return new MapObject(name, new MapID(id), taks);
    }

    /** Creates a random tak with an ID */
    public static TakObject createDummyTakObject() {
        Random r = new Random();

        String name = "Random tak name " + r.nextInt(100);
        float lat = (r.nextFloat()*20)+10;
        float lng = (r.nextFloat()*20)+10;
        return new TakObject(name, lat, lng);
    }

}
