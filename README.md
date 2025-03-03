# Contra Coffee Chatbot

Welcome to the **Contra Coffee Chatbot**, a Streamlit-based AI chatbot that interacts with users to provide information and recommendations about Contra Coffee. The chatbot utilizes OpenAI's Assistant API to process and respond to user queries in a conversational manner.

##  Features
-  AI-powered chatbot using OpenAI Assistant API
-  Maintains conversation history within the session
-  Fast and interactive responses
-  User-friendly interface with Streamlit

##  Requirements
Ensure you have the following installed:
- Python 3.8+
- Streamlit
- OpenAI Python SDK

##  Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/ramishamoosa/chatbot-for-resturants.git
   cd chatbot-for-resturants
   ```
2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install openai streamlit
   ```

##  Setup API Keys
1. Get your **OpenAI API Key** from [OpenAI](https://openai.com/)
2. Update the script with your API key:
   ```python
   openai.api_key = "your-openai-api-key"
   ```
3. Add your **Assistant ID**:
   ```python
   ASSISTANT_ID = "your-assistant-id"
   ```

##  Running the Chatbot
Start the chatbot with the following command:
```bash
streamlit run chatbot.py
```

##  How It Works
1. Initializes an OpenAI **thread** to manage conversation context.
2. Displays chat history and listens for **user input**.
3. Sends user queries to OpenAI Assistant API.
4. Waits for the assistant's **response** and updates the chat.
5. Displays the response and **maintains chat history**.



