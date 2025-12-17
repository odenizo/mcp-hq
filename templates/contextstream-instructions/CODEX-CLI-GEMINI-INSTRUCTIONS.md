## ContextStream Integration

You have access to ContextStream MCP tools for persistent memory and context.

**TOOL NAMING BY CLIENT:**
- **Codex CLI / Gemini CLI:** Use raw tool names (e.g., `session_init`)
- **GitHub Copilot CLI:** Use server-prefixed names (e.g., `contextstream-session_init`)

## TL;DR - REQUIRED EVERY MESSAGE

**For Codex CLI / Gemini CLI:**

| Message | What to Call |
|---------|--------------|
| **1st message** | `session_init(folder_path="...", context_hint="<user's message>")` |
| **2nd+ messages** | `context_smart(user_message="<user's message>")` |
| **After completing task** | `session_capture(...)` - MUST capture decisions/insights |
| **User frustration/correction** | `session_capture_lesson(...)` - MUST capture lessons |

**For GitHub Copilot CLI:**

| Message | What to Call |
|---------|--------------|
| **1st message** | `contextstream-session_init(folder_path="...", context_hint="<user's message>")` |
| **2nd+ messages** | `contextstream-context_smart(user_message="<user's message>")` |
| **After completing task** | `contextstream-session_capture(...)` - MUST capture decisions/insights |
| **User frustration/correction** | `contextstream-session_capture_lesson(...)` - MUST capture lessons |

**NO EXCEPTIONS.** Do not skip even if you think you have enough context.

---

### Why context_smart is Required (Even After session_init)

**Common mistake:** "session_init already gave me context, I don't need context_smart"

**This is WRONG. Here's why:**
- `session_init` returns the last ~10 items **BY TIME** (chronological)
- `context_smart` **SEARCHES** for items **RELEVANT to THIS message** (semantic)

**Example failure:**
- User asks: "how should I implement authentication?"
- Auth decisions were made 20 conversations ago
- `session_init` won't have it (too old, not in recent 10)
- `context_smart` FINDS it via semantic search

**Without context_smart, you WILL miss relevant older context.**

---

### When to Capture (MANDATORY)

| When | Tool | Example |
|------|------|---------|
| User makes a decision | `session_capture` | "Let's use PostgreSQL" → capture as decision |
| User states preference | `session_capture` | "I prefer TypeScript" → capture as preference |
| You complete a task | `session_capture` | Capture what was done, decisions made |
| Need past context | `session_recall` | "What did we decide about X?" |

**You MUST capture after completing any significant task.** This ensures future sessions have context.

---

### Behavior Rules

**First message of conversation:**
- Codex/Gemini: `session_init(folder_path="<cwd>", context_hint="<user's message>")`
- Copilot CLI: `contextstream-session_init(folder_path="<cwd>", context_hint="<user's message>")`

**Every subsequent message:**
- Codex/Gemini: `context_smart(user_message="<user's message>")` FIRST
- Copilot CLI: `contextstream-context_smart(user_message="<user's message>")` FIRST

**After completing a task:**
- Codex/Gemini: `session_capture(...)`
- Copilot CLI: `contextstream-session_capture(...)`

**When user asks about past decisions:**
- Codex/Gemini: `session_recall`
- Copilot CLI: `contextstream-session_recall`

---

### Lesson Capture (MANDATORY)

When the user:
1. **Expresses frustration** (caps, profanity, "COME ON", "WTF", repeated corrections)
2. **Corrects you** ("No, you should...", "That's wrong", "Fix this")
3. **Points out a mistake** (broken code, wrong approach, production issue)

You MUST immediately call the lesson capture tool:
- Codex/Gemini: `session_capture_lesson`
- Copilot CLI: `contextstream-session_capture_lesson`

With these parameters:

| Field | Description | Example |
|-------|-------------|---------|
| `title` | What to remember | "Verify assets in git before pushing" |
| `severity` | `critical`/`high`/`medium`/`low` | `critical` for production issues |
| `category` | `workflow`/`code_quality`/`verification`/`communication`/`project_specific` | `workflow` |
| `trigger` | What action caused the problem | "Pushed code referencing images without committing them" |
| `impact` | What went wrong | "Production 404 errors - broken landing page" |
| `prevention` | How to prevent in future | "Run git status to check untracked files before pushing" |
| `keywords` | Keywords for matching | `["git", "images", "assets", "push"]` |

**Example call:**
```json
{
  "title": "Always verify assets in git before pushing code references",
  "severity": "critical",
  "category": "workflow",
  "trigger": "Pushed code referencing /screenshots/*.png without committing images",
  "impact": "Production 404 errors - broken landing page",
  "prevention": "Run 'git status' to check untracked files before pushing code that references static assets",
  "keywords": ["git", "images", "assets", "push", "404", "static"]
}
```

**Why this matters:**
- Lessons are surfaced automatically in `session_init` and `context_smart`
- Future sessions will warn you before repeating the same mistake
- This prevents production issues and user frustration

**Severity guide:**
- `critical`: Production outages, data loss, security issues
- `high`: Breaking changes, significant user impact
- `medium`: Workflow inefficiencies, minor bugs
- `low`: Style/preference corrections
