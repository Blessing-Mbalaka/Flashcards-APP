# 🎓 StudyHub - Quick Start Guide

## ✅ What's Been Set Up

Your flashcard application is now a **complete Django web application** with:

### Backend (Django REST API)
- ✅ Django project initialized
- ✅ REST API with full CRUD operations
- ✅ Database models for Decks, Flashcards, and Study Sessions
- ✅ File upload endpoint for JSON flashcards
- ✅ Export endpoint to download decks
- ✅ Study session tracking with statistics
- ✅ Demo data pre-loaded (Biology, Chemistry, History decks)

### Frontend
- ✅ Modern, responsive UI with animations
- ✅ **Demo Mode** - Test with hardcoded data (no database)
- ✅ **Live Mode** - Full integration with Django backend
- ✅ Mode toggle to switch between demo and live
- ✅ Real-time stats tracking
- ✅ Spaced repetition indicators

## 🚀 How to Use

### Access the Application
The server is running at: **http://localhost:8000**

### Two Modes of Operation

#### 🎮 Demo Mode (Default)
- Pre-loaded sample flashcards
- No database required
- Perfect for testing and tours
- Upload JSON files (loaded locally, not saved)
- Click "Demo Mode" button to activate

#### 🔴 Live Mode
- Full database integration
- Upload and save flashcards permanently
- Track study sessions and progress
- Export your decks as JSON
- Click "Live Mode" button to activate

## 📝 Using the App

### Demo Mode Workflow
1. Open http://localhost:8000
2. Click "🎮 Demo Mode" (active by default)
3. Select a demo deck from the sidebar
4. Study using the flashcard interface
5. Click cards to flip them
6. Mark answers as correct/wrong
7. Track your progress

### Live Mode Workflow
1. Click "🔴 Live Mode"
2. Enter a deck name in the text box
3. Click "Upload JSON" and select a file
4. Your deck is saved to the database
5. Study your custom flashcards
6. Progress is tracked in study sessions

## 📤 Uploading Flashcards

### JSON Format Option 1 (Simple)
```json
[
  {
    "question": "What is Python?",
    "answer": "A programming language",
    "spacedRepetition": false
  }
]
```

### JSON Format Option 2 (Full)
```json
{
  "deck_name": "My Deck",
  "description": "Description here",
  "flashcards": [
    {
      "question": "Question here?",
      "answer": "Answer here",
      "spacedRepetition": true
    }
  ]
}
```

**Tip**: Click "⬇️ Download Template" to get a sample JSON file!

## 🔌 API Endpoints

All endpoints are available at `/api/`:

### Decks
- `GET /api/decks/` - List all decks
- `POST /api/decks/upload/` - Upload flashcards
- `GET /api/decks/{id}/` - Get deck with flashcards
- `GET /api/decks/{id}/export/` - Export as JSON
- `GET /api/decks/public/` - Get public decks

### Flashcards
- `GET /api/flashcards/?deck={id}` - Get cards for a deck
- `POST /api/flashcards/` - Create a flashcard

### Study Sessions
- `POST /api/sessions/` - Start a study session
- `POST /api/sessions/{id}/record_answer/` - Record answer
- `POST /api/sessions/{id}/complete/` - Complete session

## 🛠️ Management Commands

### Start the Server
```bash
python manage.py runserver
```

Or use the convenience script:
```bash
start.bat
```

### Create Admin User
```bash
python manage.py createsuperuser
```

Then access admin at: http://localhost:8000/admin

### Initialize Demo Data
```bash
python manage.py init_demo_data
```

### Reset Database
```bash
python manage.py flush
```

## 📁 Project Structure

```
Flashcards WebAPP/
├── flashcards/              # Main Django app
│   ├── models.py           # Deck, Flashcard, StudySession models
│   ├── views.py            # API views and endpoints
│   ├── serializers.py      # DRF serializers
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin panel config
│   ├── templates/
│   │   └── flashcards/
│   │       └── index.html  # Main frontend
│   └── management/
│       └── commands/
│           └── init_demo_data.py
├── studyhub/               # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3             # SQLite database
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── start.bat             # Quick start script
├── README.md             # Full documentation
└── API_TESTING.md        # API testing guide

```

## 🎯 Key Features

### Study Features
- ✅ Flip cards with animations
- ✅ Mark correct/incorrect answers
- ✅ Shuffle cards
- ✅ Navigate forward/backward
- ✅ Progress tracking
- ✅ Spaced repetition badges
- ✅ Accuracy percentage

### Data Management
- ✅ Upload JSON flashcards
- ✅ Export decks as JSON
- ✅ Public/private deck sharing
- ✅ Multiple decks support
- ✅ Deck descriptions
- ✅ Card ordering

### Developer Features
- ✅ RESTful API
- ✅ CORS enabled (for frontend development)
- ✅ Admin panel
- ✅ Demo data seeding
- ✅ Study session tracking

## 🧪 Testing the API

See `API_TESTING.md` for detailed API testing examples.

Quick test with PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/decks/" -Method Get
```

## 🎨 Customization

### Change Colors
Edit the CSS in `flashcards/templates/flashcards/index.html`

### Add New Endpoints
1. Add to `flashcards/views.py`
2. Register in `flashcards/urls.py`

### Modify Models
1. Edit `flashcards/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Run: `python manage.py runserver 8080` for different port

### Database errors
- Delete `db.sqlite3`
- Run: `python manage.py migrate`
- Run: `python manage.py init_demo_data`

### CORS errors
- CORS is enabled for all origins in development
- Check `studyhub/settings.py` CORS settings

## 🎉 Next Steps

1. **Create an admin user** to access the admin panel
2. **Upload your own flashcards** in Live Mode
3. **Explore the API** using the testing guide
4. **Customize the design** to match your preferences
5. **Add authentication** for multi-user support (optional)
6. **Deploy to production** (Heroku, AWS, etc.)

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- SQLite Documentation: https://www.sqlite.org/docs.html

---

**Enjoy studying with StudyHub! 🚀**
