export const meta = {
  name: 'juicecraft-ad-review',
  description: 'Four-lens critical review of the 15 s ad preview, then adversarial dedup into a prioritized fix list',
  phases: [
    { title: 'Critique', detail: 'motion, art direction, copy/claims, technical QA — in parallel' },
    { title: 'Verify', detail: 'check every issue against the frames, drop false ones, prioritize, map to code' },
  ],
}

const BASE = '/home/user/juicecraft/video'
const CONTEXT = `You are reviewing a 15-second advertising spot for "juicecraft", a French studio that builds custom websites (tagline: "Des sites qui ont du jus." — sites with juice). The spot must look like the work of an elite motion designer: ultra clean, convincing, premium. It exists in two formats rendered from the same HTML/JS composition:
- 16:9 (1920x1080) — preview frames: ${BASE}/prev_land/00000.png … 00449.png (30 fps; frame i is at t=(i+0.5)/30 s)
- 9:16 (1080x1920) — preview frames: ${BASE}/prev_port/00000.png … 00449.png (same timing). The vertical cut is meant for Instagram Reels / TikTok / YouTube Shorts.
Contact sheets every 0.1 s: ${BASE}/review/land_sheet_00..04.png and ${BASE}/review/port_sheet_00..04.png (each tile is labelled with its time).
Preview MP4s (silent): ${BASE}/out/preview_land_noaudio.mp4, ${BASE}/out/preview_port_noaudio.mp4. You can extract any frame or make your own crops/zooms with ffmpeg or python PIL (both installed) — write scratch files under ${BASE}/review/scratch/.
The source of the animation is ${BASE}/video.html (a deterministic seek(t) timeline; layout constants in the G object; scenes S1 hook 0–2 s, S2 press 2–3 s, S3 drop+reveal 3–5 s, S4 five proof beats 5–10 s, S5 real site on laptop+phone 10–12.5 s, S6 end card 12.5–15 s). The timing/sound cue sheet is ${BASE}/cues.json (a synced soundtrack is being produced separately to these exact cue times — sync points matter).
Story: "Votre site manque de jus ?" (an ugly 2000s website) → it gets crushed in a juice press → juice floods the screen → "juicecraft" → the real juicecraft site in a browser → 5 proofs (Sur mesure / Sur tous les écrans / Rapide / Sécurisé / Visible) with live UI demos → the real site on laptop+phone with "Votre [commerce/atelier/cabinet/restaurant] mérite un site qui a du jus." → end card with logo, tagline, CTA "Demandez votre devis".
Look at actual pixels. Open the contact sheets with the Read tool, then open full-resolution frames around anything suspicious (and around every transition). Be specific and concrete: exact time (s), format (land/port/both), the element, what is wrong, and a precise fix (ideally naming the code location/constant in video.html). Do not pad with generic advice; only report things you can point to in the frames. Rank by how much each issue hurts the "elite motion designer" impression.`

const ISSUES = {
  type: 'object',
  properties: {
    issues: { type: 'array', items: { type: 'object', properties: {
      severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
      time_s: { type: 'string', description: 'time or range, e.g. "2.35" or "9.8-10.3"' },
      format: { type: 'string', enum: ['land', 'port', 'both'] },
      element: { type: 'string' },
      problem: { type: 'string' },
      fix: { type: 'string' },
    }, required: ['severity', 'time_s', 'format', 'element', 'problem', 'fix'] } },
    overall: { type: 'string', description: 'two or three sentences: honest overall verdict from this lens' },
  },
  required: ['issues', 'overall'],
}

