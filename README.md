# AI Chatbot with OpenAI API and Flask
An interactive chatbot API built using Flask and OpenAI's GPT model. The application follows the Model-View-Controller (MVC) architecture and is deployed on Azure. The application is containerized using Docker for easy development and deployment.

## Features
- User authentication and management.
- Real-time chat interface.
- Conversations stored in a structured database.
- Continuous Integration and Continuous Deployment (CI/CD) pipelines.
- Test-Driven Development (TDD) approach.j
- Dockerized application for consistent development and deployment.

## Tools & Technologies
- Backend: Python, Flask
- AI Model: OpenAI API
- Deployment: Azure
- Database: PostgreSQL
- CI/CD: GitHub Actions
- Testing: Pytest
- Containerization: Docker, docker-compose

## Architecture
### Models
1. User Model
  - Represents individual users.
  - Fields: id, name, email, password_hash, is_guest, phone_number, origin.
  - Passwords are hashed for security.
  - Users can be guests, allowing them to test the application without registration.
2. Conversation Model
  - Represents a conversation between the user and the chatbot.
  - Fields: id, user_id, messages, last_updated, is_finished.
  - Each conversation can have multiple messages.
3. Message Model
  - Represents individual messages in a conversation.
  - Fields: id, conversation_id, role, content, created_at.
  - Messages can be converted to a dictionary format for easy processing.

### API Endpoints
1. Error Handlers
  - Handle various HTTP errors like 400 (Bad Request), 401 (Unauthorized), and 404 (Not Found).
2. /chat/initial [GET]
  - Initializes a conversation.
  - Requires an API key for authentication.
  - Returns a JWT token and the initial message from the chatbot.
3. /chat [POST]
  - Handles the chat interaction.
  - Requires a JWT token and the message content.
  - Returns the chatbot's response.
4. /chat/whatsapp [GET]
  - Verifies incoming requests for WhatsApp integration.
  - Returns a challenge if the token is valid.
5. /chat/whatsapp [POST]
  - Handles incoming messages from WhatsApp.
  - Validates the payload signature.
  - Processes the incoming message and returns an appropriate response.
### Security
- The application uses HMAC and JWT for security.
- Passwords are hashed using werkzeug.security.
- Payload signatures are validated for incoming requests.

## Setup & Installation

Clone the Repository:
```
git clone https://github.com/andresacg30/jarvis
cd jarvis
```
Build Docker Image:

```
make build
```
Run the Application:
```
make run
```
Stop the Application:
```
make stop
```
Restart the Application:
```
make restart
```
Clean Database:
```
make clean_db
```
Initialize Database:
```
make init_db
```
Tag Docker Image:
```
make docker_tag
```

## Testing
To run tests, execute:
```
pytest
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
