# Smart FAQ Service

**Smart FAQ Service** is a modular backend for intelligent FAQ management, supporting easy configuration and Docker deployment. It allows you to manage a FAQ database and provides an AI-powered endpoint to answer user questions based on existing FAQs.

---

## Features

- **CRUD API for FAQ Management:**  
  Easily create, read, update, and delete FAQ entries via RESTful endpoints.
- **AI-Powered FAQ Answering:**  
  An agent endpoint uses OpenAI's GPT model to answer user questions based on your FAQ database.
- **Async Python Backend:**  
  Built with FastAPI and SQLAlchemy's async support for high performance.
- **PostgreSQL Support:**  
  Uses asyncpg and environment-driven configuration for database connectivity.
- **Docker-Ready:**  
  Easily deployable in containerized environments.
- **Modular Architecture:**  
  Clear separation between data models, services, repositories, and agents.

---

## API Endpoints

### FAQ Management

- `POST /faqs/create`  
  Create a new FAQ entry.
- `GET /faqs/{id}`  
  Retrieve a specific FAQ.
- `GET /faqs`  
  List all FAQs.
- `PUT /faqs/{id}`  
  Update a specific FAQ.
- `DELETE /faqs/{id}`  
  Remove a specific FAQ.

### AI Agent

- `POST /ask`  
  Provide a question; get an AI-generated answer based on stored FAQs.

---

## Usage Example

### Adding an FAQ

```http
POST /faqs/create
Content-Type: application/json

{
  "question": "How do I reset my password?",
  "answer": "Click 'Forgot Password' on the login page and follow the instructions."
}
```

### Asking the AI Agent

```http
POST /ask
Content-Type: application/json

{
  "question": "How can I change my password?"
}
```

Response:

```json
{
  "answer": "Click 'Forgot Password' on the login page and follow the instructions.",
  "question": "How can I change my password?"
}
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/MikolajKocik/Smart_FAQ_Service.git
cd Smart_FAQ_Service
```

### 2. Environment Variables

Create a `.env` file in the root directory and set:

```
OPENAI_API_KEY=your_openai_api_key
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_NAME=...
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

Set up your PostgreSQL database and run any initial migrations if needed.

### 5. Start the Service

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 6. Docker Deployment

A `Dockerfile` and/or `docker-compose.yml` may be included for easy deployment.  
*(Check the repository for these files and usage instructions.)*

---

## Project Structure

```
app/
  main.py              # FastAPI app with endpoints
  services/            # Business logic (FAQ management, logging)
  repositories/        # Database access layer
  dtos/                # Data transfer objects (FAQ schemas)
  models/              # Domain models
  db/                  # Database connection and schemas
  exceptions/          # Custom error classes

agent/
  ai_agent.py          # AI agent logic using OpenAI and LangChain

.env.example           # Example environment config
requirements.txt       # Python dependencies
```

---

## Requirements

- Python 3.10+
- PostgreSQL (asyncpg)
- OpenAI API Key (for AI agent functionality)
- Docker (optional, for containerized deployment)
