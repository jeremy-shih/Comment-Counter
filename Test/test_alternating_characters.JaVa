/*
* j
*
* j
* j
* j
* j
*
*
 */

/*
*
* k
*
* k
*
* k
* k
*
* k
*
 */


import java.util.ArrayList; //@sdf

//sdf

//23

//TODO:
//sdf
public class Flight { //sdf
	private String name;
	private ArrayList airports;
	private String date;

	public Flight(String name, String date) {
	    this.name = name;
	    this.date = date;
	    this.airports = new ArrayList<Airport>();

	}

    public Boolean equals(Flight f7){
        Boolean equal = false;
        if(this.name.equals(f7.getName()))
        {
            if(this.date.equals(f7.getDate())) {
                equal = true;
            }
        }

        return equal;
    }

	public void addAirport(Airport a1) {
        this.airports.add(a1);

        if(a1.getFlights().contains(this)){
            return;
        }
        else {
            a1.addFlight(this);
        }

    }


    public ArrayList getAirports(){
        return this.airports;

    }

    public String getName(){
        return this.name;

    }

    public String getDate(){
        return this.date;

    }

    public String toString(){
        if (this.getAirports().size() == 0){
            return this.getName() + ", " + this.getDate();
        }
        else{
            String end = this.name + ", " + this.getDate();
            for (int i = 0; i != this.getAirports().size(); i++){
                        end += "\n" + ((Airport)this.getAirports().get(i)).getName();
                    }
            return end;
                }

            }


    }




