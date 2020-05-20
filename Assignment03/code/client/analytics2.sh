docker exec -it code_jobmanager_1 flink run /job.jar --amqpurl rabbitmq1 --iqueue customer_b --oqueue receiver2 --parallelism 1
