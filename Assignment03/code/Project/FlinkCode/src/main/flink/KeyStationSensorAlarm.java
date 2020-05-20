package main.java.flinkcode;

import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.api.java.tuple.Tuple3;

public class StationSensorAlarmKeySelector implements KeySelector<BTSEvent, Tuple3<String1, String2, String3>> {

	@Override
	public Tuple3<String1, String2, String3> getKey(BTSEvent value) throws Exception {
		return new Tuple3(value.station_id, value.datapoint_id, value.alarm_id);
	}
}
