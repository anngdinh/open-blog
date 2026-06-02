# Cover Image Flow v2 — Design

**Date:** 2026-06-02
**Scope:** `.claude/skills/write-blog/SKILL.md` cover-image section + re-cover existing duplicate posts.

## Problem

5 of 11 posts share a cover image with another post:

| Cover hash | Posts |
|---|---|
| `3532f737…` | database-indexes-deep-dive, ebpf-deep-dive, gvisor-vs-firecracker |
| `d29da917…` | istio-preserve-source-ip, lb-proxy-protocol-kep-1860 |

**Root cause:** the skill instructs the model to construct `https://images.unsplash.com/photo-<ID>?…`
URLs, but the model cannot browse Unsplash. It falls back to a handful of memorized photo IDs →
reuse. There is no uniqueness check.

## Solution

Replace memorized-ID construction with the **Unsplash API search endpoint** (relevance-sorted,
multiple candidates) plus a **mandatory visual-verification step**: the model downloads several
candidates, opens each with the Read tool, and picks the one that genuinely fits. Add an md5
uniqueness check and a required photographer caption (Unsplash API terms).

> **Why search + verify, not `random`?** The first implementation used `photos/random?query=`.
> It returned exactly one image of weak relevance — a JavaScript screenshot for an eBPF post,
> Scrabble tiles for a sandboxing post. The model cannot judge relevance from a URL, so it must
> actually view candidates. The search endpoint provides several relevance-ranked options to
> choose from.

### New flow (replaces steps 1–7 of the skill's "Cover image" section)

1. **Load the key.** Read `UNSPLASH_ACCESS_KEY` (the project keeps it in gitignored `.env`).
   If unset → stop and tell the user to set it (free key at unsplash.com/developers). No
   memorized-ID fallback.
2. **Pick a short query (1–2 words).** Long phrases return `No photos found`.
3. **Download ~4 candidates** from `search/photos?query=<topic>&per_page=6` to `/tmp`. Parse the
   JSON with `strict=False` (Unsplash responses can contain raw control characters).
4. **View each candidate with the Read tool** and pick the best topical match; note its `id`,
   author name, author link. If none fit, rerun with a different query.
5. **Install + check uniqueness:** copy the pick to `public/images/<slug>/cover.jpg`; md5 against
   all existing covers and warn on collision; ping `photos/<id>/download` (API compliance);
   verify >10KB.

### Caption credit

Cover block gains a credit line with the UTM params Unsplash requires:

```jsx
<div style={{display:'flex', justifyContent:'center', margin:'2rem 0'}}>
  <img src="/images/<slug>/cover.jpg" alt="..." style={{maxWidth:'800px', width:'100%', height:'auto', borderRadius:'8px'}} />
</div>
<p style={{textAlign:'center', fontSize:'0.85rem', opacity:0.7, marginTop:'-1rem'}}>
  Photo by <a href="<user.links.html>?utm_source=open-blog&utm_medium=referral">Name</a> on <a href="https://unsplash.com/?utm_source=open-blog&utm_medium=referral">Unsplash</a>
</p>
```

### Re-cover existing duplicates (minimal — break the dups only)

Keep one cover per group, re-cover the rest via the new flow + caption:

- Keep `database-indexes-deep-dive` → re-cover **ebpf-deep-dive**, **gvisor-vs-firecracker**
- Keep `istio-preserve-source-ip` → re-cover **lb-proxy-protocol-kep-1860**

The off-spec `envoy-…` PNG is not a duplicate — left untouched.

## Out of scope

- Resizing/normalizing the envoy PNG cover.
- Backfilling captions on non-duplicate posts.
