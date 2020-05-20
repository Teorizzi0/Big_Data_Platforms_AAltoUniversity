package main.java.flinkcode;
import org.apache.flink.api.java.functions.KeySelector;


public class SensorKeySelector implements KeySelector<BTSEvent, String> {

	@Override
	public String getKey(BTSEvent value) throws Exception {
		return value.datapoint_id;
	}
}
