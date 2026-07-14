# Deploy the crowdsourced annotation form (Google, free, no database)

This turns the audit tool into a shareable web form. People open a Google link,
annotate, and every answer lands in a **Google Sheet** you own. No server, no
database, no cost. It's a **Google Apps Script Web App** bound to a Sheet.

**Files in this folder:**
- `Code.gs` — the backend (serves the form, writes answers to the Sheet)
- `Index.html` — the form UI, with the 200 audit tasks embedded
- `generate_index.py` — regenerates `Index.html` (e.g. for all 4,577 tasks)

---

## One-time setup (~5 minutes)

### 1. Create the Sheet + script
1. Go to <https://sheets.google.com> → **Blank spreadsheet**.
2. Rename it e.g. `ATES Annotations`.
3. **Extensions → Apps Script**. A script editor opens.

### 2. Paste the code
1. In the editor, delete the sample `function myFunction() {}` in `Code.gs`
   and paste the entire contents of **`Code.gs`** from this folder.
2. Click the **＋** next to "Files" → **HTML** → name it exactly `Index`
   (Apps Script adds `.html` automatically). Delete its default contents and
   paste the entire contents of **`Index.html`** from this folder.
3. **Save** (💾 or Ctrl/Cmd-S).

### 3. Deploy as a Web App
1. Click **Deploy → New deployment**.
2. Gear icon ⚙ next to "Select type" → **Web app**.
3. Set:
   - **Description:** `Annotation form v1`
   - **Execute as:** **Me** (your account — so it can write to the Sheet)
   - **Who has access:** **Anyone**  *(this lets friends annotate without a Google login)*
4. **Deploy** → it asks you to **Authorize access** → pick your account →
   "Google hasn't verified this app" → **Advanced → Go to (your project) → Allow**.
   *(This warning is normal for your own scripts.)*
5. Copy the **Web app URL** (ends in `/exec`). **That's your shareable link.** ✅

Open it once yourself to test. Submissions appear on a new **`Responses`** tab
in the Sheet (auto-created on the first submit).

---

## Sharing & "divide and conquer"

Hand different people different task ranges by adding `?start=` and `?end=`:

| Person  | Link |
|---------|------|
| You     | `…/exec?start=1&end=50` |
| Friend A| `…/exec?start=51&end=100` |
| Friend B| `…/exec?start=101&end=150` |
| Friend C| `…/exec?start=151&end=200` |

No params = the whole set. Everyone's answers still land in the same `Responses` tab
(with their name, email, timestamp, and a session id), so overlaps are fine and
actually useful — duplicate labels on the same task let you measure agreement.

---

## The "annotate 20 → unlock the full mapping" incentive

In `Index.html`, near the top of the `<script>`:
```js
var UNLOCK_THRESHOLD = 20;   // tasks to annotate before unlocking
var UNLOCK_URL = "";         // paste a Drive/Sheet "anyone with link" URL here
```
Set `UNLOCK_URL` to a share link for the full `layer2_pass1_full.csv` (upload it to
Drive → Share → "Anyone with the link" → copy). Once someone submits 20, a banner
reveals the link. (Honor-system, tracked in their browser — good enough for friends.)

> Note: after editing `Index.html` in the Apps Script editor, do
> **Deploy → Manage deployments → ✏️ Edit → Version: New version → Deploy**
> to publish the change. The `/exec` URL stays the same.

---

## Scaling to all 4,577 tasks

When you're ready to crowdsource the whole dataset (not just the audit sample):
```bash
cd google-form
python3 generate_index.py --full     # rebuilds Index.html with all 4,577 tasks
```
Then paste the new `Index.html` into the Apps Script editor and redeploy a new
version. Give people ranges like `?start=1&end=100`, `?start=101&end=200`, etc.

---

## Getting the data back out

The `Responses` tab **is** your dataset — one row per (task, ability) judgment,
same columns as `audit_ratings.csv`:

```
timestamp · annotator · annotator_email · session_id · task_id · occupation ·
task_text · ability_name · llm_weight · human_judgment · corrected_weight ·
is_addition · overall_task_rating · comment
```

**File → Download → CSV** whenever you want to compute Cohen's κ or fold the
human labels back into the dataset. The κ script consumes this format directly.

---

## Quotas (you won't hit these)
Apps Script free tier: ~20,000 form loads/day and plenty of writes for a
friends-and-colleagues annotation drive. If it ever complains, it resets daily.
