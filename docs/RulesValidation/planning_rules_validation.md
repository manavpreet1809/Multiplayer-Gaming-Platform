# Iteration 1 Planning Document - Rules + Validation Sub-Team

## Document Metadata
- Sub-team: `Rules + Validation`
- Date: `2026-02-26`
- Authors: `Ryan Meroniuk, Colby Thompson, Kyle Naz, Prateek`
- Stack Alignment: `React + FastAPI + MongoDB + WebSockets`

## 1. Problem Being Addressed
This sub-team is responsible for gameplay correctness. Our core job is to design and enforce a server-authoritative move validation pipeline that works across games, not just one game implementation.

- Problem statement: The platform needs a consistent backend pipeline that validates every move, enforces turn order and game rules, and returns clear error states when moves are invalid.
- Why it matters to the platform-first goal: Shared validation logic is a cross-cutting platform service used by all games, and it supports reusable game-agnostic interfaces, stable integration with Platform Core/UI, and testable behavior for Quality + Testing.
- Failure impact if not handled well: Illegal moves may be accepted, turn progression can desync, players can act in the wrong session/state, and the platform becomes unreliable for integration, testing, and demonstration.

## 2. Scope and Ownership
### In Scope
- Move validation pipeline
- Server-authoritative rule enforcement
- Authentication and authorization checks for validation-relevant actions
- Validation error states and messages
- Turn-validation checks
- Validation contracts for platform core/UI/testing
- Validation outcome events, needed by Platform Core and Client/UI

### Out of Scope
- UI rendering and interaction design: `Client/UI`
- Lobby lifecycle ownership (create/join/leave orchestration): `Platform Core`
- End-to-end test harness ownership: `Quality + Testing`
- CI/CD pipeline ownership and release process: `Integration + Release`
- Database schema migration and production operations: `Platform Core + Integration + Release`

## 3. Validation Architecture Overview
The Rules + Validation design follows the same server-authoritative approach documented by Platform Core. Clients submit actions, backend validates all rule/security/state constraints, and only validated transitions mutate game state.

**Platform Core Interface Alignment (Pending):** Platform Core defines a `GameEngine` interface with methods `createInitialState()`, `validateMove()`, `applyMove()`, and `evaluateEnd()`, orchestrated by their `GameSessionManager`. The exact relationship between the Rules + Validation pipeline and the `GameEngine` interface needs to be finalized with Platform Core before Iteration 2 implementation begins. The validation stages, contracts, and error codes defined in this document are designed to be compatible with that interface regardless of the final integration pattern.

- Entry point(s): `make_move` over WebSocket (`/ws/game/{game_id}`) and optional endpoints for reconnect/resync workflows.
- Data sent to Rules + Validation: `playerId`, `authToken`, `sessionId`/`gameId`, `roomCode` (if applicable), `move` payload, `requestId`.
- Move payload (game-agnostic): `actionType`, action parameters, target selection/coordinates (if needed), and client timestamp.
- Validation stages: auth check, membership check, game status check, active-player check, rule legality check, conflict/version check.
- Success path: move accepted, state updated, turn advanced, update broadcast, state persisted.
- Failure path: move rejected, no state mutation, no turn advance, error event returned with code/message.
- Output contract: normalized `ValidationResult` object and standardized events (`move_accepted`, `move_rejected`, `turn_changed`, `game_over`, `error`).

## 4. Move Processing Flow
1. Receive move request
2. Authenticate/authorize player
3. Verify player membership in session
4. Verify game status allows move
5. Verify correct active player
6. Verify move legality against game rules
7. Apply or reject move
8. Emit update/error to platform core and clients

Notes:
- Idempotency/duplicate handling: duplicate move IDs are ignored; retries return prior outcome when possible.
- Ordering/version checks: server validates turn number/state version to prevent stale moves from mutating current state.

## 5. Rule Categories
- Turn-order rules: only current active player can submit a state-changing action.
- Legal-move rules: action must satisfy legal-transition rules for current game state.
- Game-finished rules: no new moves accepted once status is finished.
- Membership/authorization rules: only authenticated players assigned to session may act.
- Duplicate/late-message rules: stale/out-of-order actions are rejected with conflict errors.

