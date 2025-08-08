# Alert Test Project

A simple microservices setup for processing video alerts. The system extracts video resolution information and stores alert data in a database. It simulates notifications by printing in the terminal.
Built with FastAPI, PostgreSQL, and Nginx, Docker.

## 🏗️ Architecture

The project is split into three services:

- **Alert Service** (FastAPI): Handles alert processing and video resolution extraction
- **PostgreSQL**: Stores the alert data
- **Nginx**: Serves video files

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed

### Running the Application

1. **Clone and navigate to the project**
   ```bash
   git clone <repository-url>
   cd alert-test
   ```

2. **Start everything up**
   ```bash
   docker-compose up --build
   ```

3. **Check that it's working**
   - Alert Service API: http://localhost:8000
   - Nginx Video Server: http://localhost:8080
   - PostgreSQL: localhost:5432

## 📋 API Documentation

### Endpoints

#### POST `/alerts`

Processes an alert with video information and extracts resolution.

**Request Body:**
```json
{
  "uuid": "35df2857-3a48-4985-aed0-e68b5ae4c968",
  "video": "/videos/test_1.avi",
  "timestamp": 1748871320.6882,
  "store": "test-store"
}
```

Validation:
- The `video` field is validated in the schema using a regex-based type. It must end with one of: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm` (case-insensitive).

**Response:**
```json
{
  "status": "success",
  "resolution": "1920x1080"
}
```

#### GET `/`

Health check endpoint.

**Response:**
```json
{
  "Hello": "World"
}
```

## 🗄️ Database Schema

The `alerts` table contains the following fields:

- `id`: Primary key (auto-increment)
- `uuid`: Unique identifier for the alert
- `video`: Path to the video file (validated to end with one of: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`)
- `store`: Store identifier
- `timestamp`: Unix timestamp of the alert
- `resolution`: Extracted video resolution (e.g., "1920x1080")
- `received_at`: Timestamp when the alert was received

## 🧪 Testing

Run the test suite using Docker Compose:

```bash
docker-compose --profile test up alert_tests
```

### Test Coverage

The test suite covers:
- Input validation (missing fields)
- Video server unreachable scenarios
- Video resolution extraction failures
- Duplicate UUID handling
We could of course add a lot more tests in a production scenatrio but for the sake of time and simplicity, it is not exhaustive.

## 🔧 Development

### Project Structure

```
alert-test/
├── compose.yml              # Docker Compose configuration
├── fastapi/                 # Alert Service
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── database.py     # Database configuration
│   │   └── utils.py        # Utility functions
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # FastAPI service container
│   └── tests/              # Test suite
├── nginx/                   # Video file server
│   ├── nginx.conf          # Nginx configuration
│   ├── Dockerfile          # Nginx container
│   └── videos/             # Video files directory
└── postgres/               # Database
    └── Dockerfile          # PostgreSQL container
```

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `VIDEO_SERVER`: Nginx server URL for video files

## 🔍 Key Features

- **Video Resolution Extraction**: Uses OpenCV to extract video resolution from uploaded files
- **Schema-level Input Validation**: `video` uses a regex-validated string type to allow only `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm` (case-insensitive)
- **Duplicate Prevention**: Prevents duplicate alerts using UUID constraints
- **Error Handling**: Comprehensive error handling for video server issues and processing failures
- **Microservices Architecture**: Separated concerns with dedicated services for different functions
- **Docker Containerization**: Easy deployment and development setup

## 🛠️ Technologies Used

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL
- **Video Processing**: OpenCV
- **HTTP Client**: httpx
- **Web Server**: Nginx
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest

## 📝 Notes

- The application creates database tables automatically on startup (for simplicity)
- Video files are served through Nginx for efficient delivery
- Temporary video files are created and cleaned up during resolution extraction
- The system is designed for small-scale deployments; for production, consider using proper migration tools like Alembic

## 🚀 Scaling Improvements

### Performance Optimizations

1. **Database Scaling**
   - Implement database connection pooling (e.g., using `asyncpg` for async connections)
   - Add database read replicas for read-heavy workloads
   - Implement proper database indexing on frequently queried fields
   - Consider using Redis for caching frequently accessed data

2. **Video Processing Optimization**
   - Implement async video processing with background tasks (Celery/RQ)
   - Add video processing queue to handle high load
   - Implement video format validation before processing
   - Add support for multiple video formats (MP4, MOV, etc.)
   - Consider using GPU acceleration for video processing

3. **API Performance**
   - Implement request rate limiting
   - Add API response caching with Redis
   - Implement pagination for large result sets
   - Add request/response compression
   - Consider using FastAPI's background tasks for non-blocking operations

4. **Infrastructure Scaling**
   - Implement horizontal scaling with load balancers (HAProxy/Nginx)
   - Use container orchestration (Kubernetes/Docker Swarm)
   - Implement auto-scaling based on CPU/memory usage
   - Add health checks and circuit breakers
   - Consider using CDN for video file delivery

5. **Monitoring and Observability**
   - Add comprehensive logging (structured logging with JSON)
   - Implement metrics collection (Prometheus/Grafana)
   - Add distributed tracing (Jaeger/Zipkin)
   - Implement alerting for system health
   - Add performance monitoring and profiling

6. **Security Enhancements**
   - Implement API authentication and authorization
   - Add request validation and sanitization
   - Implement rate limiting per user/IP
   - Add CORS configuration
   - Consider using HTTPS with proper SSL certificates

7. **Data Management**
   - Implement proper database migrations (Alembic)
   - Add data archiving strategy for old alerts
   - Implement data backup and recovery procedures
   - Consider using time-series databases for historical data
   - Add data retention policies

8. **Video Storage Optimization**
   - Implement video file compression
   - Add support for video streaming (HLS/DASH)
   - Consider using object storage (S3/GCS) for video files
   - Implement video thumbnail generation
   - Add video metadata extraction and storage

9. **Error Handling and Resilience**
   - Implement retry mechanisms with exponential backoff
   - Add circuit breakers for external service calls
   - Implement graceful degradation
   - Add dead letter queues for failed processing
   - Consider using event sourcing for audit trails

10. **Development and Deployment**
    - Implement CI/CD pipelines
    - Add automated testing with different environments
    - Implement blue-green deployments
    - Add feature flags for gradual rollouts
    - Consider using infrastructure as code (Terraform/CloudFormation)
