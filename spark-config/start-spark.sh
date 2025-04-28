#!/bin/bash

# Start Spark master
${SPARK_HOME}/sbin/start-master.sh -h spark-master

# Start Spark worker
${SPARK_HOME}/sbin/start-worker.sh spark://spark-master:7077

# Keep container running
tail -f ${SPARK_HOME}/logs/*