import os
import time
import pika
import logging
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Authentication')
    #customer-X
    parser.add_argument('-u', type=str, help='Insert your user id')
    #message
    parser.add_argument('-file', type=str, help='Stream file is missing')
    return parser.parse_args()

def data_streaming(msg, topic):
    logging.info("Stream data : Starting connection to RabbitMQ")
    credentials = pika.PlainCredentials('client', 'client')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    conn = pika.BlockingConnection(parameters)
    channel = conn.channel()
    channel.queue_declare(queue=topic, durable=True)
    logging.info("Message sending")
    channel.basic_publish(exchange='',
                        routing_key=topic,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = 2,
                        ))
    print("\n sending %s" % message)
    logging.info("Closing connection")
    conn.close()


if __name__ == "__main__":
    args = parse_arguments()
    if args.file is None or not os.path.exists(args.file):
        print("%s" % args.file)
        logging.debug("Please insert file to be passed")
        exit(0)
    with open(args.file) as csv:
        data = csv.read()
        line = data.splitlines()
        k = 0
        for lineToStream in line:
            if k == 0:
                k+=1
                continue
            time.sleep(1)
            data_streaming(lineToStream, args.u)
            k+=1

