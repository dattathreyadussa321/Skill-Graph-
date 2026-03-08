# Learning Path Recommendation System — Back-end

## 1. Description
Back-end API for a Learning Path Recommendation System built with **Django 4.0** and **Neo4j Graph Database**.  
Uses graph-based algorithms to recommend personalized learning paths by analyzing career requirements, courses, and learning objects (skills, tools, frameworks, etc.).

## 2. Tech Stack
| Layer | Technology |
|-------|-----------|
| **Framework** | Django 4.0.4 |
| **Graph DB** | Neo4j 4.x (via `neomodel` + `py2neo`) |
| **Language** | Python 3.10 |
| **Algorithm** | Genetic Algorithm, Jaccard/Overlap Similarity, Graph traversal |
| **Visualization** | igraph (learning path graphs) |

## 3. Prerequisites
- **Python** 3.10+
- **pip** 20.0.4+
- **Neo4j Community/Desktop** 4.x (running on `localhost:7687`)

## 4. Setup & Run

### 4.1 Clone the Project
```bash
git clone <repository-url>
cd Learning-Path-Recommendation-System
```

### 4.2 Create & Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\activate

# Activate (CMD)
venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate
```

### 4.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 4.4 Configure Environment Variables
Copy `.localenv` to `.env` and fill in your Neo4j credentials:
```bash
copy .localenv .env
```

Edit `.env` with your values:
```env
SCHEME=bolt://
URL=localhost:7687
NEO4J_USER=neo4j
USERNAMEE=neo4j
PASSWORD=your_neo4j_password
```

### 4.5 Start Neo4j Database
Make sure Neo4j is running before making API calls.

**Option A — Neo4j Desktop:**  
Open Neo4j Desktop → Start your database on port `7687`.

**Option B — Docker:**
```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/your_neo4j_password neo4j:4.4
```

### 4.6 Run Django Server
```bash
python manage.py runserver
```
The server will start at **http://localhost:8000/**

## 5. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/apis/career/` | GET | Get all careers |
| `/apis/career/one?id=<id>` | GET | Get career by ID |
| `/apis/career/lo?id=<id>` | GET | Get learning objects needed for career |
| `/apis/lo/language/` | GET | Get all programming languages |
| `/apis/lo/knowledge` | GET | Get all knowledge LOs |
| `/apis/lo/tool` | GET | Get all tool LOs |
| `/apis/lo/platform` | GET | Get all platform LOs |
| `/apis/lo/framework` | GET | Get all framework LOs |
| `/apis/course?id=<id>` | GET | Get course info |
| `/apis/course/provided/lo?id=<id>` | GET | Get LOs provided by course |
| `/apis/course/required/lo?id=<id>` | GET | Get LOs required by course |
| `/apis/user/login?email=<email>` | GET | Login by email |
| `/apis/user/register` | POST | Register `{name, email}` |
| `/apis/user/info/?id=<id>` | GET | Get user info |
| `/apis/user/create` | POST | Create user `{id, cost, time}` |
| `/apis/user/objective` | POST | Set career objective `{user_id, career_id}` |
| `/apis/user/has` | POST | Add user skills `{user_id, list_lo}` |
| `/apis/user/need?id=<id>` | GET | Get LOs user needs |
| `/apis/user/learning-path?id=<id>` | GET | Generate learning path |
| `/admin/` | GET | Django Admin panel |

## 6. Project Structure
```
Learning-Path-Recommendation-System/
├── RecommendationSystem/     # Django settings & URLs
├── apis/                     # API views & URL routing
├── models/                   # Neo4j models (neomodel) & connection
├── services/                 # Business logic layer
├── algorithm_implementation/ # Learning path algorithm v1
├── algorithm_v2/             # Learning path algorithm v2
├── constants/                # Algorithm constants
├── utilities/                # Cypher query builders
├── static/                   # Generated learning path visualizations
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables (local)
```
