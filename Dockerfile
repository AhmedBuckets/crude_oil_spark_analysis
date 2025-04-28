FROM openjdk:11-jre-slim
# Set environment variables
ENV SPARK_VERSION=3.3.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PYTHONHASHSEED=1
ENV PYSPARK_PYTHON=python3

# Install necessary packages including Python
RUN apt-get update && apt-get install -y curl wget procps python3 python3-pip python3-numpy python3-setuptools

# Download and extract Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} ${SPARK_HOME} && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Download Iceberg runtime JAR for Spark 3.3
RUN wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.3_2.12/1.3.1/iceberg-spark-runtime-3.3_2.12-1.3.1.jar -P ${SPARK_HOME}/jars/

# Set PATH
ENV PATH=${PATH}:${SPARK_HOME}/bin:${SPARK_HOME}/sbin
ENV PYTHONPATH=${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-*.zip

# Create a directory for Iceberg warehouse
RUN mkdir -p /warehouse/iceberg

# Create the start script directly in the Dockerfile to avoid line ending issues
RUN echo '#!/bin/bash\n\
# Start Spark master\n\
${SPARK_HOME}/sbin/start-master.sh -h spark-master\n\
# Start Spark worker\n\
${SPARK_HOME}/sbin/start-worker.sh spark://spark-master:7077\n\
# Keep container running\n\
tail -f ${SPARK_HOME}/logs/*\n\
' > /start-spark.sh && chmod +x /start-spark.sh

# Copy configuration files
COPY spark-config/spark-defaults.conf ${SPARK_HOME}/conf/

# Install Python dependencies
COPY scripts/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Set working directory
WORKDIR ${SPARK_HOME}
RUN echo "umask 000" >> /etc/bash.bashrc

# Expose Spark ports
EXPOSE 8080 7077 6066 4040

# Start command
CMD ["/start-spark.sh"]