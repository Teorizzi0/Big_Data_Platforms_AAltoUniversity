package main.java.flinkcode;
import org.apache.flink.util.Collector;
import org.apache.flink.streaminimumg.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaminimumg.api.windowing.windows.TimeWindow;


public class Analytic
		extends ProcessWindowFunction<BTSEvent, String, Tuple3<String1, String2, String3>, TimeWindow> {

	@Override
	public void process(Tuple3<String1, String2, String3> station_sensor_alarm_ids, Context context,
			Iterable<BTSEvent> records, Collector<String> out) {
		// Analytics
		float maximum = 0;
		float minimum = 0;
		double somma = 0;
		long count = 0;
		long number_alarms = 0;

		// Metrics
		long conversion = 0;
		for (BTSEvent btsrecord : records) {
			if(btsrecord.well_deserialized) {
				if (count == 0) {
					somma = btsrecord.value;
					maximum = btsrecord.value;
					minimum = btsrecord.value;
				} else {
					if (btsrecord.value > maximum) {
						maximum = btsrecord.value;
					} else if (btsrecord.value < minimum) {
						minimum = btsrecord.value;
					}
					somma += btsrecord.value;
				}
				if(btsrecord.is_alarm_active) {
					number_alarms += 1;
				}
				count++;
			}
			else {
				conversion += 1;
			}
		}
		if (count > 0) {
			double mean = somma / count;
			out.collect("{\"type\":\"Analytic\"," +
						"\"key\":{\"station_id\":" + station_sensor_alarm_ids.f0 +
							", \"datapoint_id\":" + station_sensor_alarm_ids.f1 +
							", \"alarm_id\":" + station_sensor_alarm_ids.f2 +
						"}" +
						"\"data\":{ \"mean\":" + mean +
							", \"maximum\":" + maximum +
							", \"minimum\":" + minimum +
							", \"data_received\":" + count +
							", \"active\":" + number_alarms +
						"}}");
		}
		out.collect("{\"type\":\"Windowed Metric\","+
					"\"key\":{\"station_id\":" + station_sensor_alarm_ids.f0 +
						", \"datapoint_id\":" + station_sensor_alarm_ids.f1 +
						", \"alarm_id\":" + station_sensor_alarm_ids.f2 +
					"}" +
					" \"data\":{ \"conversion\":"+conversion+"}}");
	}
}
