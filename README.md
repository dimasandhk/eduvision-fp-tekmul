# OCR Camera App 📸💬

A modern web application that captures images from your camera, extracts text using OCR, and provides an AI-powered chat interface to discuss the extracted text.

## ✨ Features

- **📷 Camera Capture**: Access webcam directly from browser
- **🔍 OCR Processing**: Extract text with confidence scores and bounding boxes
- **✅ Accept/Reject Flow**: Review results before proceeding
- **🤖 AI Chat**: Powered by DeepSeek AI for intelligent text analysis
- **📱 Responsive Design**: Works on desktop and mobile
- **🎨 Clean UI**: Simple, modern interface

## 🚀 Quick Start

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Setup** (optional):

   ```bash
   python setup.py
   ```

3. **Start the App**:

   ```bash
   python app.py
   ```

   Or use the batch file: `run_app.bat`

4. **Open Browser**: Go to `http://localhost:5000`

## 🔧 Configuration

Edit `config.py` to customize:

- DeepSeek API key (for enhanced AI features)
- OCR languages and confidence threshold
- Server settings

## 🎯 How to Use

1. **Start Camera** → Allow camera permissions
2. **Capture Image** → Position text in front of camera
3. **Review Results** → See extracted text with bounding boxes
4. **Choose Action**:
   - ✅ **Accept**: Start AI chat about the text
   - 🔄 **Try Again**: Capture new image
5. **Chat with AI** → Ask questions, get translations, summaries, etc.

## 🤖 AI Features

The AI assistant can help with:

- 🌐 **Translations** to different languages
- 📝 **Summaries** and explanations
- 📊 **Text analysis** (word count, etc.)
- ❓ **Q&A** about the content
- 💡 **Insights** and suggestions

## 💻 Requirements

- Python 3.7+
- Webcam access
- Modern web browser
- Internet connection (for AI features)

## 📦 Dependencies

- Flask (web framework)
- OpenCV (image processing)
- EasyOCR (text recognition)
- OpenAI (AI integration)
- Pillow (image handling)

## 🔑 API Setup

1. Sign up at [DeepSeek Platform](https://platform.deepseek.com)
2. Get your API key
3. Add it to `config.py`:
   ```python
   DEEPSEEK_API_KEY = "sk-your-actual-api-key"
   ```

> **Note**: The app works without an API key for basic functionality, but AI features require a valid key.

## 🛠️ Troubleshooting

- **Camera not working**: Check browser permissions
- **OCR poor quality**: Ensure good lighting and clear text
- **AI not responding**: Check your API key in config.py
- **Installation issues**: Make sure Python and pip are properly installed

## 📱 Browser Support

- Chrome/Chromium ✅
- Firefox ✅
- Safari ✅
- Edge ✅

## 🎨 UI Design

The interface features:

- Clean, minimal design
- Smooth animations
- Mobile-responsive layout
- Intuitive controls
- Real-time feedback
