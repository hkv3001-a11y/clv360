# CLV360 Phase 1 — Design Spec
**Date:** 2026-05-07  
**Status:** Approved  
**Scope:** Contractor vertical — internal command center

---

## 1. Product Overview

CLV360 is an internal AI-powered command center for small contracting businesses. It eliminates the owner/project manager as the manual relay between field crews and the office. Field workers send updates via their existing channels; the AI processes them and keeps the dashboard current automatically.

**Phase 1 focus:** Contractor/field service vertical only. One tenant per deployment for now (multi-tenant/SaaS infrastructure is Phase 3).

**North star metric:** Owner spends less time manually relaying job status updates between field and office.

---

## 2. Users & Roles

| Role | Access | How they interact |
|------|--------|-------------------|
| Owner | Full dashboard + AI chat | Web browser |
| Project Manager | Full dashboard + AI chat (same as owner for Phase 1) | Web browser |
| Field Worker | None (no login) | Text, WhatsApp, or email |

Field workers never touch the dashboard. They communicate exactly as they do today; the system meets them where they are.

---

## 3. What's In Scope (Phase 1)

- Job/project tracking dashboard
- AI chat assistant for owner/PM
- Inbound message pipeline (SMS, WhatsApp, email → AI parser → dashboard)
- Crew member management
- Weather panel with 7-day forecast
- Proactive AI alerts (stale jobs, weather impact warnings)

**Explicitly out of scope for Phase 1:**
- Login / authentication (no auth — run locally)
- Client-facing portal
- Leads pipeline
- Mobile app
- Billing/subscription infrastructure
- Multi-tenant / multi-business support
- Other industry verticals (real estate, car sales, etc.)

---

## 4. Data Model

### Job
```
id, name, address, status (active | on_hold | completed | cancelled),
crew_member_id, percent_complete, start_date, target_date, created_at, updated_at
```

### CrewMember
```
id, name, phone, email, created_at
```

### ActivityEntry
```
id, job_id, source_name, channel (sms | whatsapp | email | manual | ai),
raw_message, parsed_action, created_at
```

### Note
```
id, job_id (nullable — null = general note), body, author, created_at
```

### User (Owner / PM)
```
id, email, name, role (owner | pm), created_at
```
*(Auth handled by Supabase — to be connected later)*

---

## 5. Dashboard Layout

**Layout A — Command Center (approved)**

```
┌─────────────────────────────────────────────────┐
│  72°F  Nashville · Partly Cloudy · Wind 8mph     │
│  Mon☀️ Tue🌧️ Wed⛈️ Thu☀️ Fri⛅ Sat☀️ Sun☀️    │
├──────────────────────────┬──────────────────────┤
│  📋 Active Jobs          │  🤖 AI Assistant     │
│  ─────────────────────── │  ─────────────────── │
│  Johnson Roofing  75% ✅ │  [chat history]      │
│  Garcia Drywall   30% ⏸️ │                      │
│  Smith Foundation 10% ⚠️ │                      │
│  Lee HVAC Install  0% 🔵 │  [input bar]         │
└──────────────────────────┴──────────────────────┘
```

- Weather bar spans full width at the top (7-day forecast, current conditions)
- Left panel: job list with status color indicators and completion percentage
- Right panel: AI chat always visible — no toggling required
- Status colors: green (active/on track), amber (on hold), red (delayed/flagged), blue (pending/not started)

---

## 6. AI Assistant Capabilities

### 6a. Inbound Parser (background, always running)
Processes messages from field workers via SMS, WhatsApp, or email. Maps each message to a job and takes the appropriate action.

Examples:
- "Johnson roof is done" → status: completed, percent: 100, logs activity
- "Garcia job delayed, waiting on drywall" → status: on_hold, logs reason
- "Starting the Lee HVAC job now" → status: active, logs start
- Unrecognized → logs as raw note, flags for owner review

**Stub for Phase 1:** SMS and WhatsApp webhooks are stubbed out. A test endpoint (`POST /api/inbound/test`) accepts a JSON payload `{channel, sender_name, message}` so the pipeline can be tested without live Twilio/WhatsApp connections.

### 6b. Conversational Assistant (owner/PM initiated)
Natural language queries against live dashboard data.

Examples:
- "What's behind schedule?" → returns delayed/stale jobs
- "Which crew member is free this week?" → checks active assignments
- "Summarize this week's activity" → digest from activity feed
- "Mark the Garcia job complete" → takes direct action, confirms

