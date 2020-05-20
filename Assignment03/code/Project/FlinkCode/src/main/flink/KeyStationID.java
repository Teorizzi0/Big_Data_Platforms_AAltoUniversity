package main.java.flinkcode;

import org.apache.flink.api.java.functions.KeySelector;

//keyed by station_id
public class StationKeySelector implements KeySelector<BTSEvent, String> {

	@Override
	public String getKey(BTSEvent value) throws Exception {
		return value.station_id;
	}
}
