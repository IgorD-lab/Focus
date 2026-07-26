# Study App — Functional Scoping Plan

## Context

Igor wants a study app. The stated ingredients were a pomodoro timer, a video player (YouTube or
local), and Obsidian-integrated notes across 3 monitors. But the conversation surfaced that those
are symptoms, not the problem. Two real problems came out:

1. **Startup friction.** Every time he switches what he's learning, he has to manually open,
   arrange, close and reopen the same constellation of apps. That cost is paid at exactly the
   moment motivation is lowest, so studying doesn't start. *(Same failure economics as the Vault
   project: willpower-funded decisions at the worst moment.)*
2. **State drift.** He forgets to pause, runs into overtime to protect flow, takes a break and
   never comes back. The timer stops reflecting reality, so it stops being useful.

The design north star, identical to the Vault project's: **the tooling enforces the state, not the
willpower.** Here that means the *window layout itself* is the mode — work mode is everything
fullscreen, break mode is everything un-fullscreened and minimized — and the timer's state
transitions are driven by what he clicks (and, crucially, by what he *doesn't* click).

This plan produces a **functional specification** — the first document of his AWOS flow
(functional spec → technical spec → tasks → incremental implementation). It is deliberately
stack-free, matching `~/Desktop/FileSystemOverhaul/functional-spec.md`.

---

## Deliverables

| Path | What |
|---|---|
| `~/Desktop/Study/` | New project folder (the "study folder" requested) |
| `~/Desktop/Study/functional-spec.md` | The main deliverable — full functional spec, ~500 lines |
| `~/.claude/projects/-home-igord-Desktop/memory/study-app.md` | Project memory (type: `project`), linked to `[[igor-profile]]` and `[[file-org-overhaul]]` |
| `~/.claude/projects/-home-igord-Desktop/memory/MEMORY.md` | One-line index pointer appended |

**Not in this plan:** technical spec, task breakdown, any code. Those are the next steps after the
functional spec is reviewed.

**Working name:** `nixie` (short, CLI-friendly, names the aesthetic, sits alongside his existing
`vault` CLI). Alternatives to consider in the spec: `labmem`, `meter`, `tube`. Trivially renamed.

---

## Locked-in design decisions

These came out of the Q&A and must be captured verbatim in the spec — they are the actual design.

### 1. The timer: absence of a click is the signal

The novel mechanic, and Igor's own design. Nothing ever interrupts flow, because continuing to work
requires no action.

```
WORK (preset, e.g. 25m)
  ├─ at ~15% remaining ── soft chime + non-blocking corner toast
  │                       (percentage-based, NOT fixed 5m — 5m on a 25m block is annoying)
  ├─ at 0:00 ─────────── soft chime + toast:  [ Start Break ]  [+5] [+10] [+25]
  └─ NO CLICK ─────────► WORK_OVERTIME  (silent, fullscreen stays, credit accrues)

WORK_OVERTIME
  ├─ elapsed hits 2× block (e.g. 50m on a 25m preset) ──► offer:
  │     "Switch to 50/10 for the rest of the session?"
  │       accept  → preset changes for remaining session, credit ZEROED (no double-dip)
  │       ignore  → credit keeps accruing
  └─ [ Start Break ] ──► BREAK with duration = preset_break + credit
                          (credit is spent on ONE break, then zeroed:
                           15m overtime turns a 5m break into a 20m break)

BREAK
  ├─ warning chime near end (percentage-based)
  ├─ at 0:00 ── chime + toast: [ Start Work ]
  └─ NO CLICK ─────────► BREAK_OVERTIME

BREAK_OVERTIME
  ├─ burns remaining credit first (credit ticks DOWN, visibly)
  ├─ credit exhausted ──► RED TIME accrues (tracked for reflection, not punishment)
  └─ red time ≥ 10m ───► SESSION_OVER

SESSION_OVER
  └─ end screen with metrics. Closes NOTHING (unsaved work is sacred).
     Exits fullscreen, releases the desktop.
```

**Credit rules:** earned only from work overtime · spendable on exactly one break, or absorbed by
break overtime · **expires at session end, never carries over** · forfeited if the longer-block
offer is accepted.

### 2. Layout modes — the friction killer

One action puts him *in* the workspace. Monitor roles, using real hardware names found on disk:

| Mode | `DP-1` ASUS 1440p (center) | `HDMI-A-1` (left) | `DP-2` (right) |
|---|---|---|---|
| **`applied`** (coding, Arduino) | primary app — VS Code / Arduino IDE | video tutorial | Obsidian notes |
| **`tutorial`** (default, pure watching) | video tutorial | terminal / browser / reference | Obsidian notes |

- A **keybind rotates the roles** so he can promote the video or the editor to center mid-session.
- **Work mode** = fullscreen all three. **Break mode** = un-fullscreen + minimize, desktop freed.
- **Global summon keybind** brings the control panel up *over* fullscreen for on-the-fly changes —
  implemented as a **pyprland scratchpad**, which he already has configured and running.

### 3. Storage — all four choices confirmed, all plain files

| Thing | Where | Format |
|---|---|---|
| Workspace profiles | `~/Desktop/Study/profiles/<subject>.toml` | hand-editable TOML (apps, monitor roles, timer preset, video, note path) |
| Session note | `<Obsidian vault>/Study/<subject>/<YYYY-MM-DD>.md` | created from template, opened via `obsidian://` URI |
| Session metrics | appended into that same note | frontmatter + footer — blocks, extensions, credit, red time, materials touched |
| Material vault | `<Obsidian vault>/Study/_inbox/*.md` | markdown + frontmatter: `url`, `subject`, `priority`, `status`, `added`, `est_duration` |

**Material vault behaviour:** fire-and-forget. One keybind → paste a YouTube link → pick subject +
priority → done, zero further thought. When he later picks that subject, the app surfaces a
priority-ordered "next up" queue. Lives inside the Obsidian vault so it stays fully browsable and
editable even if the app is broken or abandoned — same durability principle as the Vault project.

**Timer library:** presets (`25/5`, `50/10`, `60/10`, `90/20`, `120/40`) each optionally bound to a
YouTube "study with me" video that matches the cycle. The app's timer stays authoritative; the
video is ambience/visual, not the source of truth.

### 4. Aesthetic — Steins;Gate / Y2K / nixie lab

Confirmed direction, replacing the four generic options offered. Concretely, for the spec's design
brief section:

- **Nixie-tube numerals** as the primary timer display — amber-orange neon glow, visible wire mesh,
  ghost digits idling behind the lit one. The end-of-session screen is a divergence-meter-style
  readout, not a "hooray".
- **Y2K Japanese lab equipment** chrome: worn beige/rust panels, hairline warning stripes, tape
  labels, small katakana/romaji annotations, chunky physical-looking toggles.
- **CRT surface**: subtle scanlines, slight bloom, barrel curvature at edges, boot-sequence
  transitions between modes.
- **Palette**: near-black + amber/orange primary + one cold cyan for secondary readouts. No bright
  fills, no emoji, no rounded friendly shapes, no celebration confetti.
- Original work in that *idiom* — no lifted Steins;Gate assets, names, or trademarks.

---

## Difficulty assessment (the question actually asked)

| Piece | Difficulty | Why |
|---|---|---|
| Multi-monitor window orchestration | **Easy** | `hyprctl dispatch` + window rules. Sounds like the hard part; is the easiest part, because Hyprland is fully scriptable. |
| Summon-over-fullscreen panel | **Easy** | pyprland scratchpad — already installed and configured on his machine. |
| Work/break fullscreen toggling | **Easy** | Same `hyprctl` mechanism. |
| Timer state machine + credit | **Easy–Medium** | A few hundred lines. The *design* was the hard part and it's now settled. |
| Obsidian integration | **Easy** | Write markdown, open via `obsidian://open?vault=…&file=…`. No plugin required. |
| Material vault | **Easy** | Markdown + frontmatter; same shape as the Vault project's rules files. |
| Video playback | **Easy–Medium** | `mpv` + `yt-dlp` is the light path — important given weak hardware. Browser YouTube is the heavy fallback. |
| **Nixie/CRT UI** | **Medium** | This is where the real hours go. Everything else is plumbing. |

**Verdict:** a crude but genuinely usable v1 is a weekend. The polished version is a couple of weeks
of evenings, and nearly all of that is UI craft and behavioural tuning of the timer — **there are no
technical unknowns and nothing here requires a heavy Electron-class app.** The multi-monitor
requirement, which sounded like the risk, is the cheapest part because of Hyprland.

---

## Functional spec outline

Mirroring the structure of `~/Desktop/FileSystemOverhaul/functional-spec.md`:

1. **Problem statement** — startup friction + state drift; why previous attempts (raw pomodoro apps)
   failed; the "tooling enforces state, not willpower" north star
2. **Current state** — how a study session starts today, manual step by manual step, with the real
   monitor/app inventory found on disk
3. **Design principles** — flow is never interrupted · no punishment mechanics · files over
   databases · nothing is ever auto-closed · MVP-first, upgradeable
4. **Core concepts** — Session · Block · Subject Profile · Layout Mode · Credit · Red Time · Material
5. **The timer state machine** — the diagram above, fully specified with every transition and edge case
6. **Layout modes & monitor roles** — the table above, plus role rotation and work/break transitions
7. **Subject profiles** — what a profile declares, example TOML, how a new subject is created
8. **Material vault** — capture flow, priority model, surfacing rules
9. **Notes & Obsidian integration** — template, path convention, metrics write-back
10. **Timer library & study videos** — presets and video binding
11. **Design brief** — the nixie/Y2K/CRT direction above, screen by screen (control panel, work
    overlay, break screen, end-of-session readout)
12. **Out of scope for v1** — app blocking/denylists, activity surveillance, VS Code extension,
    cross-device sync, mobile
13. **Open decisions** — final name; exact chime sounds; whether the thesis vault
    (`~/Desktop/Diplomski`) gets its own profile; percentage for the pre-warning chime

---

## Verification

The functional spec is stack-free, so verification is review-based, not executable:

1. **Read it end to end** and confirm the timer state machine matches the mechanic Igor described —
   especially that *not clicking* is always the flow-preserving choice in work, and always the
   costly one in break.
2. **Trace three concrete scenarios** through the spec and confirm each is unambiguous:
   - "Python asyncio tutorial, pure watching, 25/5, finish on time"
   - "Arduino coding, 25/5, hit flow, run 30 min over, decline the 50/10 offer, cash the credit into
     one long break"
   - "5-minute break, go cook, come back 40 minutes later" → credit burns, red time accrues, session
     auto-concludes without closing anything
3. **Sanity-check the environment claims** against the machine — monitor names/positions, pyprland
   scratchpad availability, Obsidian vault paths — all confirmed present during planning.
4. **Then**: technical spec → `tasks.md` (AWOS vertical slices) → implement slice 1, exactly as the
   Vault project ran.

---

## Environment facts confirmed on disk (2026-07-26)

| Thing | Value |
|---|---|
| Center monitor | `DP-1` — ASUSTek XG27ACS, 2560x1440@180, scale 1.25, at `0x0` |
| Left monitor | `HDMI-A-1` — Dell SE2717H, 1920x1080@75, at `-1920x0` |
| Right monitor | `DP-2` — Dell U2312HM, 1920x1080@60, at `2048x0` |
| Compositor | Hyprland (HyDE config) with **pyprland + `scratchpads` plugin already enabled** |
| Obsidian | native binary at `/usr/bin/obsidian`; vaults at `~/Documents/Obsidian Vault/` and `~/Desktop/Diplomski/` |
