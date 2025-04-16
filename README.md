# ClickHouse & Flat File Data Ingestion Tool

A web-based application that facilitates bidirectional data ingestion between ClickHouse database and Flat Files. The application supports JWT token-based authentication, column selection, and provides detailed ingestion reporting.

## Features

- Bidirectional data flow:
  - ClickHouse → Flat File ingestion
  - Flat File → ClickHouse ingestion
- JWT token-based authentication for ClickHouse
- Interactive column selection
- Data preview functionality
- Progress tracking
- Error handling with user-friendly messages

## Tech Stack

- Backend:
  - Python FastAPI
  - ClickHouse Python Driver
  - Pandas for data handling
- Frontend:
  - React with TypeScript
  - Material-UI components
  - Axios for API calls
- Database:
  - ClickHouse

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.8+ (for local development)
- npm or yarn

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Environment Setup:

Create a `.env` file in the root directory:
```env
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=8123
CLICKHOUSE_DB=default
CLICKHOUSE_USER=default
JWT_SECRET_KEY=your-secret-key
```

3. Using Docker (Recommended):
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

4. Local Development Setup:

Backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## Usage Guide

1. Select Data Source:
   - Choose between ClickHouse database or Flat File

2. Configure Connection:
   - For ClickHouse:
     - Enter host, port, database, user, and JWT token
   - For Flat File:
     - Select a CSV/TXT file
     - Specify the delimiter

3. Select Columns:
   - View available columns
   - Select desired columns for ingestion
   - Use "Select All" for bulk selection

4. Preview Data:
   - Review the first 100 records
   - Verify column mapping and data format

5. Start Ingestion:
   - Monitor progress
   - View completion status and record count

## Testing

The application includes example datasets for testing:

1. ClickHouse Example Datasets:
   - UK Price Paid Dataset
   - Ontime Dataset

2. Test Cases:
   - Single table export (ClickHouse → File)
   - CSV import (File → ClickHouse)
   - Connection/authentication testing
   - Data preview functionality

## Error Handling

The application includes comprehensive error handling for:
- Connection failures
- Authentication issues
- File format problems
- Data type mismatches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT 