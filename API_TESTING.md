# API Testing Guide

## Test the API Endpoints

### 1. List All Decks
```bash
curl http://localhost:8000/api/decks/
```

### 2. Get a Specific Deck with Flashcards
```bash
curl http://localhost:8000/api/decks/1/
```

### 3. Upload a New Deck from JSON
```bash
curl -X POST http://localhost:8000/api/decks/upload/ \
  -H "Content-Type: application/json" \
  -d '{
    "deck_name": "Test Deck",
    "description": "A test deck",
    "flashcards": [
      {
        "question": "What is 2+2?",
        "answer": "4",
        "spacedRepetition": false
      },
      {
        "question": "What is the capital of France?",
        "answer": "Paris",
        "spacedRepetition": true
      }
    ]
  }'
```

### 4. Create a Study Session
```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"deck": 1}'
```

### 5. Record an Answer
```bash
curl -X POST http://localhost:8000/api/sessions/1/record_answer/ \
  -H "Content-Type: application/json" \
  -d '{"correct": true}'
```

### 6. Export a Deck
```bash
curl http://localhost:8000/api/decks/1/export/
```

### 7. Get Public Decks
```bash
curl http://localhost:8000/api/decks/public/
```

### 8. Create a Single Flashcard
```bash
curl -X POST http://localhost:8000/api/flashcards/ \
  -H "Content-Type: application/json" \
  -d '{
    "deck": 1,
    "question": "New question?",
    "answer": "New answer",
    "spaced_repetition": false,
    "order": 0
  }'
```

## PowerShell Examples

If using PowerShell, use Invoke-RestMethod:

### List Decks
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/decks/" -Method Get
```

### Upload Deck
```powershell
$body = @{
    deck_name = "PowerShell Deck"
    flashcards = @(
        @{
            question = "What is PowerShell?"
            answer = "A task automation framework"
            spacedRepetition = $false
        }
    )
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/decks/upload/" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

## Sample JSON Files

### Simple Format (flashcards_simple.json)
```json
[
  {
    "question": "What is Python?",
    "answer": "A high-level programming language",
    "spacedRepetition": false
  },
  {
    "question": "What is Django?",
    "answer": "A Python web framework",
    "spacedRepetition": true
  }
]
```

### Full Format (flashcards_full.json)
```json
{
  "deck_name": "Programming Basics",
  "description": "Essential programming concepts",
  "is_public": true,
  "flashcards": [
    {
      "question": "What is a variable?",
      "answer": "A storage location with a name and value",
      "spacedRepetition": false
    },
    {
      "question": "What is a function?",
      "answer": "A reusable block of code that performs a task",
      "spacedRepetition": true
    }
  ]
}
```

## Testing with the Web Interface

1. Open http://localhost:8000
2. Try **Demo Mode** first to see how it works
3. Switch to **Live Mode**
4. Enter a deck name
5. Upload a JSON file
6. Study the flashcards
7. Check the stats tracking

## Django Admin

1. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

2. Visit http://localhost:8000/admin

3. Manage decks, flashcards, and sessions through the admin interface
