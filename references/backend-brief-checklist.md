# Backend Brief Checklist — detailed prompts per section

Companion to `backend-systems-brief`. Work these prompts; skip a section only by writing n.a. with a reason.

## 1. System responsibilities (product language)

- For each user promise in the mechanisms: what must the system make TRUE, always? Phrase as "the system guarantees…" sentences.
- Which guarantees are trust-critical (user leaves if broken once)? Mark them.

## 2. Trust-critical mechanisms

- Memory: what is stored, who can read it, how wrong memories are corrected, growth over time.
- Judging/scoring: where the verdict is computed, what is logged (verdict + reason + delta + time), replay/audit ability.
- Paid actions: atomicity of deduction+execution, refund on failure, idempotency of retries.
- Moderation/creator validation: pipeline states, who can action, evidence retention.

## 3. Data categories (classify EVERY data kind the product touches)

- user-visible / hidden system evidence / audit / user-editable / sensitive (PII, verification, payment) / disposable.
- For sensitive: retention promise, disposal moment, and what survives (e.g. "verification raw data discarded; boolean + date kept").
- For user-editable: conflict rule when system and user edit the same thing.

## 4. Lifecycle map

- Per entity: create → update → summarize/derive → publish/share → archive → delete → recover → appeal. Which transitions are user-triggered vs system-triggered vs operator-triggered?
- Deletion: soft vs hard, cascade scope, and the user-facing promise ("delete removes X within Y").

## 5. Permissions and boundaries

- Roles (user/creator/moderator/admin) × surfaces: who reads, who writes, who approves.
- Safety boundaries: age-gated content excluded server-side for unverified accounts (structural, not UI filter).
- Public/private transitions: what happens to derived data (rankings, counts) when content goes private.

## 6. Failure and dispute handling

- For each trust-critical mechanism: the worst realistic failure, what the user sees, the recovery path, what support/ops needs to resolve it.
- Disputes: what evidence exists (logs, versions), who arbitrates.

## 7. Operational questions

- Cost drivers (per-turn AI calls, storage growth, image generation) with the rough order of magnitude.
- Latency budgets on the hot path; what degrades gracefully when a dependency is slow.
- Observability: which product events MUST be measurable at launch (tie to the PRD's success metrics).
- Abuse: rate limits, self-boosting, scraping, prompt injection where AI-facing.

## 8. Engineering decisions later (questions, not decisions)

- List the architecture-level choices deliberately deferred (storage, queues, providers) — one line each on what product constraint bounds the choice.
