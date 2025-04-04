# app.py (Updated)
from flask import Flask, request, jsonify, render_template
import random
import re # Using regex for slightly better matching

app = Flask(__name__)

# --- Business Name Constant ---
BUSINESS_NAME = "TechBridge Innovations"
# --- Location Constant (based on context) ---
BUSINESS_LOCATION = "Randburg, Gauteng, South Africa"
# --- Contact Info Constants (Replace with actuals) ---
SUPPORT_EMAIL = "support@techbridgeinnovations.co.za" # Example email
SUPPORT_PHONE = "011 109 7412" # Example phone

# --- Simple FAQ Database ---
# Using a list of dictionaries for more flexible matching (keywords, regex)
faqs = [
    {
        "keywords": ["hours", "open", "working hours", "time"],
        "question": "What are your operating hours?",
        # Answer updated to include business name
        "answer": f"{BUSINESS_NAME} is open Monday to Friday, 9 AM to 5 PM SAST."
    },
    {
        "keywords": ["location", "address", "where are you", "situated"],
        "question": "What is your location?",
        # Answer updated to include business name and location constant
        "answer": f"{BUSINESS_NAME}'s main office is based in {BUSINESS_LOCATION}."
    },
    {
        "keywords": ["contact", "support", "phone", "email", "help"],
        "question": "How can I contact support?",
        # Answer updated to include business name and contact constants
        "answer": f"You can reach {BUSINESS_NAME} support via email at {SUPPORT_EMAIL} or call us at {SUPPORT_PHONE} during business hours."
    },
    {
        "keywords": ["services", "offer", "what do you do"],
        "question": "What services do you offer?",
        # Answer updated to include business name
        "answer": f"{BUSINESS_NAME} specializes in providing innovative tech solutions, including custom software development, RPA automation, and data analysis services."
    },
    {
        "keywords": ["price", "cost", "pricing", "quote"],
        "question": "Can I get pricing information?",
         # Answer updated to include business name
        "answer": f"Pricing varies depending on the project scope. Please contact {BUSINESS_NAME} for a detailed quote tailored to your needs."
    },
    {
        "keywords": ["name", "business name", "company name", "who are you"], # Added keywords for name
        "question": "What is the business name?", # Added specific question
        "answer": f"Our business name is {BUSINESS_NAME}." # Added specific answer
    },
    {
        "keywords": ["hi", "hello", "hey", "greetings"],
        "question": "Greetings",
         # Answer updated to potentially include business name
        "answer": random.choice([
            f"Hello! Welcome to {BUSINESS_NAME}. How can I help you today?",
            "Hi there! What can I do for you?",
            f"Hey! Ask me anything about {BUSINESS_NAME}."
        ])
    },
     {
        "keywords": ["thanks", "thank you", "appreciate it"],
        "question": "Thanks",
        "answer": random.choice(["You're welcome!", "Happy to help!", "No problem! Let me know if there's anything else."])
    },
    {
        "keywords": ["bye", "goodbye", "see ya"],
        "question": "Goodbye",
        "answer": random.choice([f"Goodbye! Thanks for contacting {BUSINESS_NAME}.", "Have a great day!", "See you later!"])
    },
    # Add more FAQs here following the same structure
]

# --- Fallback Responses ---
fallback_responses = [
    "I'm sorry, I don't have the answer to that right now. Could you please rephrase or ask about our services, location, or hours?",
    f"That's a good question! For specific details, you might need to contact {BUSINESS_NAME} support directly at {SUPPORT_EMAIL}.",
    "I understand you're asking about that, but I'm still learning. Try asking about our core services or contact details.",
    f"My apologies, I couldn't find information on that in my knowledge base. Please reach out to the {BUSINESS_NAME} team for assistance."
]

# --- Chatbot Logic ---
def get_bot_response(user_message):
    """Finds a relevant FAQ answer based on keywords."""
    user_message_lower = user_message.lower().strip()

    if not user_message_lower:
        return "Please type a message!"

    best_match = None
    highest_match_count = 0

    # Iterate through FAQs to find the best keyword match
    for faq in faqs:
        match_count = 0
        for keyword in faq["keywords"]:
            # Use regex to find whole word matches (more reliable)
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', user_message_lower):
                 match_count += 1
            # Allow partial match for greetings/thanks/bye for flexibility
            elif keyword.lower() in ["hi", "hello", "hey", "greetings", "thanks", "thank you", "bye", "goodbye"] and keyword.lower() in user_message_lower:
                match_count +=1

        # Simple logic: prioritize the faq with the most matching keywords
        if match_count > highest_match_count:
            highest_match_count = match_count
            best_match = faq

    if best_match and highest_match_count > 0:
        # Check if the answer needs dynamic elements (like random choice)
        if isinstance(best_match["answer"], list):
             return random.choice(best_match["answer"])
        else:
            return best_match["answer"]
    else:
        # If no keywords match, return a random fallback response
        return random.choice(fallback_responses)

# --- Flask Routes ---
@app.route("/")
def home():
    """Serves the main HTML page."""
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handles incoming chat messages."""
    try:
        user_message = request.json["message"]
        response = get_bot_response(user_message)
        return jsonify({"reply": response})
    except Exception as e:
        print(f"Error processing chat request: {e}")
        # Provide a slightly more informative error for debugging if needed
        # return jsonify({"reply": f"Sorry, something went wrong: {str(e)}"}), 500
        return jsonify({"reply": "Sorry, something went wrong on my end."}), 500


if __name__ == "__main__":
    # Use port 5000 or another if needed, host='0.0.0.0' makes it accessible on your network
    app.run(debug=False, host='0.0.0.0', port=5000)