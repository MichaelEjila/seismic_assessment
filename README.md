# seismic_assessment

This project contains two separate Django services (Frontend and Backend APIs) that communicate using RabbitMQ.

## Prerequisites

- Install Docker: [Docker installation guide](https://docs.docker.com/get-docker/)
- Install Docker Compose: [Docker Compose installation guide](https://docs.docker.com/compose/install/)

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/MichaelEjila/seismic_assessment.git
    cd seismic_assessment
    ```

2. Ensure that Docker is running.

3. Pull the required images from Docker Hub and start the services using:

    ```bash
    docker pull michaelejila/library_frontend:latest
    docker pull michaelejila/library_admin:latest
    docker pull michaelejila/rabbitmq:latest
    docker-compose up
    ```

   This will pull the Frontend, Backend, and RabbitMQ images and spin up all services.

## Access the Services

- **Frontend API**: Visit [http://localhost:8000](http://localhost:8000)
- **Backend API**: Visit [http://localhost:8001](http://localhost:8001)
- **RabbitMQ Management UI**: Visit [http://localhost:15672](http://localhost:15672) (default login: guest/guest)

## Running the RabbitMQ Consumer

To enable the **Frontend API** to listen for RabbitMQ messages, run the following command in a separate terminal within the `frontend` service container:

    ```bash
    docker-compose exec frontend python manage.py consume_rabbitmq
    ```

## Stopping the Services

To stop the services, press `Ctrl+C` or run:

```bash
docker-compose down
