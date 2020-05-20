import os
import time
import pika
import logging
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Authentication')
    #queue
    parser.add_argument('-queue', type=str, help='Insert a name for the queue')
    return parser.parse_args()

def response(c, m, p, b):
    print(" [x] Incoming percentage %r" % b)
    time.sleep(0.6)
    logging.info("Receive data : %r" % b)
    c.basic_ack(delivery_tag = m.delivery_tag)

if __name__ == "__main__":
    args = parse_arguments()
    if args.queue is None:
        logging.debug("error in the queue")
        exit(0)
    logging.info("Data received and RabbitMQ started")
    credentials = pika.PlainCredentials('client', 'client')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    logging.info("Data received and Topic creation")
    channel.queue_declare(queue=args.queue)
    channel.basic_consume(queue=args.queue, on_message_callback=callback)
    print('Waiting messagges')
    channel.start_consuming()
    