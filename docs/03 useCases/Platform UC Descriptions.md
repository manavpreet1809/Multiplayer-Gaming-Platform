# Platform Use Case Diagram (Updated) #

## Changes from Quality Feedback ##

- **UC-2**: Added UC-16: Manage Friends
- **UC-3**: UC-05 now includes lobby capacity validation

## Use Case Diagram ##

For use in [editor.plantuml.com](editor.plantuml.com):

```plantuml
@startuml
title OMG Platform - Platform Use Cases (Updated)

left to right direction
skinparam packageStyle rectangle

actor "User" as User
actor "Authenticated\nPlayer" as AuthPlayer
actor "Game Server" as Server

AuthPlayer --|> User

rectangle "Platform" {
  usecase "UC-01: View Game List" as UC01
  usecase "UC-02: Create Account" as UC02
  usecase "UC-03: Log In" as UC03
  usecase "UC-04: View Dashboard" as UC04
  usecase "UC-05: Join Game Lobby" as UC05
  usecase "UC-06: Enqueue for\nNext Available Game" as UC06
  usecase "UC-07: Chat" as UC07
  usecase "UC-08: Join Game" as UC08
  usecase "UC-09: View Profile" as UC09
  usecase "UC-10: Edit Account\nSettings" as UC10
  usecase "UC-11: Delete Account" as UC11
  usecase "UC-12: View Leaderboard" as UC12
  usecase "UC-13: Submit Move" as UC13
  usecase "UC-14: View Game Results" as UC14
  usecase "UC-15: Create / Join Party" as UC15
  usecase "UC-16: Manage Friends" as UC16
  usecase "Validate Lobby\nCapacity" as VLC
}

User --> UC01
User --> UC02
User --> UC03

AuthPlayer --> UC04
AuthPlayer --> UC05
AuthPlayer --> UC06
AuthPlayer --> UC07
AuthPlayer --> UC08
AuthPlayer --> UC09
AuthPlayer --> UC10
AuthPlayer --> UC11
AuthPlayer --> UC12
AuthPlayer --> UC13
AuthPlayer --> UC14
AuthPlayer --> UC15
AuthPlayer --> UC16

Server --> UC13
Server --> UC14

UC03 ..> UC04 : <<include>>
UC05 ..> UC07 : <<extend>>
UC05 ..> VLC : <<include>>
UC06 ..> UC08 : <<extend>>
UC08 ..> UC13 : <<include>>
UC13 ..> UC14 : <<extend>>
UC10 ..> UC09 : <<extend>>
UC16 ..> UC15 : <<extend>>

@enduml
```
