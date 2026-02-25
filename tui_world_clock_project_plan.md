# TUI World Clock -- Project Plan

## Overview

This project is a terminal-based multi-timezone clock application built
in Python using `rich` for rendering. The application will provide a
searchable timezone picker, multi-timezone display, persistent
configuration, and 12h/24h toggle support.

After stabilizing the `rich` version, the application can later be
rebuilt using `textual` for a more advanced TUI architecture.

------------------------------------------------------------------------

# Phase 1: Rich-Based Implementation

## 1. Technical Stack

-   Python 3.10+
-   rich (UI rendering)
-   zoneinfo (built-in timezone handling)
-   json (config persistence)
-   pathlib (filesystem handling)
-   threading or asyncio (optional for clean refresh loop)

------------------------------------------------------------------------

## 2. Core Features

### 2.1 Multi-Timezone Support

-   Display multiple clocks simultaneously.
-   Each clock row contains:
    -   Label (editable)
    -   IANA timezone name
    -   Current time
    -   UTC offset
-   Highlight selected clock.
-   Support add/remove operations.

### 2.2 Searchable Timezone Picker

-   Load available timezones from `zoneinfo.available_timezones()`
-   Allow incremental search:
    -   Typing filters list in real-time
    -   Arrow keys navigate results
    -   Enter selects timezone
-   Accept flexible matching:
    -   Partial match (e.g., "Kolkata" → Asia/Kolkata)
    -   Case insensitive

### 2.3 Persistent Config File

Location:

    ~/.config/tui-world-clock/config.json

Structure:

``` json
{
  "format_24h": true,
  "timezones": [
    {
      "label": "India",
      "zone": "Asia/Kolkata"
    },
    {
      "label": "London",
      "zone": "Europe/London"
    }
  ]
}
```

Auto-create config file on first run. Save on: - Add - Remove - Toggle
format - Rename

### 2.4 12h / 24h Toggle

-   Default: 24h
-   Press `t` to toggle
-   Persist preference in config file
-   Format logic:
    -   24h → `%H:%M:%S`
    -   12h → `%I:%M:%S %p`

------------------------------------------------------------------------

## 3. UI Layout Design

### Header

-   Title: "TUI World Clock"
-   Current mode (12h/24h)
-   Help hint line

### Clock Table

Columns: - Label - Time - UTC Offset - Timezone Name (dimmed)

Example layout:

  -------------------------------------------
          TUI World Clock \| 24h Mode
  -------------------------------------------
     India 19:42:11 UTC+05:30 Asia/Kolkata
  London 14:12:11 UTC+00:00 Europe/London New
   York 09:12:11 UTC-05:00 America/New_York

  -------------------------------------------

## (a)add (d)delete (t)toggle (q)quit

------------------------------------------------------------------------

## 4. Interaction Model

Keybindings:

  Key   Action
  ----- -----------------
  a     Add timezone
  d     Delete selected
  r     Rename label
  t     Toggle 12h/24h
  ↑ ↓   Navigate clocks
  /     Search timezone
  q     Quit

------------------------------------------------------------------------

## 5. Clean Refresh Loop

-   Refresh every 1 second.
-   Avoid full terminal clear where possible.
-   Use `rich.Live()` context manager.
-   Re-render only dynamic time content.
-   Gracefully handle terminal resize.

Example architecture:

Main Loop: 1. Load config 2. Initialize Live render 3. While running: -
Read non-blocking input - Update state - Render table - Sleep 1 second

------------------------------------------------------------------------

## 6. Project Structure

    tui_world_clock/
    ├── app.py
    ├── ui.py
    ├── timezone_manager.py
    ├── config_manager.py
    ├── models.py
    └── utils.py

### Responsibilities

-   app.py → entry point, event loop
-   ui.py → render functions
-   timezone_manager.py → zoneinfo logic
-   config_manager.py → load/save config
-   models.py → Clock model
-   utils.py → formatting helpers

------------------------------------------------------------------------

## 7. Edge Cases

-   Invalid timezone
-   DST transitions
-   Duplicate entries
-   Empty config file
-   Corrupt config file
-   Terminal resize
-   Rapid keypress handling

------------------------------------------------------------------------

# Phase 2: Refactor to Textual

After stabilizing Phase 1:

## Goals

-   Proper component-based architecture
-   Dedicated screens (Main view / Search modal)
-   Scrollable list widgets
-   Reactive state model
-   Cleaner keyboard handling
-   Better layout control

## Improvements Over Rich

-   Structured layout system
-   Event-driven UI
-   Built-in focus handling
-   Built-in scroll containers
-   Modal dialogs for search

## Migration Strategy

1.  Keep core logic (timezone + config) unchanged.
2.  Replace ui.py entirely.
3.  Implement App subclass in textual.
4.  Convert main loop into reactive state updates.

------------------------------------------------------------------------

# Future Enhancements

-   Alarm system
-   Countdown timers
-   Time difference calculator
-   Sunrise/sunset (astral)
-   Theme support (dark/light)
-   Export ISO timestamp
-   Multiple layout modes (compact / detailed)
-   Fullscreen digital clock mode

------------------------------------------------------------------------

# Milestones

Phase 1 \[ \] Basic rendering \[ \] Multi-timezone support \[ \] Search
picker \[ \] Persistence \[ \] Toggle format \[ \] Stable refresh loop

Phase 2 \[ \] Textual refactor \[ \] Modal search UI \[ \] Component
separation \[ \] Improved UX polish

------------------------------------------------------------------------

# Final Goal

A stable, keyboard-driven, minimal, high-clarity world clock tool
optimized for Linux terminal workflows.