const LENSES = [
  { key: 'motion', prompt: `LENS: MOTION DESIGN & TIMING. Judge like a senior motion designer at a top studio. Check: easing quality (anything linear or mechanical where it should be eased, or ease-outs that feel limp), anticipation/overshoot, continuity across cuts (do elements carry momentum and screen direction from one scene to the next, or do they just appear/disappear?), pacing and energy curve over 15 s, holds long enough to read each text (rule of thumb ~0.25 s per short word after it settles), frames where things pop in/out without a transition, the five proof beats (are they legible in 1 s each?), the liquid transitions (do they read as juice?), the end card hold. Sample densely around transitions (every frame).` },
  { key: 'art', prompt: `LENS: ART DIRECTION, TYPOGRAPHY & COMPOSITION. Judge like an agency art director. Check: composition and balance of every scene in BOTH formats (dead space, crowding, elements too small to read on a phone, scale hierarchy), type sizes/line breaks/widows, colour harmony and contrast, consistency of the visual language (paper/ink/juice palette), how premium each frame looks, and SAFE ZONES for 9:16 social: TikTok/Reels overlay UI on roughly the bottom 20–25 % and the right ~12 % (icons) and the top ~10 % — any key text/CTA/logo in those zones in the port version is a problem. Also check the 16:9 end card and logo lockup proportions.` },
  { key: 'copy', prompt: `LENS: COPY, MESSAGE & CLAIMS. Judge like a French senior copywriter and a compliance reviewer. Check: French spelling, accents, typography (espaces insécables before ? ! : in French, guillemets), consistency of wording with the brand, whether the narrative is convincing in 15 s (problem → solution → proof → call to action), whether the CTA is strong and clear, and any claim that could be misleading in an ad (e.g. a displayed performance score of 98, fictional businesses shown as if they were clients, "Paiement sécurisé" demos, a fake search result — are they framed as illustrations or could a viewer read them as real client results?). Read every text visible in the frames (zoom in).` },
  { key: 'tech', prompt: `LENS: TECHNICAL QA. Judge like a finishing/online editor. Check frame by frame for: glitches, z-order errors, elements visible outside their scene, text clipping or overflow, aliasing/jaggies, banding in gradients, flicker between consecutive frames (compare neighbours), one-frame pops, misaligned elements, images not loaded or blurry/upscaled screenshots, the WebGL liquid edges (hard/aliased or too soft?), grain level, black/white levels, and anything that differs incorrectly between the two formats. Use pixel diffs between consecutive frames (python PIL/numpy) to find sudden jumps, then inspect them.` },
]

phase('Critique')
const reviews = await parallel(LENSES.map(l => () =>
  agent(`${CONTEXT}\n\n${l.prompt}\n\nReturn your findings via the structured output.`, { label: `critic:${l.key}`, phase: 'Critique', schema: ISSUES })
    .then(r => r ? { lens: l.key, ...r } : null)))

const all = reviews.filter(Boolean)
log(`${all.reduce((n, r) => n + r.issues.length, 0)} raw issues from ${all.length} critics`)

phase('Verify')
const FINAL = {
  type: 'object',
  properties: {
    fixes: { type: 'array', items: { type: 'object', properties: {
      priority: { type: 'integer', description: '1 = most important' },
      severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
      time_s: { type: 'string' }, format: { type: 'string' },
      problem: { type: 'string' }, evidence: { type: 'string', description: 'which frame(s) you opened and what you saw' },
      code_change: { type: 'string', description: 'precise change to video.html (function/constant, old → new), or "n/a"' },
      lenses: { type: 'array', items: { type: 'string' } },
    }, required: ['priority', 'severity', 'time_s', 'format', 'problem', 'evidence', 'code_change', 'lenses'] } },
    rejected: { type: 'array', items: { type: 'object', properties: { issue: { type: 'string' }, reason: { type: 'string' } }, required: ['issue', 'reason'] } },
    verdict: { type: 'string' },
  },
  required: ['fixes', 'rejected', 'verdict'],
}
const final = await agent(`${CONTEXT}

Four critics (motion, art direction, copy/claims, technical QA) reviewed the preview. Their raw findings (JSON):
${JSON.stringify(all, null, 1)}

Your job: be the adversarial lead. For EVERY issue, open the cited frames yourself and try to refute it — reject anything not actually visible, anything that is a matter of taste with no clear improvement, or anything whose "fix" would make the spot worse. Merge duplicates across critics. For the survivors, read ${BASE}/video.html and write a precise code change for each (function or constant, what to change from → to). Prioritize by impact on the "elite motion designer, ultra clean, convincing" bar; blockers first. Keep the list actionable (it will be applied by one engineer in one pass): at most ~20 fixes, each self-contained. List the rejected issues with one-line reasons.`, { label: 'lead-verifier', phase: 'Verify', schema: FINAL })

return { final, critics: all.map(r => ({ lens: r.lens, overall: r.overall, n: r.issues.length })) }
