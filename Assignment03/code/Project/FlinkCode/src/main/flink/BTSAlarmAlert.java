/*
 * CS-E4640
 * Linh Truong
 */
package main.java.flinkcode;

public class BTSAlarmAlert {
	public boolean warning = false;
	public String station_id;

	public BTSAlarmAlert() {
	}

	public BTSAlarmAlert(String station_id, boolean warn) {
		this.station_id = station_id;
		this.warn = warn;
	}

	public String toJSON() {
		return "{\"alarm\":{\"station_id\":" + station_id + ", \"isactive\"}}";
	}

}
