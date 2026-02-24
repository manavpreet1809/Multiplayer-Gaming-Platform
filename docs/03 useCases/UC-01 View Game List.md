# UC-01: View Game List #

## Use Case Diagram ##

For use in [editor.plantuml.com](editor.plantuml.com), SVG also attached:

```plantuml
@startuml
title UC-01: View Game List

left to right direction
skinparam packageStyle rectangle

actor "User" as User

rectangle "Platform" {
  usecase "View Game List" as UC01
  usecase "View Game Details" as VGD
}

User --> UC01
UC01 ..> VGD : <<extend>>

@enduml
```

---

## Description ##

| Field | Detail |
|---|---|
| **Use Case ID** | UC-01 |
| **Primary Actor** | User |
| **Goal** | See available games (browse-only) |
| **Preconditions** | None (no authentication required) |
| **Trigger** | User visits the welcome page |
| **Postconditions** | None (no session created) |

**Main Success Scenario:**

1. User navigates to the welcome/landing page.
2. System retrieves the list of available games.
3. System displays the game list with basic info (name, description, player count).
4. User optionally selects a game to view more details.

**Alternative Flows:**

- **4a.** User selects a game → System displays a detail panel with game rules and current player counts.
- **4b.** User does not select a game → Use case ends.

**Exceptions:**

- **2a.** No games are available → System displays an appropriate message ("No games available at this time").
