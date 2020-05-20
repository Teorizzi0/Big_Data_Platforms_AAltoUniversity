package main.java.flinkcode;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.util.Collector;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.util.Collector;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
import java.io.StringReader;
import java.text.SimpleDateFormat;
import java.util.Date;


public class BTSParser implements MapFunction<String, BTSEvent> {

	@Override
	public void Map(String line, Collector<BTSEvent> out) throws Exception {
		CSVRecord record = CSVFormat.RFC4180.withIgnoreHeaderCase().parse(new StringReader(line)).getRecords().get(0);
		try {
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss z");
			Date date = format.parse(record.get(3));
			BTSEvent event = new BTSEvent(record.get(0), record.get(1), record.get(2), date,
					Float.valueOf(record.get(4)), Float.valueOf(record.get(5)), Boolean.valueOf(record.get(6)), true);
			out.collect(event);
		} catch (Exception e) {
			BTSEvent event = new BTSEvent(record.get(0), record.get(1), record.get(2), new Date(), 0f, 0f, true,
					false);
			out.collect(event);
		}
	}
}

//I found this method to parse a CSV: https://github.com/apache/commons-csv/blob/master/src/test/java/org/apache/commons/csv/CSVParserTest.java