## 6. Validation Interfaces and Contracts
### Request Contract
- `sessionId`: target game session identifier
- `playerId`: acting player identifier
- `authToken`: authentication token/session token
- `move`: action payload (game-agnostic envelope + game-specific body)
- `clientVersion` (optional): client-known state/turn version for conflict checks
- `requestId`: unique request identifier for duplicates

### Response Contract
- `isValid`: boolean decision
- `errorCode`: stable machine-readable code for failures
- `errorMessage`: user-facing or log-facing reason
- `updatedState`: server-approved state snapshot/delta (on success)
- `nextActivePlayerId`: next turn owner (on success)
- `serverVersion`: authoritative state version after processing
- `requestId`: echoed correlation identifier

### Events
- `move_accepted`
- `move_rejected`
- `turn_changed`
- `game_over`
- `error`

Note: These are the **validation outcome types** that the Rules + Validation pipeline produces. Platform Core (via EventBus/GameSessionManager) is responsible for actually broadcasting these events to connected clients over WebSocket. Rules + Validation returns a `ValidationResult` to Platform Core; Platform Core handles dispatch and notification.

## 7. Error codes
`NOT_YOUR_TURN`: Player attempted move out of turn, Show turn warning

`ILLEGAL_MOVE`: Move violates game rules, Show invalid-move reason

`GAME_FINISHED`: Move sent after game end, Lock input and refresh

`PLAYER_NOT_IN_SESSION`: Unauthorized session action, Rejoin/login flow

`STATE_CONFLICT`: Stale/duplicate/out-of-order action, Resync state

`UNAUTHENTICATED`: Missing/invalid auth token, Re-authenticate

`UNAUTHORIZED_ACTION`: Authenticated but not allowed for action, Block action and show permission error

`INVALID_PAYLOAD`: Event payload missing required fields, Correct payload and retry

Note:
- Client/UI displays friendly messages while keeping code available for automated tests and logs.

## 8. State Update Behavior
### On Valid Move
- State mutation behavior: backend applies move to authoritative state only after all checks pass.
- Turn advancement behavior: active player moves to next valid player only after successful apply.
- Broadcast behavior: updated state and turn change events sent to all participants in the session room.
- Persistence behavior: post-update state and move history are persisted for reconnect/recovery.

### On Invalid Move
- No-op behavior: no board/state mutation and no turn advancement.
- Error response behavior: `move_rejected`/`error` returned with code and reason.
- Retry/recovery behavior: player may submit a new valid action; stale clients must resync if `STATE_CONFLICT`.

## 9. Data Model Touchpoints
- Game status (aligned with Platform Core): `Created | WaitingForPlayers | ReadyToStart | Starting | TurnSelect | Ended | ReportingResults`. Move submissions are only accepted when the game is in the `TurnSelect` state. Moves sent during any other state are rejected with `GAME_FINISHED` (if `Ended`/`ReportingResults`) or an appropriate error for pre-game states.
- Active player: current turn owner ID
- Session membership: session participant list and roles
- Board/game payload: authoritative state snapshot used for rule evaluation
- Move history/version: request IDs, turn numbers, state versions for conflict/duplicate handling
- Auth context: token claims/session identity needed for authorization checks

## 10. Reliability and Security
### Reliability
- Reconnect handling: client reloads latest state via REST and rejoins WebSocket room.
- Duplicate/late message handling: reject or ignore stale/duplicate requests by `requestId` and `serverVersion`.
- Conflict protection strategy: strict server version checks before apply; state conflict returns explicit error.

### Security/Access
- Auth requirements: all state-changing actions require valid token/session.
- Authorization checks: only users in session can submit `make_move`; non-participants blocked.
- Spectator permissions (if used): read-only event subscription, no state-changing actions.

## 11. Cross-Team Integration
### Platform Core Integration
- Where core calls validation: before any move application and turn progression decision.
- What validation returns to core: normalized decision, error code/message, updated state and next player.
- Core dependencies: stable session identifiers, participant membership, game lifecycle status.

### Client/UI Integration
- Required UI states/messages: accepted move, rejected move reason, turn indicator, game-over state.
- Required events for turn/error/game-end: `move_accepted`, `move_rejected`, `turn_changed`, `game_over`, `error`.
- UI dependencies: consistent event schema and field names (`event`, `payload`, `timestamp`, `requestId`).

