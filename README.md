# TimeSeal

TimeSeal is a local-first temporal journaling application designed to preserve thought history as immutable checkpoints.

Instead of organizing notes strictly by day, TimeSeal allows users to create intentional “seals” — snapshots of their thinking at meaningful moments in time.

Each seal becomes a permanent, read-only record that can only be extended through reflections.

---

## Philosophy

> Time moves forward. Thoughts evolve. The past remains preserved.

- Thought history is not bound to strict daily cycles
- Users create intentional checkpoints (“seals”) to preserve a state of mind
- Sealed entries are immutable and cannot be modified
- Reflections extend historical entries without altering original content
- The system prioritizes continuity of thought over rewriting history

---

## Core Concept

TimeSeal operates on a simple model:

WORKING STATE → SEAL (Checkpoint) → SEALED HISTORY → REFLECTION LAYER

- **Working State**: Active, editable notes
- **Seal (Checkpoint)**: User-triggered snapshot of current state
- **Sealed History**: Immutable record stored via Git snapshot
- **Reflection Layer**: Append-only continuation of past thoughts

---

## Features

### Journaling & Reflection

- Local-first journaling system
- Manual checkpoint ("Seal") creation
- Timestamped entries for traceability
- Read-only access to sealed history
- Reflection system for extending past checkpoints
- Quick return to the current working state
- Plain text / Markdown-based storage
- Git-based snapshot history for sealed states

### AI Integration

TimeSeal can generate structured metadata for journal entries using local language models through LM Studio.

Current capabilities include:

- Local AI-powered metadata generation
- Entry summarization
- Topic tag extraction
- Local-only processing (no cloud dependency)
- LM Studio server integration
- Dynamic model selection
- In-app model loading and switching

The AI system is entirely optional and operates locally on the user's machine. Its purpose is to support reflection and note organization while preserving the user's original writing.

---

## Tech Stack

* Python
* PySide6 (Qt-based UI framework)
* Local filesystem storage (Markdown / text files)
* Git for snapshot-based history preservation
* LM Studio (local LLM runtime)
* Local language models (user selectable)

---

## Design Goals

TimeSeal is an experiment in structured memory and temporal awareness in software systems.

It explores how personal software can:

- Preserve cognitive history without overwriting it
- Treat meaningful moments as explicit checkpoints
- Separate “thinking in progress” from “thought already preserved”
- Use Git as a model for human reflection and memory

---

## Status

Active personal project and experimental journaling tool.

Current focus areas:

* Temporal journaling workflow
* Reflection-based note preservation
* Local AI-assisted metadata generation
* LM Studio integration

The project is under active development and the AI subsystem is expected to evolve as new features are added.

---