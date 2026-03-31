# jarvis-assistant
A rule-based voice assistant built with Django, JavaScript, HTML, and CSS. Supports math operations, calculus, graph plotting, reminders, and basic task automation with voice interaction and a simple memory system.

The project focuses on combining backend logic, mathematical processing, voice interaction, and database storage to simulate a functional assistant. It supports both text and voice input and can handle a variety of tasks ranging from calculations to basic automation.

Features
Voice input and speech output using Web Speech API
Chat-based interface for interaction
Arithmetic operations (addition, division, multiplication, modulus)
Calculus operations like derivatives and integrals using SymPy
Trigonometric and logarithmic calculations
Graph plotting for mathematical expressions
Basic memory system (stores user name and preferences)
Task management (reminders and task listing)
Web actions:
Open YouTube
Open Spotify
Open news
Perform Google search

How it works-
User provides input through text or voice
Input is sent to the Django backend via an API
The system processes commands using rule-based conditions
Mathematical queries are handled using SymPy
Graphs are generated using Matplotlib and returned as images
Based on the command, actions like opening websites are triggered from the frontend
Responses are displayed in the UI and optionally spoken using speech synthesis
User data and tasks are stored in the database using Django ORM

Tech Stack
Backend: Django (Python)
Frontend: HTML, CSS, JavaScript
Math Engine: SymPy
Graphing: Matplotlib, NumPy
Database: SQLite
Voice: Web Speech API

This is a rule-based system, so it depends on predefined conditions to process commands. It works well for structured inputs but does not provide full natural language understanding like AI-based assistants.
