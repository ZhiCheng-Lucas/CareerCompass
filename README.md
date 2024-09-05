# CareerCompass

## Project Structure

This project follows a modular structure to organize code and separate concerns. Here's an overview of the main components:

### `app/`: Main Application Package

- `main.py`: Entry point of the application
- `config.py`: Configuration settings

#### `api/`: API-related Code

- `routes.py`: Defines API routes
- `endpoints/`: Organizes endpoint logic by feature

#### `core/`: Core Functionality

- `security.py`: Handles authentication and authorization
- `database.py`: Database connection and session management

#### `models/`: Database Models (for MongoDB)

#### `schemas/`: Pydantic Schemas

Used for request/response validation

#### `services/`: Business Logic and External Service Integrations

- `linkedin_scraper.py`: Implements the LinkedIn job scraper
- `resume_parser.py`: Handles resume parsing and analysis
- `job_matcher.py`: Matches resumes to jobs
- `email_service.py`: Manages email notifications
- `calendar_service.py`: Integrates with calendar APIs

#### `utils/`: Utility Functions and Helpers

- `openai_helper.py`: Wrapper for OpenAI API interactions
- `accessibility.py`: Implements accessibility features

### `tests/`: Test Files

### `scripts/`: Utility Scripts

Includes database initialization

### Configuration Files

- `.env`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`

## Getting Started

- Todo

## License

- Todo
