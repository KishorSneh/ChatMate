# Chat-Mate

An AI-Based Intelligent Academic Assistant

## Project Description

Chat-Mate is a Flask-based AI-powered chatbot system designed to assist users with academic learning through intelligent interaction. The system allows users to upload study materials, ask questions, generate MCQs, summaries, and flash cards, and receive context-aware responses.

The project focuses on demonstrating the design and implementation of an intelligent learning assistant rather than competing with commercial AI platforms.

## Key Features: 
- User authentication and session management
- Document-based question answering (PDF support)
- OCR-based text extraction from images
- MCQ generation
- Short and long answer generation
- Flash card generation based on selected chapters
- Chat history tracking
- Admin dashboard for monitoring and management

## System Architecture

Chat-Mate follows a client-server architecture:
- Frontend handles user interaction through a web interface
- Backend processes requests using Flask
- AI modules handle query understanding and response generation
- Database manages users, sessions, and logs
- The system can be deployed locally or on a private server.

## Technology Stack
### Backend
- Python
### Frontend
- Flask
- HTML
- CSS
- JavaScript

### AI & Processing
- PDF text extraction
- OCR for image handling

### Database
- SQLite 

## Installation & Setup
### Prerequisites
- Python 3.9 or above
- pip package manager

### Steps
```bash
git clone https://github.com/your-username/chat-mate.git
cd chat-mate
pip install -r requirements.txt
python server.py
```

The application will run on:
```bash
http://127.0.0.1:5000
```

## Usage
- Register or log in as a user
-Upload study materials (PDF or image)
- Ask questions related to the uploaded content
- Generate MCQs, summaries, or flash cards
- View chat history and responses
Admins can access the dashboard to monitor system activity and manage content.

## Modules
- User Interaction & Session Management
- Authentication & Authorization
- File Management (PDF & OCR)
- AI Processing
- Learning Content Generation
- Database Management
- Admin Dashboard

## Future Enhancements
- Voice-based interaction
- Mobile application support
- Multilingual support
- Advanced analytics for admin dashboard
- Cloud deployment
- Spaced repetition for flash cards

## Contributors
- Kishor Sneh
- Mansuri Saniya
- Shah Rose
* Guided by: Ms. Happy Patel
### Department of Computer Science, Gujarat University

## License
This project is developed for academic purposes
