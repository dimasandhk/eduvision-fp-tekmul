import cv2
import easyocr
import base64
import io
import numpy as np
from flask import Flask, render_template, request, jsonify, session, redirect
from PIL import Image
import uuid
import os
from openai import OpenAI

# Load configuration
try:
    from config import (
        DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, OCR_LANGUAGES, 
        OCR_CONFIDENCE_THRESHOLD, SECRET_KEY, DEBUG, HOST, PORT
    )
    print("✅ Configuration loaded from config.py")
except ImportError as e:
    print(f"⚠️ Could not load config.py: {e}")
    print("📝 Using fallback configuration...")
    # Fallback configuration if config.py doesn't exist
    DEEPSEEK_API_KEY = "sk-xxx"
    DEEPSEEK_BASE_URL = "https://openrouter.ai/api/v1"
    OCR_LANGUAGES = ['en', 'id']
    OCR_CONFIDENCE_THRESHOLD = 0.3
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize OpenAI client for DeepSeek
try:
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL
    )
    print("✅ OpenAI client initialized for DeepSeek")
except Exception as e:
    print(f"⚠️ Could not initialize OpenAI client: {e}")
    client = None

class OCRProcessor:
    def __init__(self, languages=None):
        if languages is None:
            languages = OCR_LANGUAGES
        print("Initializing EasyOCR...")
        self.reader = easyocr.Reader(languages)
        self.confidence_threshold = OCR_CONFIDENCE_THRESHOLD
        print("EasyOCR initialized!")

    def process_image(self, image_array):
        """Process image with EasyOCR and return results with bounding boxes"""
        try:
            results = self.reader.readtext(image_array)
            return results
        except Exception as e:
            print(f"Error processing image: {e}")
            return []

    def draw_results(self, image_array, results):
        """Draw bounding boxes and text on the image"""
        image = image_array.copy()
        
        for (bbox, text, confidence) in results:
            if confidence > self.confidence_threshold:  # Use configurable threshold
                # Get bounding box coordinates
                (top_left, top_right, bottom_right, bottom_left) = bbox
                top_left = (int(top_left[0]), int(top_left[1]))
                bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
                
                # Draw rectangle around text
                cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
                
                # Put text above the rectangle
                cv2.putText(image, f"{text} ({confidence:.2f})", 
                           (top_left[0], top_left[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        return image

# Initialize OCR processor
ocr_processor = OCRProcessor()

@app.route('/')
def index():
    """Main page with camera interface"""
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    """Process captured image and return OCR results"""
    try:
        # Get image data from request
        image_data = request.json['image']
        
        # Remove data URL prefix
        image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        image_array = np.array(image)
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Process with OCR
        results = ocr_processor.process_image(image_array)
        
        # Draw bounding boxes
        image_with_boxes = ocr_processor.draw_results(image_array, results)
        
        # Convert back to base64 for frontend
        image_with_boxes_rgb = cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_with_boxes_rgb)
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
          # Extract text for chat
        extracted_text = []
        for (bbox, text, confidence) in results:
            if confidence > ocr_processor.confidence_threshold:
                extracted_text.append({
                    'text': text,
                    'confidence': confidence
                })
        
        # Store extracted text in session
        session['extracted_text'] = extracted_text
        session['session_id'] = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'image_with_boxes': f"data:image/png;base64,{img_str}",
            'extracted_text': extracted_text
        })
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/update_selected_text', methods=['POST'])
def update_selected_text():
    """Update session with user-selected text items"""
    try:
        data = request.get_json()
        selected_text = data.get('selectedText', [])
        
        if not selected_text:
            return jsonify({
                'success': False,
                'error': 'No text items selected'
            })
        
        # Store selected text in session, maintaining user's order
        session['extracted_text'] = selected_text
        
        return jsonify({
            'success': True,
            'selected_count': len(selected_text)
        })
    
    except Exception as e:
        print(f"Error updating selected text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/chat')
def chat():
    """Chat interface page"""
    if 'extracted_text' not in session:
        return redirect('/')
    
    return render_template('chat.html')

@app.route('/get_initial_explanation', methods=['GET'])
def get_initial_explanation():
    """Get initial explanation of extracted text"""
    try:
        extracted_text = session.get('extracted_text', [])
        
        if not extracted_text:
            return jsonify({
                'success': False,
                'error': 'No extracted text found'
            })
        
        # Create initial explanation
        text_parts = [item['text'] for item in extracted_text]
        full_text = ' '.join(text_parts)
        
        explanation = f"""I've analyzed the image and extracted the following text:

**Extracted Text:**
{full_text}

**Text Analysis:**
- Total text segments detected: {len(extracted_text)}
- Confidence levels: {', '.join([f'{item["confidence"]:.2f}' for item in extracted_text])}

**What I can see:**
The image contains text that appears to be {'handwritten' if any(item['confidence'] < 0.7 for item in extracted_text) else 'printed'}. 

You can now ask me questions about this text, request translations, summaries, or any other analysis you'd like me to perform!"""

        return jsonify({
            'success': True,
            'explanation': explanation,
            'extracted_text': full_text
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/chat_message', methods=['POST'])
def chat_message():
    """Handle chat messages"""
    try:
        user_message = request.json['message']
        extracted_text = session.get('extracted_text', [])
        
        if not extracted_text:
            return jsonify({
                'success': False,
                'error': 'No text context available'
            })
        
        # Create context from extracted text
        text_parts = [item['text'] for item in extracted_text]
        full_text = ' '.join(text_parts)
        
        # Simple response logic (you can enhance this with actual AI/LLM integration)
        response = generate_chat_response(user_message, full_text)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_chat_response(user_message, extracted_text):
    """Generate response using OpenAI with DeepSeek model"""
    try:
        # Check if OpenAI client is available
        if client is None:
            print("⚠️ OpenAI client not available, using fallback response")
            return generate_fallback_response(user_message, extracted_text)
            
        # Create a conversation context with the extracted text
        system_prompt = f"""This will be the main context of this conversation`{extracted_text}`, 
        respond to the user's question based on the context provided."""

        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=512,
            temperature=0.8
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        # Fallback to simple responses if API fails
        return generate_fallback_response(user_message, extracted_text)

def generate_fallback_response(user_message, extracted_text):
    """Fallback response when OpenAI API is not available"""
    user_msg_lower = user_message.lower()
    
    if any(word in user_msg_lower for word in ['translate', 'translation']):
        return f"I can help translate the extracted text: '{extracted_text}'. However, I would need to know which language you'd like me to translate it to. Please specify the target language."
    
    elif any(word in user_msg_lower for word in ['summary', 'summarize']):
        return f"Here's a summary of the extracted text:\n\nThe text reads: '{extracted_text}'\n\nThis appears to be {len(extracted_text.split())} words long. Would you like me to provide more specific analysis?"
    
    elif any(word in user_msg_lower for word in ['explain', 'meaning', 'what']):
        return f"The extracted text is: '{extracted_text}'\n\nThis text appears to contain information that could be analyzed further. What specific aspect would you like me to explain?"
    
    elif any(word in user_msg_lower for word in ['count', 'words', 'characters']):
        word_count = len(extracted_text.split())
        char_count = len(extracted_text)
        return f"Text statistics:\n- Word count: {word_count}\n- Character count: {char_count}\n- Text: '{extracted_text}'"
    
    else:
        return f"I understand you're asking about the extracted text: '{extracted_text}'\n\nI can help you with:\n- Translation to other languages\n- Text analysis and summary\n- Word/character counts\n- Explanation of content\n\nWhat would you like to know more about?"

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
