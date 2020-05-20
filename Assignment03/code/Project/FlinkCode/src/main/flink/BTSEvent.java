/*
* CS-E4640
 * Linh Truong
 */
package main.java.flinkcode;

import java.util.Date;

public class BTSEvent {
	public String station_id;
	public String datapoint_id;
	public String alarm_id;
	public Date event_time;
	public float value;
	public float valueThreshold;
	public boolean alarm;
	public boolean deserialized; // if the input event could be deserialized
	

	BTSEvent() {

	}

	BTSEvent(String station_id, String datapoint_id, String alarm_id, Date event_time, Float value,
			Float valueThreshold, boolean alarm_active, boolean deserialized) {
		this.station_id = station_id;
		this.datapoint_id = datapoint_id;
		this.alarm_id = alarm_id;
		this.event_time = event_time;
		this.value = value;
		this.valueThreshold = valueThreshold;
		this.alarm = alarm_active;
		this.deserialized = deserialized;
	}

	public String toString() {
		return "station_id:" + station_id + "; datapoint_id:" + datapoint_id + "; time: " + event_time.toString()
				+ "; alarm_id:" + alarm_id + "; value:" + value;
	}
}
