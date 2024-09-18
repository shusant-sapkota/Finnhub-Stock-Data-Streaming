#Import the docker image from the dockerhub
FROM bitnami/spark:latest

# Copy the requirements file from local to the container
COPY requirements.txt /opt/bitnami/spark/requirements.txt

#Install Python dependencies for this project
RUN pip install -r /opt/bitnami/spark/requirements.txt

# Set the default command to start Spark Master
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]