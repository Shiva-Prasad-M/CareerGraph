# CareerGraph

CareerGraph is a small career exploration application built around a graph database.

The idea is simple: instead of treating skills, job roles, companies, and learning resources as separate lists, CareerGraph connects them. A user selects the skills they already have and the application shows roles that match those skills, the skills they are missing, recommended learning resources, and how the different parts of the career path are connected.

The project was built as part of the Wexa AI CognoDB take-home assignment.

## What it does

A user can:

* Select their current skills
* Find roles that match those skills
* See a match percentage for each role
* Check which skills are missing for a selected role
* Get recommended courses for those gaps
* Explore connections between skills, roles, and companies
* View basic statistics about the graph

The main purpose is not to provide a perfect career recommendation system. It is to demonstrate how a graph database can be used when the relationships between different pieces of information are important.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Neo4j Python Driver
* Pydantic
* Uvicorn

### Frontend

* React
* Vite
* React Flow
* JavaScript
* CSS

### Database

* CognoDB
* openCypher
* Bolt protocol

CognoDB is used as the graph database and is accessed through the official Neo4j Python driver.

---

## Why a Graph Database?

The main reason for using a graph database here is the number of relationships between the entities.

For example:

```text
Docker
   │
   ├── REQUIRED_FOR → Backend Developer
   │                       │
   │                       └── OFFERED_BY → Company
   │
   └── RELATED_TO → Kubernetes
```

In a relational database, these connections would normally require several tables and joins.

With a graph database, the relationships are part of the data model itself. This makes queries such as "which roles are connected to the skills I already know, and which companies offer those roles?" more natural to express.

Another example is finding related skills through multiple relationships:

```text
Skill → Related Skill → Role → Company
```

This type of traversal is one of the main reasons graph storage makes sense for this application.

---

## Data Model

The current graph contains the following main node types:

```text
(:Skill)
(:Role)
(:Company)
(:Course)
(:Category)
```

Relationships include:

```text
(:Skill)-[:REQUIRED_FOR]->(:Role)

(:Role)-[:OFFERED_BY]->(:Company)

(:Course)-[:TEACHES]->(:Skill)

(:Skill)-[:RELATED_TO]->(:Skill)

(:Skill)-[:SIMILAR_TO]->(:Skill)
```

### Basic model

```text
                         ┌──────────────┐
                         │   Category   │
                         └──────┬───────┘
                                │
                                │
                         ┌──────▼───────┐
                         │    Course    │
                         └──────┬───────┘
                                │
                              TEACHES
                                │
                                ▼
┌──────────────┐       ┌────────────────┐       ┌───────────────┐
│    Skill     │──────▶│      Role      │──────▶│    Company    │
└──────┬───────┘       └────────────────┘       └───────────────┘
       │
       │ RELATED_TO
       ▼
┌──────────────┐
│    Skill     │
└──────────────┘
```

The exact graph can grow as more career data is added.

---

## Example Graph

Suppose a user selects:

```text
Docker
JavaScript
REST APIs
```

The application can follow relationships in the graph to find roles that require those skills.

A simplified traversal looks like:

```text
Docker
  ↓
Related Skill
  ↓
Backend Developer
  ↓
Company
```

The application then uses the selected skills and required skills of the role to calculate the match and identify gaps.

---

## Main Features

### 1. Skill selection

The dashboard loads available skills from CognoDB.

Users can select one or more skills before searching for career options.

### 2. Career matching

The backend compares the selected skills with the skills required by available roles.

The result contains the matching roles and their match percentages.

### 3. Skill gap

After selecting a role, CareerGraph checks which required skills are not present in the user's selected skills.

For example:

```text
Your skills:

JavaScript
REST APIs
Node.js

Role:

Backend Developer

Missing:

Docker
PostgreSQL
```

### 4. Learning recommendations

The application uses course-to-skill relationships to suggest learning resources related to the missing skills.

### 5. Graph explorer

The graph view displays the relationships between:

```text
Skills
   ↓
Related Skills
   ↓
Roles
   ↓
Companies
```

This makes the reason behind a recommendation easier to understand than showing a list of roles alone.

### 6. Graph statistics

The dashboard also shows basic information about the graph, including:

* Number of nodes
* Number of relationships

---

## Project Structure

```text
CareerGraph/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py
│   │   │   └── queries.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── skills.py
│   │   │   ├── roles.py
│   │   │   ├── companies.py
│   │   │   └── graph.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       └── career_service.py
│   │
│   ├── seed/
│   │   └── seed.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── ...
│   │
│   ├── package.json
│   └── ...
│
└── README.md
```

`.env` is not committed to the repository.

---

## Backend API

The backend exposes REST endpoints for the frontend.

### Health

```http
GET /api/health
```

Used to check whether the API can connect to CognoDB.

### Skills

```http
GET /api/skills
```

Returns the available skills.

### Career matching

```http
POST /api/graph/match
```

Example request:

```json
{
  "skills": [
    "Docker",
    "JavaScript",
    "REST APIs"
  ]
}
```

### Missing skills

```http
POST /api/graph/missing-skills
```

Checks the difference between the user's skills and the skills required for a role.

### Learning path

```http
POST /api/graph/learning-path
```

Returns learning resources connected to the missing skills.

### Graph exploration

```http
POST /api/graph/explore-related
```

Returns connected graph data used by the React Flow visualization.

### Graph statistics

```http
GET /api/graph/stats
```

Returns the number of nodes and relationships in the graph.

---

## Cypher Queries

The application uses parameterised Cypher queries through the Neo4j Python driver.

For example, career matching uses the selected skills as a query parameter rather than building a Cypher string manually.

A typical graph traversal looks like:

```cypher
MATCH (s:Skill)-[:REQUIRED_FOR]->(r:Role)
WHERE s.name IN $skills
RETURN r
```

A multi-hop traversal can follow:

```text
Skill → Role → Company
```

For example:

```cypher
MATCH (s:Skill)-[:REQUIRED_FOR]->(r:Role)-[:OFFERED_BY]->(c:Company)
WHERE s.name IN $skills
RETURN s.name, r.name, c.name
```

This is one of the places where the graph model is useful because the query directly describes the relationships being explored.

---

## Database Constraints

The graph uses uniqueness constraints for important entities.

```cypher
CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
FOR (s:Skill)
REQUIRE s.name IS UNIQUE;
```

Similar constraints are used for:

* Role
* Company
* Course
* Category

This prevents duplicate entities from being inserted during seeding.

---

## Seed Data

The repository includes a seed script for creating the initial graph data.

The seed data contains realistic examples of:

* Skills
* Roles
* Companies
* Courses
* Categories
* Relationships between them

The goal of the seed data is to provide enough connections for the application to demonstrate graph traversal without requiring a large external dataset.

---

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/Shiva-Prasad-M/CareerGraph.git
cd CareerGraph
```

### 2. Create a CognoDB instance

Create a free CognoDB instance from the CognoDB Cloud console.

Copy the connection URI and password when the instance is created.

The password should be stored as an environment variable.

### 3. Backend setup

Open the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
backend/.env
```

Add:

```env
COGNODB_URI=your_cognodb_bolt_uri
COGNODB_PASSWORD=your_cognodb_password
```

Do not commit this file.

### 4. Load the graph

Run the seed script:

```bash
python -m seed.seed
```

This creates the initial graph data.

### 5. Start the backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will provide the local frontend URL.

---

## Environment Variables

The backend requires:

```env
COGNODB_URI=
COGNODB_PASSWORD=
```

The frontend uses:

```env
VITE_API_URL=
```

Production credentials are configured through the hosting provider rather than committed to Git.

---

## Error Handling

The backend handles database failures instead of exposing raw application errors to the frontend.

For example, if CognoDB is unavailable, API endpoints return an appropriate HTTP error response and the frontend displays an error state.

The UI also includes loading and empty states so that a failed or empty request does not leave the page looking broken.

---

## Deployment

The application can be deployed as two services:

```text
React/Vite frontend
        │
        ▼
FastAPI backend
        │
        ▼
CognoDB
```

The backend needs the CognoDB connection variables configured in the hosting provider.

The frontend needs the deployed backend URL configured through:

```env
VITE_API_URL
```

The backend CORS configuration must also include the deployed frontend URL.

### Live Demo

> Add the deployed frontend URL here after deployment.

```text
https://your-careergraph-demo-url
```

### API

> Add the deployed backend URL here after deployment.

```text
https://your-careergraph-api-url
```

---

## Screenshots

Add screenshots of the finished application here.

Recommended screenshots:

1. Dashboard with skills selected
2. Career match results
3. Skill gap and learning recommendations
4. Graph Explorer
5. Graph statistics
6. Swagger API documentation

Example:

```text
docs/
├── dashboard.png
├── career-matches.png
├── skill-gap.png
├── graph.png
└── swagger.png
```

---

## What I Learned

The main thing I wanted to understand with this project was where a graph database actually makes sense.

The interesting part wasn't just storing skills and roles. It was being able to follow the relationships between them and use those relationships to answer questions such as:

* Which roles are connected to my current skills?
* What skills am I missing for a particular role?
* Which companies are connected to those roles?
* What learning resources are related to the missing skills?
* Which skills are related to each other?

That made CognoDB a better fit for this use case than simply storing the same information as unrelated records.

---

## Future Improvements

There are several things that could be added if the project were expanded:

* User profiles and saved career paths
* More comprehensive career data
* Experience-level based matching
* Salary and location information
* More detailed learning paths
* Authentication
* Better ranking of career recommendations
* More graph traversal options

For this assignment, the focus was kept on the graph model, API, and the core career exploration flow.

---

## Assignment

Built for the Wexa AI CognoDB take-home assignment.

Repository:

https://github.com/Shiva-Prasad-M/CareerGraph