### Quality + Testing Integration
- Test cases they need from Rules + Validation: valid move, invalid move, not-your-turn, stale state, unauthorized action, finished-game move attempt.
- Mocks/fixtures/contracts provided: error codes, sample payloads, event contract examples.
- QA dependencies: agreed expected outcomes for each error code and state transition.

### Integration + Release Integration
- Contract stability requirements: validation contract for requests/responses/events.
- CI expectations for validation tests: automated unit/integration checks for acceptance/rejection paths.

## 12. Dependencies Map

### What We Need From Other Teams
#### From Platform Core
- API/service: authoritative session/game service entry point for validation invocation.
- Data model: active player, game status, participant membership, session metadata.
- Event routing: publish/subscribe path for accepted/rejected/turn/game-over events.

#### From Client/UI
- Screens/components: game room components that consume validation outcomes.
- Error display contract: mapping from error codes to UI messages.
- State management expectation: client treats server as source of truth and resyncs on conflict.

#### From Quality + Testing
- Test framework support: integration harness to execute validation scenarios end-to-end.
- Shared fixtures: reusable session/move payload fixtures for edge cases.
- Coverage expectations: agreed minimum validation-path coverage for key failure modes.

#### From Integration + Release
- CIDC pipeline: run validation test suite on merge requests.
- Branch/review rules: cross-team review changes.
- Doc/release standards: centralized API/event contract documentation location.

### What We Provide To Other Teams
#### To Platform Core
- Validation service interfaces: game-agnostic validation entry points and outcomes.
- Error/result contract: stable codes and decision envelope used for turn/state decisions.

#### To Client/UI
- User-facing validation/error codes: documented set of validation failures.
- Events: clear accepted/rejected/turn/game-over behavior for UI state handling.

#### To Quality + Testing
- Rule test ideas: list of validation scenarios and expected results.
- Edge-case scenarios: duplicate messages, stale versions, unauthorized actions, finished-game actions.

#### To Integration + Release
- Stable contract docs: maintained request/response/event specs.
- Validation test entry points: commands and fixtures for CIDC integration tests.

## 13. Milestones
### Iteration 1 (Design and Planning)
- I1-M1: Finalize Rules + Validation problem statement, ownership scope, and cross-team interfaces.
- I1-M2: Complete class diagram, use case package, and state machine aligned with Platform Core flow.
- I1-M3: Define validation error codes and contract draft (`request`, `result`, `events`).
- I1-M4: Complete planning document and presentation with dependencies, risks, and trade-offs.

### Iteration 2 (Implementation Progress)
- I2-M1: Implement baseline validation pipeline with auth, membership, turn, and legality checks.
- I2-M2: Integrate accepted/rejected event flow with Platform Core + Client/UI.
- I2-M3: Add conflict handling and reconnect behavior.
- I2-M4: Provide test ideas and examples to Quality + Testing and pass first integrated flows.

### Iteration 3 (Stability and Demonstration)
- I3-M1: edge-case handling and reduce integration bugs.
- I3-M2: Ensure validation behavior is stable across all demo game flows.
- I3-M3: Finalize documentation for contracts, errors, and integration behavior.
- I3-M4: Support final showcase with deterministic, test-backed validation outcomes.

## 14. High-Level Task Breakdown
`I1-01`: Draft/update Rules + Validation class diagram with interface points

`I1-02`: Draft 2-4 use cases and full descriptions (actors/preconditions/flow/postconditions/exceptions)

`I1-03`: Draft validation/move-processing state machine

`I1-04`: Define validation contracts + error taxonomy

`I1-05`: Write dependencies map, milestone plan, and risk section

`I1-06`: Finalize planning PDF + presentation material

`I2-01`: Implement baseline validation pipeline in backend service layer

`I2-02`: Integrate event flow with platform core and client

`I3-01`: Stabilize edge-case handling and finalize contract docs


## 15. Assumptions and Trade-Offs
- Assumption: Rules + Validation runs as server-authoritative logic in the FastAPI backend.
- Trade-off: improves fairness/consistency, but increases backend complexity and contract strictness.

- Assumption: Auth checks are part of validation ownership.
- Trade-off: stronger security control in one pipeline, but tighter dependency on auth/session data quality.

- Assumption: Design remains game-agnostic through shared interfaces with pluggable rule adapters.
- Trade-off: better reuse across games, but adapter design must be disciplined to avoid game-specific bugs.

