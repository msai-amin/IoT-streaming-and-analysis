# Real-time IoT Sensor Data Analytics Pipeline

A comprehensive pipeline for ingesting, processing, and analyzing data from IoT sensors in real-time.

## Architecture

This project implements a complete IoT data pipeline with the following components:

- **Data Simulation**: Scripts to generate simulated sensor data (temperature, humidity, motion)
- **Data Ingestion**: MQTT and/or Apache Kafka for message brokering
- **Stream Processing**: Real-time data processing using Apache Flink/Kafka Streams/Spark Streaming
- **Storage**: Time-series databases (InfluxDB/TimescaleDB) for efficient storage and querying
- **Visualization**: Real-time dashboards using Grafana
- **Edge Computing**: Simulated edge processing capabilities

![Architecture Diagram](docs/images/architecture_diagram.png)

## Features

- Real-time data ingestion from multiple sensor types
- Stream processing for anomaly detection and analytics
- Configurable alerting based on sensor thresholds
- Historical data storage with efficient time-series queries
- Interactive dashboards for monitoring and analysis
- Scalable architecture using containerization

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/iot-sensor-analytics-pipeline.git
   cd iot-sensor-analytics-pipeline
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the infrastructure using Docker Compose:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

4. Generate sample sensor data:
   ```bash
   python data/generators/sensor_simulator.py
   ```

5. Access the Grafana dashboard at http://localhost:3000

For detailed setup instructions, see [Setup Documentation](docs/setup.md).

## Project Structure

- `data/`: Sample data and data generation scripts
- `ingestion/`: MQTT and Kafka configurations
- `processing/`: Stream processing applications
- `storage/`: Database configurations and scripts
- `visualization/`: Grafana dashboards and web UI
- `edge/`: Edge computing simulations
- `docker/`: Docker configurations for all services

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 