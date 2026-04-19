# IRONIQ - Indian Powerlifting AI

## Overview
Welcome to the **IRONIQ** project! 🤖💪 The Indian Powerlifting AI project aims to revolutionize how athletes train and achieve their fitness goals through advanced technology. With personalized training plans and intelligent tracking, IRONIQ is your ultimate workout companion!

## Features
- Personalized training plans tailored to your experience level
- AI-generated workout recommendations
- Progress tracking and workout logging
- Integration with Streamlit for a user-friendly web interface
- Utilization of Supabase for backend data management

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** Supabase
- **AI Technologies:** Machine Learning models for training recommendations

## System Architecture Diagram
![System Architecture](link_to_diagram)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Techno2323/powerlifting-ai.git
   cd powerlifting-ai
   ```
2. Set up your environment with Streamlit:
   ```bash
   pip install streamlit
   ```
3. Create an account on Supabase and set up your database.
4. Update the `.streamlit/secrets.toml` file with your Supabase credentials (See Configuration Guide).

## Configuration Guide for `.streamlit/secrets.toml`
```toml
[database]
url = "YOUR_SUPABASE_URL"
key = "YOUR_SUPABASE_ANON_KEY"
```

## Usage Walkthrough
### Login
- Navigate to the login page to enter your credentials.

### Creating Your First Plan
- Follow the prompts to set up your personalized training plan.

### Logging Workouts
- Use the workout logging feature to track your exercises and progress.

## Project Structure
```
/powerlifting-ai
├── .streamlit
│   └── secrets.toml
├── main.py
└── requirements.txt
```

## Training Experience Levels
- **Beginner:** For those just starting out.
- **Intermediate:** For users who have some experience.
- **Advanced:** For seasoned lifters accustomed to heavy training.
- **Elite:** For competitive powerlifters.

## Goal Types
- **Cut:** Weight loss and fat reduction.
- **Bulk:** Muscle gain and growth.
- **Build Strength:** Targeting strength improvements.
- **Powerbuilding:** A mix of bodybuilding and powerlifting.

## Diet Options
- **Vegetarian:** Plant-based meal plans.
- **Non-Vegetarian:** Includes meat in meal plans.
- **Eggetarian:** Vegetarian with eggs included.

## API Keys and Credentials Needed
Make sure to obtain the necessary API keys from Supabase and update your secrets.

## Troubleshooting Section
- If you encounter issues, follow these steps:
  - Ensure all dependencies are installed.
  - Check your Supabase credentials in `.streamlit/secrets.toml`.

## Contributing Guidelines
- Fork the repository and create a new branch for your feature.
- Follow the coding standards and ensure your code is well-documented.
- Submit a pull request with a clear description of your changes.

Happy lifting! 💪