### 6c. Proactive Alerts (AI-initiated, shown in chat + dashboard)
- Job has no activity update in 5+ days → flag to owner
- Upcoming weather event (rain, storm) at job location → warn owner
- Surfaced at login and periodically in the chat panel

---

## 7. Inbound Message Pipeline

```
Field worker sends message
       ↓
[SMS]     Twilio webhook  ─┐
[WhatsApp] Twilio webhook  ─┼→ POST /api/inbound/{channel}
[Email]   Postmark webhook ─┘
       ↓
FastAPI validates webhook signature
       ↓
Send to Claude API:
  - System prompt: "You are a job update parser. Given a message and
    the current job list, identify which job is being updated and
    what action to take."
  - User message: raw text + job list context
       ↓
Claude returns structured JSON:
  { job_id, action, percent_complete, status, summary }
       ↓
FastAPI writes ActivityEntry + updates Job in Supabase
       ↓
Supabase real-time pushes update to dashboard
       ↓
Dashboard updates live — owner sees it instantly
```

**Phase 1 stub:** Twilio and Postmark connections are not wired up. Use `POST /api/inbound/test` to simulate any channel. Supabase connection is also stubbed — local SQLite used for initial development, with a clean migration path to Supabase.

---

## 8. Tech Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| Frontend | React + Tailwind CSS | Dark theme, component-based |
| Backend | Python + FastAPI | Existing prototype as reference |
| Database | SQLite → Supabase (PostgreSQL) | SQLite for local dev; Supabase connected later |
| Auth | None (Phase 1) → Supabase Auth (Phase 2) | No login required for Phase 1 — run locally, open access |
| AI | OpenRouter API | claude-sonnet-4-6 via OpenRouter |
| SMS | Twilio | Stubbed for Phase 1 |
| WhatsApp | Twilio WhatsApp Business API | Stubbed for Phase 1; owner chooses SMS or WhatsApp during onboarding |
| Email inbound | Postmark inbound | Stubbed for Phase 1 |
| Frontend hosting | Vercel | |
| Backend hosting | Railway | |
| Real-time updates | Supabase Realtime | Connected with Supabase later |

---

## 9. Key API Endpoints

```
GET  /api/jobs                     — list all jobs
POST /api/jobs                     — create job
PUT  /api/jobs/{id}                — update job
DELETE /api/jobs/{id}              — delete job

GET  /api/jobs/{id}/activity       — get activity feed for a job
POST /api/jobs/{id}/activity       — manually add activity entry

GET  /api/crew                     — list crew members
POST /api/crew                     — add crew member
PUT  /api/crew/{id}                — update crew member
DELETE /api/crew/{id}              — remove crew member

GET  /api/notes                    — list all notes
POST /api/notes                    — create note

POST /api/inbound/test             — simulate inbound field message (Phase 1 testing)
POST /api/inbound/sms              — Twilio SMS webhook (stubbed)
POST /api/inbound/whatsapp         — Twilio WhatsApp webhook (stubbed)
POST /api/inbound/email            — Postmark inbound webhook (stubbed)

POST /api/chat                     — send message to AI assistant, returns response
GET  /api/weather                  — fetch weather for configured location

GET  /api/alerts                   — get current proactive alerts
```

---

## 10. Build Order (Phase 1)

1. **Backend foundation** — FastAPI app, SQLite data layer, all CRUD endpoints
2. **AI chat** — Claude API integration, conversational assistant
3. **Inbound pipeline** — parser logic + `/api/inbound/test` stub endpoint
4. **Frontend shell** — React app, Layout A structure, dark theme
5. **Jobs panel** — job list, status indicators, create/edit/delete
6. **AI chat panel** — frontend chat UI wired to `/api/chat`
7. **Weather panel** — top bar with 7-day forecast
8. **Activity feed** — per-job update history
9. **Crew management** — crew list, assignments
10. **Proactive alerts** — AI-generated flags surfaced in dashboard

---

## 11. Future Phases (not in scope now)

- **Phase 2:** Supabase + auth wired up, Twilio SMS + WhatsApp live, email inbound live
- **Phase 3:** Multi-tenant SaaS infrastructure, billing (Stripe), onboarding flow
- **Phase 4:** Additional verticals (real estate, car sales) built on the same platform core
- **Phase 5:** Client-facing status portal
