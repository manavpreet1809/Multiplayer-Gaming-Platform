# Ryan Validation Notes

## Context
Current proposed stack:
- React + TypeScript (client)
- Django/Python (backend API)
- MongoDB (database)

---

## Plan A (my recommendation):

### Stack
- Backend: Java + Spring Boot
- Database: PostgreSQL
- Migrations: Flyway
- Testing: JUnit + integration tests
- UI: javaFx or react

### Architecture
- REST endpoints for account, lobby, matchmaking, session setup.
- turn updates
- board state updates
- match/game end notifications
- Server-authoritative game engine and move validation.
- Repository interfaces for database(not needed can be stubbed maybe we add later for extra credit?):
- `UserRepository`
- `MatchRepository`
- `StatsRepository`
- `LeaderboardRepository`

### Why this fits the class project
- Closer to current starter repo (Maven + JavaFX/react + Java-first setup).
- Lower onboarding cost for a large mixed-skill team.
- Fewer technologies to coordinate.

---

## Plan B (closer to their plan): Python + FastAPI + Mongo

### Stack
- Backend: Python + FastAPI
- Database: MongoDB
- Testing: Pytest
- Frontend: React + TypeScript (single frontend)

### Architecture Constraints (must-have)
- Clear module boundaries:
- auth
- lobby/matchmaking
- game session + move validation
- stats/leaderboard
- persistence adapters
- Repository interface pattern still required (do not scatter database calls).

### Main risks
- Higher skill barrier for less experienced teammates.
- Cross-stack friction (Python backend + React frontend + Mongo + async realtime).
- More likely that advanced students carry most of the implementation.

---

## Why Plan A over the Initial Plan (Component-by-Component)

### 1) Backend Framework: Spring Boot over Django.
- Team fit: existing course setup and repo are Java/Maven already.
- everyone already knows java already, worried that if we use smth like react the students who dont know it will quickly fall behind.
- API knowledge isnt a requirement so same issue as react, people could quickly fall behind.
- fewer cross-language handoff issues between backend and game logic.

### 2) Database: PostgreSQL over MongoDB
- Data shape in this project is relational-heavy:
- users
- sessions/matches
- participants
- move history
- stats/leaderboards
- SQL querying is straightforward for leaderboard and history views.

### 4) Repo/Team Workflow
- Plan A uses tech that all students should be familiar with, reduces people learning API's/ react. 
- New contributors can become productive faster.

### 5) Risk Profile for 20-Person Team
- Initial plan (React + Django + Mongo) is valid technically, but higher coordination risk.
- Plan A is more conservative and more likely to finish with broad contributor participation.
- For class grading, reliable integration and demonstrable end-to-end flows are more valuable than tech complexity.

---