- Assumption: Client submits actions only; server decides accepted state.
- Trade-off: prevents client-side desync and cheating, but requires a robust backend.

- Assumption: Conflict protection uses version/request identifiers.
- Trade-off: safer behavior, but adds complexity to request contracts and debugging.

- Assumption: Event schema stays standardized (`event`, `payload`, `timestamp`, `requestId`).
- Trade-off: easier integration/testing, but all teams must conform and coordinate schema updates.

## 16. Acceptance Criteria (Definition of Done)
- Validation rejects illegal actions consistently with stable error codes.
- Turn progression advances only after successful validation and apply.
- Auth and session-membership checks are enforced for state-changing actions.
- Duplicate/stale requests do not corrupt state and return deterministic outcomes.
- Cross-team contracts are documented and agreed by dependent teams.
- Iteration 1 deliverables are complete in required formats and aligned with Platform Core plan.

## 17. Use Case Descriptions

### UC-RV-01: Validate and Apply a Legal Move

| Field | Description |
|---|---|
| **Use Case ID** | UC-RV-01 |
| **Use Case Name** | Validate and Apply a Legal Move |
| **Actors** | Player, Platform Core (GameSessionManager), Rules + Validation Pipeline |
| **Description** | A player submits a move during their turn. The validation pipeline confirms the move is legal and applies it to the game state. |

**Preconditions:**
- The game session exists and is in the `TurnSelect` state.
- The player is authenticated with a valid token/session.
- The player is a registered participant in the game session.
- It is currently this player's turn (they are the active player).

**Main Success Flow:**
1. Player sends a `make_move` event over WebSocket with their move payload, `sessionId`, `playerId`, `authToken`, and `requestId`.
2. Pipeline authenticates the player using the provided `authToken`.
3. Pipeline verifies the player is a member of the specified session.
4. Pipeline checks that the game status is `TurnSelect` (game is active and accepting moves).
5. Pipeline confirms the player is the current active player for this session.
6. Pipeline evaluates the move payload against the game-specific rule adapter to confirm legality.
7. Pipeline checks `clientVersion`/`requestId` to confirm the move is not stale or duplicated.
8. Move passes all checks. Pipeline applies the move to the authoritative game state.
9. Pipeline evaluates end conditions (win/loss/draw). No end condition detected.
10. Pipeline advances the turn to the next valid active player.
11. Pipeline returns a `ValidationResult` to Platform Core with `isValid: true`, `updatedState`, `nextActivePlayerId`, and incremented `serverVersion`.
12. Platform Core broadcasts `move_accepted` and `turn_changed` events to all session participants.

**Postconditions:**
- The game state has been updated with the applied move.
- The turn has advanced to the next player.
- The move is recorded in the move history with its `requestId` and turn number.
- The updated state is persisted for reconnect/recovery.

**Exceptions:**
- None for this use case. All failure scenarios are covered by UC-RV-02.

---

### UC-RV-02: Reject an Invalid Move

| Field | Description |
|---|---|
| **Use Case ID** | UC-RV-02 |
| **Use Case Name** | Reject an Invalid Move |
| **Actors** | Player, Platform Core (GameSessionManager), Rules + Validation Pipeline |
| **Description** | A player submits a move that fails one or more validation checks. The pipeline rejects the move without modifying game state. |

**Preconditions:**
- The game session exists.
- The player sends a `make_move` event with a move payload.

**Main Success Flow:**
1. Player sends a `make_move` event over WebSocket with their move payload.
2. Pipeline begins the validation stage sequence (auth → membership → status → turn → legality → conflict).
3. One of the validation stages fails (see Alternative Flows below).
4. Pipeline halts further processing immediately upon the first failure.
5. Pipeline returns a `ValidationResult` to Platform Core with `isValid: false`, the appropriate `errorCode`, and a descriptive `errorMessage`.
6. Platform Core sends a `move_rejected` event back to the requesting player with the error code and message.

**Postconditions:**
- The game state is unchanged (no mutation occurred).
- The turn has not advanced; the same player remains active.
- The `serverVersion` is unchanged.
- The player may submit a corrected move.

**Alternative Flows (by validation stage):**

