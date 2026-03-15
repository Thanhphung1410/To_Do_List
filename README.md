# To-Do List - Levels 0–4

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Base Endpoints

- `GET /health` -> `{ "status": "ok" }`
- `GET /` -> `{ "message": "Hello To-Do" }`

## API (v1)

Base prefix: `/api/v1`

### Create
- `POST /api/v1/todos`

```json
{
  "title": "Buy milk",
  "description": "2 bottles",
  "is_done": false
}
```

### List (filter/search/sort/pagination)
- `GET /api/v1/todos?is_done=false&q=milk&sort=-created_at&limit=10&offset=0`

Response:
```json
{
  "items": [],
  "total": 0,
  "limit": 10,
  "offset": 0
}
```

### Get by id
- `GET /api/v1/todos/{id}`

### Update (full)
- `PUT /api/v1/todos/{id}`

### Patch (partial)
- `PATCH /api/v1/todos/{id}`

### Delete
- `DELETE /api/v1/todos/{id}`

### Complete
- `POST /api/v1/todos/{id}/complete`
