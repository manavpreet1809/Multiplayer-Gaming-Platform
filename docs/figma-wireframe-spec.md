# Figma Wireframe Spec — OMG Platform UI Components

Use this document as a reference when building wireframes in the [Design Guide](https://www.figma.com/design/KAps47asfJObGfMwfNiw1e/Chalant-Auramaxxers-Design-Guide?node-id=0-1&t=G9A39dURMMiFEj8H-1).

---

## Global Design Tokens

### Color Palette

| Name                 | Hex       | Usage                                                      |
| -------------------- | --------- | ---------------------------------------------------------- |
| Purple (Primary)     | `#662691` | Buttons, links, headings, active states, board grid lines  |
| Lavender (Secondary) | `#BEB8EB` | Borders, dividers, secondary surfaces, table headers       |
| Coral (Danger)       | `#F56476` | Errors, logout, loss states, O marks                       |
| Mint (Success)       | `#ADFCF9` | Success banners, ready status, win states, winning cells   |
| Yellow (Warning)     | `#F8F4A6` | Notifications, queue status, selected squares, draw states |

**Derived tints:**

| Name         | Hex       | Derived From | Usage                             |
| ------------ | --------- | ------------ | --------------------------------- |
| Dark Purple  | `#4e1d6e` | Purple       | Hover states                      |
| Light Purple | `#ebe8f5` | Purple       | Hover backgrounds, light surfaces |
| Light Coral  | `#fde2e5` | Coral        | Error backgrounds                 |
| Dark Mint    | `#0a7a6f` | Mint         | Success text                      |
| Dark Yellow  | `#7a6f00` | Yellow       | Warning text                      |

### Typography

- **Font Family:** Roboto (Google Fonts)
- **Weights:** 300 (Light), 400 (Regular), 500 (Medium), 700 (Bold)

| Element            | Size            | Weight |
| ------------------ | --------------- | ------ |
| Page title (h1)    | 1.75rem (28px)  | 700    |
| Section title (h2) | 1.5rem (24px)   | 700    |
| Subsection (h3)    | 1.125rem (18px) | 600    |
| Body text          | 1rem (16px)     | 400    |
| Labels             | 0.875rem (14px) | 600    |
| Small / Captions   | 0.75rem (12px)  | 500    |

### Spacing & Layout

- **Border radius (cards/forms):** 8px
- **Border radius (buttons):** 4px
- **Border radius (badges/pills):** 12px
- **Card padding:** 2rem (32px)
- **Form max-width:** 400px
- **Page max-width:** 900px (dashboard views), 700px (profile/leaderboard)
- **Grid gap:** 1rem (16px)
- **Box shadow (cards):** `0 2px 8px rgba(0, 0, 0, 0.1)`

### Button Styles

| Variant   | Background  | Text      | Border        | Hover BG      |
| --------- | ----------- | --------- | ------------- | ------------- |
| Primary   | `#662691`   | White     | None          | `#4e1d6e`     |
| Outline   | White       | `#662691` | 1px `#662691` | `#ebe8f5`     |
| Secondary | White       | `#662691` | 1px `#BEB8EB` | `#ebe8f5`     |
| Danger    | White       | `#F56476` | 1px `#F56476` | `#fde2e5`     |
| Link      | Transparent | `#662691` | None          | — (underline) |

---

## Screens & Components

### Screen 1: Login (AUTH-02 / UC-03)

**Layout:** Centered card on `#f5f5f5` background, full viewport height

```
┌─────────────────────────────────┐
│          [f5f5f5 bg]            │
│                                 │
│    ┌───────────────────────┐    │
│    │      Log In (h2)      │    │
│    │                       │    │
│    │  [Error alert bar]    │    │
│    │                       │    │
│    │  Username or Email    │    │
│    │  ┌─────────────────┐  │    │
│    │  │ text input      │  │    │
│    │  └─────────────────┘  │    │
│    │  Password             │    │
│    │  ┌─────────────────┐  │    │
│    │  │ password input  │  │    │
│    │  └─────────────────┘  │    │
│    │  ┌─────────────────┐  │    │
│    │  │    LOG IN btn   │  │    │
│    │  └─────────────────┘  │    │
│    │                       │    │
│    │  Forgot password?     │    │
│    │       Create account  │    │
│    └───────────────────────┘    │
│           400px wide            │
└─────────────────────────────────┘
```

**Elements:**

- Card: white, 8px radius, shadow, 2rem padding, 400px max-width
- Title: "Log In", 1.5rem, 700 weight, `#333`, centered
- Error bar: `#fde2e5` bg, `#F56476` text, 4px radius, 0.875rem
- Labels: 0.875rem, 600 weight, `#555`
- Inputs: full width, 1px `#ccc` border, 4px radius, focus → `#662691` border + purple shadow
- Button: Primary style, full width, 0.75rem padding
- Links: `#662691`, underline, 0.875rem, flex row space-between

---

### Screen 2: Register (AUTH-01 / UC-02)

**Layout:** Same centered card pattern as Login

```
┌───────────────────────┐
│   Create Account (h2) │
│                       │
│   [Error alert bar]   │
│                       │
│   Username            │
│   [text input]        │
│   Email               │
│   [email input]       │
│   Password            │
│   [password input]    │
│   Confirm Password    │
│   [password input]    │
│                       │
│   [CREATE ACCOUNT btn]│
│                       │
│   Already have an     │
│   account? Log in     │
└───────────────────────┘
```

**Same styles as Login.** Additional validations: min 6 chars password, password match.

---

### Screen 3: Reset Password (AUTH-03)

**Layout:** Same centered card, two-step flow

**Step 1 — Identify:**

```
┌───────────────────────┐
│  Reset Password (h2)  │
│                       │
│  Username or Email    │
│  [text input]         │
│                       │
│  [CONTINUE btn]       │
│                       │
│  Back to Log In       │
└───────────────────────┘
```

**Step 2 — New Password:**

```
┌───────────────────────┐
│  Reset Password (h2)  │
│                       │
│  Resetting for: user  │
│                       │
│  New Password         │
│  [password input]     │
│  Confirm New Password │
│  [password input]     │
│                       │
│  [RESET PASSWORD btn] │
│                       │
│  Back to Log In       │
└───────────────────────┘
```

**Success state:** "Password has been reset" message with a "Back to Log In" button.

---

### Screen 4: Dashboard (UC-04)

**Layout:** 900px max-width centered container

```
┌─────────────────────────────────────────────────────────────┐
│  Dashboard (h1)    player1  [idle]   [Profile][Leaderboard][Log Out]
│  ──────────────────────────────────────────────────────────
│
│  ┌─ Notification Banner (yellow, if any) ──────────────────┐
│  │  Notifications:  • Game invite from player2             │
│  └─────────────────────────────────────────────────────────┘
│
│  ┌─ Status Banner (conditional) ───────────────────────────┐
│  │  "A game is ready for you!"           [JOIN GAME btn]   │  ← mint bg, game-ready
│  │  "You are in the matchmaking queue…"                    │  ← yellow bg, in-queue
│  │  "You are in a game lobby."                             │  ← light purple bg, in-lobby
│  └─────────────────────────────────────────────────────────┘
│
│  What would you like to do? (h2)
│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │  Browse   │  │  Create  │  │   Join   │  │   Find   │  │   Open   │
│  │  Games    │  │  Game    │  │   Game   │  │  Match   │  │   Chat   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
│     180px min, auto-fill grid, 1rem gap, secondary button style
└─────────────────────────────────────────────────────────────┘
```

**Elements:**

- Header: flex row, title + user info + nav buttons
- Status badge: pill (12px radius), bg color per status
- Nav buttons: outline style, `#BEB8EB` border; Log Out uses danger style
- Notification section: `#F8F4A6` bg, 8px radius
- Action grid: `grid-template-columns: repeat(auto-fill, minmax(180px, 1fr))`
- Action cards: white bg, 1px `#BEB8EB` border, 8px radius, hover → purple border + shadow

---

### Screen 5: Game List (UC-01)

**Layout:** 900px max-width

```
┌────────────────────────────────────────────────────┐
│  Browse Games (h2)                         [Back]  │
│                                                    │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  Chess        │  │  Tic-Tac-Toe │               │
│  │  Classic game │  │  Classic 3x3 │               │
│  │  42 online    │  │  18 online   │               │
│  └──────────────┘  └──────────────┘                │
│     240px min cards, grid layout                   │
│                                                    │
│  ┌─ Detail Panel (selected game) ──────────────────┐
│  │  Chess                                          │
│  │  Classic chess game...                          │
│  │  42 players online                              │
│  │  [JOIN LOBBY btn]                               │
│  └─────────────────────────────────────────────────┘
│     light purple bg, lavender border               │
└────────────────────────────────────────────────────┘
```

---

### Screen 6: Game Lobby (UC-05)

**Layout:** 900px max-width

```
┌────────────────────────────────────────────────────┐
│  Chess Lobby (h2)          [Waiting...]  [Leave]   │
│  Lobby ID: abc123                                  │
│  ──────────────────────────────────────────────────│
│                                                    │
│  Players (1/2) (h3)                                │
│  ┌────────────────────────────────────────────┐    │
│  │  player1                        Ready ✓    │    │
│  ├────────────────────────────────────────────┤    │
│  │  Waiting for player…  (dashed, italic)     │    │
│  └────────────────────────────────────────────┘    │
│                                                    │
│  [Toggle Ready]  [Start Game]                      │
│                                                    │
│  ─────────────── Chat ────────────────             │
│  ┌───────────────────────────────────┐             │
│  │  (embedded Chat component)        │             │
│  └───────────────────────────────────┘             │
└────────────────────────────────────────────────────┘
```

**Elements:**

- Status pill: yellow bg for "Waiting", mint bg for "Started"
- Leave button: danger outline
- Player rows: lavender borders, 4px radius
- Empty slots: dashed border, italic gray text
- Ready/Start buttons: outline / primary purple

---

### Screen 7: Chat (UC-07)

**Layout:** 350px tall flex column (embeddable)

```
┌─────────────────────────────────────┐
│  Lobby Chat (h3, purple)            │
│  ┌─────────────────────────────────┐│
│  │  player1: Hello!        12:00  ││
│  │  player2: Ready?        12:01  ││
│  │                                 ││
│  │  (scrollable, lavender border)  ││
│  └─────────────────────────────────┘│
│  ┌──────────────────────┐ ┌──────┐ │
│  │ Type a message…       │ │ Send │ │
│  └──────────────────────┘ └──────┘ │
└─────────────────────────────────────┘
```

- Sender names: 600 weight, `#662691`
- Timestamps: 0.7rem, `#bbb`, right-aligned
- Send button: primary purple

---

### Screen 8: Profile (UC-09)

**Layout:** 700px max-width

```
┌──────────────────────────────────────────────┐
│  Player Profile (h2)          [Back to Dash] │
│                                              │
│  ┌──────────────────────────────────┐        │
│  │  Username          player1      │        │
│  │  ─────────────────────────────  │        │
│  │  Email       player1@email.com  │        │
│  └──────────────────────────────────┘        │
│                                              │
│  Overall Stats (h3)                          │
│  ┌────┐  ┌────┐  ┌────┐  ┌────┐             │
│  │ 10 │  │  6 │  │  3 │  │  1 │             │
│  │Plyd│  │Wins│  │Loss│  │Ties│             │
│  └────┘  └────┘  └────┘  └────┘             │
│   purple text, lavender border cards         │
│                                              │
│  Per-Game Stats (h3)                         │
│  ┌────────┬──────┬───┬───┬──────┬─────┐     │
│  │ Game   │Played│ W │ L │ Rank │ MMR │     │
│  ├────────┼──────┼───┼───┼──────┼─────┤     │
│  │ Chess  │  7   │ 4 │ 3 │Silver│1200 │     │
│  │ T-T-T  │  3   │ 2 │ 0 │ Gold │1400 │     │
│  └────────┴──────┴───┴───┴──────┴─────┘     │
│   header: light purple bg, purple text       │
│                                              │
│  [Edit Account Settings btn]                 │
└──────────────────────────────────────────────┘
```

---

### Screen 9: Leaderboard (UC-12)

**Layout:** 700px max-width

```
┌──────────────────────────────────────────────┐
│  Leaderboard (h2)             [Back to Dash] │
│                                              │
│  [Chess] [Tic-Tac-Toe] [Overall]  ← tabs    │
│   active tab: purple bg + white text         │
│   inactive: white bg, lavender border        │
│                                              │
│  ┌───┬──────────┬──────┬─────┬─────┐        │
│  │ # │ Player   │ Rank │ MMR │ W/L │        │
│  ├───┼──────────┼──────┼─────┼─────┤        │
│  │ 1 │ master   │ Gold │1800 │50/10│        │
│  │ 2 │ player1  │Silver│1200 │30/20│  ← mint bg (current user)
│  │ 3 │ newbie   │Bronze│ 900 │10/15│        │
│  └───┴──────────┴──────┴─────┴─────┘        │
│                                              │
│  "Play more games to appear..."  (if unranked)
└──────────────────────────────────────────────┘
```

---

### Screen 10: Game Results (UC-14)

**Layout:** 500px max-width, centered

```
┌──────────────────────────────────┐
│                                  │
│  ┌────────────────────────────┐  │
│  │        Victory!            │  │  ← mint bg for win
│  │     Winner: player1        │  │     coral bg for loss
│  └────────────────────────────┘  │     yellow bg for draw
│                                  │
│      MMR Change     New Rank     │
│        +25            Gold       │
│   (green/mint)     (default)     │
│                                  │
│  [Return to Dashboard]          │
│  [Play Again]  [View Leaderboard]│
└──────────────────────────────────┘
```

---

### Screen 11: Tic-Tac-Toe Board (UC-13 UI)

**Layout:** Centered, 300x300px board

```
┌──────────────────────────────────┐
│   You (X)    vs    Opponent (O)  │
│           Your turn              │
│                                  │
│   ┌─────┬─────┬─────┐           │
│   │  X  │     │  O  │           │
│   ├─────┼─────┼─────┤           │  4px purple grid lines
│   │     │  X  │     │           │
│   ├─────┼─────┼─────┤           │
│   │     │     │  O  │           │
│   └─────┴─────┴─────┘           │
│         300 x 300px              │
└──────────────────────────────────┘
```

**Board tokens:**

- Grid lines: `#662691` (4px gap)
- Cells: white bg, hover → `#ebe8f5`
- X marks: `#662691`, 3rem, 700 weight
- O marks: `#F56476`, 3rem, 700 weight
- Winning cells: `#ADFCF9` bg
- Active player indicator: `#ebe8f5` bg pill

---

### Screen 12: Chess Board (UC-13 UI)

**Layout:** Centered, 480x480px board (8x8 grid of 60px squares)

```
┌──────────────────────────────────────┐
│   You (white)   vs   Opponent (black)│
│              Your turn               │
│                                      │
│  Captured: ♟♟                        │
│                                      │
│   a  b  c  d  e  f  g  h            │
│  ┌──┬──┬──┬──┬──┬──┬──┬──┐          │
│ 8│♜ │♞ │♝ │♛ │♚ │♝ │♞ │♜ │         │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤          │
│ 7│♟ │♟ │♟ │♟ │♟ │♟ │♟ │♟ │         │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤          │
│  │  │  │  │  │  │  │  │  │  ...     │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤          │
│ 2│♙ │♙ │♙ │♙ │♙ │♙ │♙ │♙ │         │
│  ├──┼──┼──┼──┼──┼──┼──┼──┤          │
│ 1│♖ │♘ │♗ │♕ │♔ │♗ │♘ │♖ │         │
│  └──┴──┴──┴──┴──┴──┴──┴──┘          │
│                                      │
│  Captured: ♟                         │
└──────────────────────────────────────┘
```

**Board tokens:**

- Light squares: `#ebe8f5`
- Dark squares: `#BEB8EB`
- Board border: 2px `#662691`
- Selected square: `#F8F4A6` bg
- Last move: `rgba(248, 244, 166, 0.5)` bg
- Move indicator dots: `rgba(102, 38, 145, 0.3)`, 16px circle
- Capture rings: `rgba(102, 38, 145, 0.3)`, 54px circle, 4px border
- Pieces: Unicode glyphs, 2.5rem
- File/rank labels: 0.75rem, 500 weight, `#999`
- Responsive: 44px squares on screens < 600px

---

## Figma Setup Checklist

1. **Create color styles** for all 5 palette colors + derived tints
2. **Create text styles** for each typography tier (h1–caption)
3. **Create component variants** for buttons (primary, outline, secondary, danger, link)
4. **Create input component** with default, focus, disabled, and error states
5. **Build each screen** as a separate Figma frame (use 1440px desktop width)
6. **Add auto-layout** to match the CSS flex/grid patterns described above
7. **Use the component instances** across screens for consistency