- **3a. Authentication fails:** Player's `authToken` is missing, expired, or invalid. Error code: `UNAUTHENTICATED`.
- **3b. Membership check fails:** Player is not a registered participant in this session. Error code: `PLAYER_NOT_IN_SESSION`.
- **3c. Game status check fails:** Game is in `Ended` or `ReportingResults` state. Error code: `GAME_FINISHED`. Game is in a pre-game state (`Created`, `WaitingForPlayers`, `ReadyToStart`, `Starting`). Error code: `UNAUTHORIZED_ACTION`.
- **3d. Active player check fails:** It is not this player's turn. Error code: `NOT_YOUR_TURN`.
- **3e. Rule legality check fails:** The move violates game-specific rules (e.g., invalid position, illegal piece movement). Error code: `ILLEGAL_MOVE`.
- **3f. Conflict/version check fails:** The `clientVersion` does not match the current `serverVersion`, or the `requestId` has already been processed. Error code: `STATE_CONFLICT`.
- **3g. Payload validation fails:** Required fields are missing or malformed in the move payload. Error code: `INVALID_PAYLOAD`.

---

### UC-RV-03: Detect Game Over After Move

| Field | Description |
|---|---|
| **Use Case ID** | UC-RV-03 |
| **Use Case Name** | Detect Game Over After Move |
| **Actors** | Player, Platform Core (GameSessionManager), Rules + Validation Pipeline |
| **Description** | After a valid move is applied, the pipeline's end-condition evaluation detects a win, loss, or draw, ending the game. |

**Preconditions:**
- The game session is in the `TurnSelect` state.
- The player is authenticated, is a session member, and it is their turn.
- The player submits a valid move that passes all validation checks.

**Main Success Flow:**
1. Player sends a `make_move` event with a valid move payload.
2. Pipeline runs all validation stages (auth, membership, status, turn, legality, conflict). All pass.
3. Pipeline applies the move to the authoritative game state.
4. Pipeline runs end-condition evaluation against the updated state using the game-specific rule adapter.
5. End condition is detected (win for a player, or draw/tie).
6. Pipeline sets the game status to `Ended`.
7. Pipeline returns a `ValidationResult` to Platform Core with `isValid: true`, `updatedState` reflecting the final board, a `gameOver` indicator with the result (winner ID or draw), and game status `Ended`.
8. Platform Core broadcasts `move_accepted` and `game_over` events to all session participants with the result.
9. Platform Core transitions the game to `ReportingResults` and records the outcome for stats/leaderboard.

**Postconditions:**
- The game state reflects the final move and the game status is `Ended`.
- No further moves are accepted for this session (subsequent attempts return `GAME_FINISHED`).
- The game result (winner/draw) is available for Platform Core to record in stats and leaderboards.
- The final state is persisted.

**Exceptions:**
- **5a. No end condition detected:** The game continues normally. Turn advances to the next player as described in UC-RV-01. This is the standard case, not an error.

## 18. Risks and Mitigations

- **Risk:** Platform Core changes their API, event schema, or `GameEngine` interface during implementation.
  - Mitigation: Establish versioned contracts early. Hold regular sync meetings with Platform Core. Perform early integration testing in Iteration 2 to catch mismatches before they compound.

- **Risk:** Game-specific rules are harder to abstract into a game-agnostic adapter pattern than expected.
  - Mitigation: Validate the adapter design with the simplest game first (Tic-Tac-Toe) before applying it to more complex games (Connect Four, Checkers). Keep the adapter interface minimal.

- **Risk:** Validation pipeline does not integrate cleanly with Platform Core's `GameSessionManager` orchestration flow.
  - Mitigation: Align on the interface contract with Platform Core before implementation starts in Iteration 2. Document the expected call sequence and return types. The pending `GameEngine` interface alignment (see Section 3) must be resolved first.

- **Risk:** Auth and session data provided by other teams is inconsistent or incomplete, causing false validation failures.
  - Mitigation: Implement defensive validation with clear, specific error codes so issues are traceable. Do not assume clean input from upstream. Log validation stage failures for debugging.

- **Risk:** Scope creep into Platform Core's territory (e.g., lobby validation, matchmaking checks, session lifecycle management).
  - Mitigation: Strict scope boundaries as documented in Section 2. If a validation concern arises that falls outside R+V ownership, document it and escalate to Platform Core rather than absorbing it.