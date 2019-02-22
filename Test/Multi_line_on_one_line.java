
import com.sun.xml.internal.bind.v2.TODO;

import java.lang.reflect.Array;
import java.util.ArrayList;

/*
* sdf
*
* f
* f
* f
* f
*
*
 */

//sdf

/*
* f
* f
 */

/* */

/*
* sdf
* */

// sdf
public class Airport { //sd
    //sd
    //TODO:
    private String name;
    private ArrayList flights;

    public Airport(String name) {
        this.name = name;
        this.flights = new ArrayList<Flight>();
    }

    public Boolean equals(Airport a1) {
        Boolean equal = false;
        if (this.name.equals(a1.getName())) {
            if (this.flights.size() == a1.flights.size()) {
                for (int i = 0; i < a1.getFlights().size(); i++) {
                    if (this.getFlights().contains(a1.getFlights().get(i))) {
                    } else {
                        return false;
                    }

                }
                equal = true;
            }
        }


        return equal;
    }


    public Integer size() {
        return 0;
    }


    public Boolean wasVisitedBy(Flight f1) {

        int i = 0;
        Boolean visited = false;
        while (i != f1.getAirports().size()) {
            if (f1.getAirports().get(i) == this) {
                visited = true;
            }
            ;
            i = i + 1;
        }

        return visited;


    }

    public Boolean onSameFlight(Airport a2) {
        Boolean same = false;
        for (int i = 0; i < a2.getFlights().size(); i++) {
            if (this.getFlights().contains(a2.getFlights().get(i))) {
                same = true;
            }
            ;
        }


        return same;


    }

    public void addFlight(Flight f2) {
        this.flights.add(f2);
        if (f2.getAirports().contains(this)) {
            return;
        } else {
            f2.addAirport(this);
        }


    }

    public ArrayList getFlights() {

        return this.flights;
    }

    public String getName() {
        return this.name;

    }

    public String toString(){
        if (this.getFlights().size() == 0){
            return this.getName() + " ()";
        }
        else{
            String end = this.name + " (";
            for (int i = 0; i != this.getFlights().size(); i++){
                String f1 = ((Flight)this.getFlights().get(i)).getName();
                if (i != this.getFlights().size() - 1){
                    end += f1 + ", ";
                }
                else{
                    end += f1;
                }
            }
            end += ")";
            return end;

        }
    }


}

