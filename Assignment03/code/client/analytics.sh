docker exec -it code_jobmanager_1 flink run /job.jar --amqpurl rabbitmq1 --iqueue customer --oqueue receiver1 --parallelism 1
