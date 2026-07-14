/**
 * ATES Task→Ability Crowdsource Annotation — Backend
 * ---------------------------------------------------
 * Serves the annotation form and writes every submission into a Google Sheet.
 * No external database. Runs entirely inside your Google account for free.
 *
 * SETUP: This script must be CONTAINER-BOUND to a Google Sheet.
 *   Create a Google Sheet → Extensions → Apps Script → paste this file
 *   (and Index.html) → Deploy → Web app.
 * See DEPLOY.md for the full step-by-step.
 */

// Name of the tab where annotations are stored (auto-created on first submit).
var RESPONSE_SHEET = 'Responses';

// Column headers written to the Responses tab.
var HEADERS = [
  'timestamp', 'annotator', 'annotator_email', 'session_id',
  'task_id', 'occupation', 'task_text', 'ability_name',
  'llm_weight', 'human_judgment', 'corrected_weight',
  'is_addition', 'overall_task_rating', 'comment'
];

/**
 * Serves the HTML form. Supports optional ?start= &end= URL params so you can
 * hand out different task ranges to different people (divide and conquer).
 *   e.g.  ...exec?start=1&end=50   ...exec?start=51&end=100
 */
function doGet(e) {
  var t = HtmlService.createTemplateFromFile('Index');
  t.startParam = (e && e.parameter && e.parameter.start) ? e.parameter.start : '';
  t.endParam   = (e && e.parameter && e.parameter.end)   ? e.parameter.end   : '';
  return t.evaluate()
    .setTitle('ATES Task→Ability Annotation')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1.0')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Returns (creating if needed) the Responses sheet with a header row. */
function getResponseSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(RESPONSE_SHEET);
  if (!sh) {
    sh = ss.insertSheet(RESPONSE_SHEET);
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
  }
  return sh;
}

/**
 * Called from the browser via google.script.run.
 * payload = {
 *   annotator: string, email: string, sessionId: string,
 *   rows: [[task_id, occupation, task_text, ability_name, llm_weight,
 *           human_judgment, corrected_weight, is_addition,
 *           overall_task_rating, comment], ...]
 * }
 *
 * UPSERT behavior (keyed on session_id + task_id):
 *   - Same annotator (same session_id) re-submitting the SAME task_id
 *     -> their previous rows for that task are REPLACED (no duplicates).
 *   - A DIFFERENT annotator (different session_id) submitting the same task
 *     -> stored as separate rows. Every annotator keeps their own entry.
 *
 * Returns { ok, written, replaced, totalResponses }.
 */
function submitAnnotation(payload) {
  var lock = LockService.getScriptLock();
  lock.waitLock(30000); // serialize writes so simultaneous submits don't collide
  try {
    var sh = getResponseSheet_();
    var ts = new Date();
    var sid = String(payload.sessionId || '');
    var prefix = [ts, payload.annotator || '', payload.email || '', sid];
    var out = (payload.rows || []).map(function (r) { return prefix.concat(r); });
    if (out.length === 0) return { ok: true, written: 0, replaced: 0, totalResponses: sh.getLastRow() - 1 };

    var taskId = String(out[0][4]); // task_id column (0-based index 4)
    var SID_COL = 3, TASK_COL = 4;  // 0-based positions of session_id and task_id

    // 1) Remove this annotator's PRIOR rows for THIS task (if any), so a
    //    re-submit updates in place instead of duplicating.
    var replaced = 0;
    var last = sh.getLastRow();
    if (last > 1 && sid) {
      var data = sh.getRange(2, 1, last - 1, HEADERS.length).getValues();
      var rowsToDelete = [];
      for (var i = 0; i < data.length; i++) {
        if (String(data[i][SID_COL]) === sid && String(data[i][TASK_COL]) === taskId) {
          rowsToDelete.push(i + 2); // +2: skip header (row 1) and 0-based offset
        }
      }
      // Delete bottom-up so earlier row numbers stay valid as we remove.
      for (var j = rowsToDelete.length - 1; j >= 0; j--) {
        sh.deleteRow(rowsToDelete[j]);
        replaced++;
      }
    }

    // 2) Append the fresh rows for this (annotator, task).
    var startRow = sh.getLastRow() + 1;
    sh.getRange(startRow, 1, out.length, out[0].length).setValues(out);
    SpreadsheetApp.flush();
    return { ok: true, written: out.length, replaced: replaced, totalResponses: sh.getLastRow() - 1 };
  } catch (err) {
    return { ok: false, error: String(err) };
  } finally {
    lock.releaseLock();
  }
}

/** Lightweight stat call for the form's progress banner. */
function getGlobalCount() {
  var sh = getResponseSheet_();
  return Math.max(0, sh.getLastRow() - 1);
}
