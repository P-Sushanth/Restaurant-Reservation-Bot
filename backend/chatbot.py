import re
from datetime import datetime

class Chatbot:
    def __init__(self):
        self.context = {} # To store conversation state if needed (e.g., asking for missing details)

    def extract_intent(self, message: str):
        message = message.lower()
        
        if any(word in message for word in ["menu", "food", "eat", "list"]):
            return "get_menu"
        
        if any(word in message for word in ["book", "reserve", "reservation", "table"]):
            return "make_reservation"
            
        if any(word in message for word in ["available", "free", "open", "time"]):
            return "check_availability"
            
        if any(word in message for word in ["cancel", "delete", "remove"]):
            return "cancel_reservation"
            
        if any(word in message for word in ["hello", "hi", "hey"]):
            return "greeting"
            
        return "unknown"

    def extract_entities(self, message: str):
        """
        Attempt to extract date, time, and guests from natural language.
        Very basic extraction for demonstration.
        """
        entities = {}
        
        # Extract guests (e.g., "for 2", "2 people")
        guests_match = re.search(r'(\d+)\s*(people|guests|persons|pax)?', message)
        if guests_match:
            entities['guests'] = int(guests_match.group(1))
            
        # Extract time (e.g., "7 pm", "19:00")
        time_match = re.search(r'(\d{1,2})[:\.]?(\d{2})?\s*(am|pm)?', message.lower())
        if time_match:
            # This is a very simplified parser and might trigger false positives.
            # In a real app, use dateparser or similar library.
            pass 
            
        return entities

    def get_response(self, message: str):
        intent = self.extract_intent(message)
        
        if intent == "greeting":
            return {
                "message": "Hello! Welcome to The Gourmet Bot. I can show you the menu, check availability, or make a reservation for you.",
                "action": None
            }
            
        if intent == "get_menu":
            return {
                "message": "Here is our menu. It's compressed for speed!",
                "action": "fetch_menu"
            }
            
        if intent == "make_reservation":
            return {
                "message": "I'd act on that if I had all the details! Please use the form or provide date, time, and party size.",
                "action": "prompt_reservation"
            }
            
        if intent == "check_availability":
            return {
                "message": "I can check that for you. What date and time?",
                "action": "prompt_availability"
            }
            
        if intent == "cancel_reservation":
            return {
                "message": "To cancel, please provide your reservation ID.",
                "action": "prompt_cancellation"
            }
            
        return {
            "message": "I'm not sure I understand. Try asking for the menu or booking a table.",
            "action": None
        }

bot = Chatbot()
