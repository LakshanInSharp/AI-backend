# AI Backend API

A FastAPI-based backend service that provides AI-powered query processing and PDF document handling capabilities.

## Features

- 🔍 AI-powered query processing
- 📄 PDF document upload and processing
- 🗄️ Vector database integration with Pinecone
- 🚀 FastAPI for high-performance API endpoints
- 🔒 Secure environment variable management

## Prerequisites

- Python 3.8 or higher
- Pinecone account and API key
- (Optional) OpenAI API key if using OpenAI models

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r req.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your actual configuration values.

## Configuration

The following environment variables need to be configured in your `.env` file:

- `MODEL_NAME`: Name of the AI model to use
- `PINECONE_API`: Your Pinecone API key
- `PINECONE_INDEX`: Name of your Pinecone index
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `LOG_LEVEL`: Logging level (default: DEBUG)

## Running the Application

Start the FastAPI server:
```bash
uvicorn App:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Available Endpoints

#### 1. Query Processing
- **Endpoint**: `POST /api/query`
- **Description**: Process a query using AI
- **Request Body**:
```json
{
    "query": "Your question here"
}
```
- **Response**:
```json
{
    "response": "AI-generated response"
}
```

#### 2. PDF Upload
- **Endpoint**: `POST /api/upload-pdf`
- **Description**: Upload and process a PDF document
- **Request**: Form data with PDF file
- **Response**:
```json
{
    "message": "Successfully uploaded to vector database"
}
```

## Project Structure

```
.
├── App.py                 # Main FastAPI application
├── routes/               # API route handlers
│   ├── query_routes.py   # Query processing endpoints
│   └── pdf_routes.py     # PDF handling endpoints
├── Services/             # Service layer implementations
├── Chroma_DB/           # Vector database storage
├── .env.example         # Example environment variables
├── req.txt             # Project dependencies
└── README.md           # This documentation
```

## Development

### Adding New Features

1. Create new route handlers in the `routes/` directory
2. Implement service logic in the `Services/` directory
3. Update the main `App.py` to include new routes
4. Add any new environment variables to `.env.example`

### Testing

The application includes logging for debugging purposes. Check the `app.log` file for detailed logs.

## Security Considerations

- Never commit your `.env` file to version control
- Keep your API keys secure
- Use appropriate CORS settings in production
- Implement rate limiting for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Support

For support, please [add your contact information or issue reporting process] 
