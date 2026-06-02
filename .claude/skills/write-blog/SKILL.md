---
name: write-blog
description: >
  Write a new blog post (MDX) for the open-blog project following established conventions —
  consistent keyword definitions, proper image handling, text diagrams, and reference sections.
  Use this skill whenever the user wants to write, create, or draft a new blog post, even if
  they don't say "blog" explicitly — trigger on phrases like "write about X", "create a post
  about X", "I want to write about X", "draft an article on X", or when the user provides
  reference URLs and asks to turn them into content.
---

# Blog Post Writer

You are writing a blog post for the **open-blog** project — a Next.js MDX blog. Posts live at
`src/app/blog/<slug>/page.mdx` with images at `public/images/<slug>/`.

## Before you start writing

### 1. Determine the language

If the user has not specified a language, ask them which language to write in before proceeding.
Do not assume. The blog has posts in both Vietnamese and English — the user decides.

### 2. Gather context

Understand what the user wants to write about. If they provide reference URLs or blog posts,
read them carefully — they are your primary source material. If no references are given, use
your own knowledge but be upfront about anything you're uncertain of.

### 3. Study existing conventions

Read 1-2 existing posts under `src/app/blog/*/page.mdx` to absorb the current style. Pay
attention to how the frontmatter, imports, metadata export, and components are structured.
Use `src/app/blog/clean-architecture/page.mdx` as the canonical reference for the full
boilerplate pattern.

## Writing the post

### File structure

Create the post at `src/app/blog/<slug>/page.mdx`.

**For short-to-medium posts** (under ~500 lines of content), use a single file:

```
src/app/blog/<slug>/
└── page.mdx          # Everything in one file
```

**For long posts** (over ~500 lines, or when the reference article has many sections), split
into multiple MDX files and import them into the main page. This keeps each file manageable
and allows writing sections in parallel:

```
src/app/blog/<slug>/
├── page.mdx                    # Main file: frontmatter, imports, boilerplate, section imports
├── _sections/
│   ├── 01-introduction.mdx
│   ├── 02-background.mdx
│   ├── 03-core-concept.mdx
│   ├── 04-deep-dive.mdx
│   ├── 05-advanced.mdx
│   └── 06-conclusion.mdx
```

The main `page.mdx` imports and renders each section:

```
---
title: "<Post Title>"
description: "<Brief description>"
date: YYYY-MM-DD
---

import { generateBlogMetadata } from "../../../lib/blog";
import BlogJsonLd from "../../../components/blog-json-ld";
import Title from "../../../components/title";

import Introduction from "./_sections/01-introduction.mdx";
import Background from "./_sections/02-background.mdx";
import CoreConcept from "./_sections/03-core-concept.mdx";
import DeepDive from "./_sections/04-deep-dive.mdx";
import Advanced from "./_sections/05-advanced.mdx";
import Conclusion from "./_sections/06-conclusion.mdx";

export const metadata = generateBlogMetadata({
  title: "<Post Title>",
  description: "<Brief description>",
  date: "YYYY-MM-DD",
  slug: "<slug>"
})

<BlogJsonLd
  url={metadata.openGraph.url}
  title={metadata.title}
  description={metadata.description}
  authorName="Developer"
  publishDate={new Date(metadata.openGraph.publishedTime).toISOString()}
  imageUrl={metadata.openGraph.images?.[0]?.url}
/>

<Title title={metadata.title} date={metadata.date} />

[cover image here]

<Introduction />
<Background />
<CoreConcept />
<DeepDive />
<Advanced />
<Conclusion />

## References

- [Title](url)
- ...
```

Each section file is a plain MDX file with no frontmatter — just content starting with `##`:

```
## Section Title

Content here...
```

**When to split:** if the reference article has 10+ sections, or the total content would exceed
~500 lines, or you're translating a very long article. The split makes it easier to write
sections in parallel using subagents, and keeps each file readable.

**Naming convention:** prefix with numbers (`01-`, `02-`) to maintain order. Use the `_sections/`
directory (underscore prefix) so Next.js doesn't treat them as routes.

### Keyword definitions

When introducing a technical term for the first time, use a blockquote with the term in bold,
followed by a colon and the explanation. This format is consistent across all blog posts:

```markdown
> **Term Name (English if needed)**: Explanation of the term in the chosen language. Include
> enough context so the reader understands what it is and why it matters.
```

If multiple related terms need defining together, use consecutive blockquotes:

```markdown
> **Network Namespace**: Explanation here...

> **veth pair (Virtual Ethernet)**: Explanation here...

> **Bridge**: Explanation here...
```

This format matters because it creates a visual pattern readers can scan for — when they see
a blockquote with a bold term, they know it's a definition. Keep this consistent across every
post.

### Cover image

Every blog post should have a cover image at the top, right after the `<Title>` component.
This image sets the visual tone for the post and appears in social previews.

**Do NOT construct `https://images.unsplash.com/photo-<ID>?…` URLs from memory.** You cannot
browse Unsplash, so any photo ID you "recall" is a guess — and guessing leads to the same few
IDs being reused across posts (duplicate covers). Fetch real candidates through the **Unsplash
API search endpoint**, then **look at the images with the Read tool and pick the one that
actually fits** — you cannot judge relevance from the URL alone, and a single random photo is
often off-topic (a query for an eBPF post returned a JavaScript screenshot once).

**How to find and add a cover image:**

1. **Get the API key.** The key lives in the gitignored `.env` file as `UNSPLASH_ACCESS_KEY`
   (free key from unsplash.com/developers, 50 req/hr). If it is not set, **stop** and ask the
   user to set it — do not fall back to constructing URLs by hand.

2. **Choose a short query (1–2 words).** Long phrases like `virtual machine sandbox security
   isolation` often return `No photos found`. Prefer `cybersecurity`, `database`, `kubernetes`,
   `network switch`. Pick a query whose photos will read clearly at banner size.

3. **Download a handful of candidates** to `/tmp` with the search helper (replace `SLUG`/`QUERY`):

   ```bash
   SLUG="<slug>"; QUERY="<topic keywords>"
   export $(grep -v '^#' .env | grep UNSPLASH_ACCESS_KEY | xargs)
   [ -z "$UNSPLASH_ACCESS_KEY" ] && { echo "UNSPLASH_ACCESS_KEY not set — stop and ask the user"; exit 1; }
   resp=$(curl -s "https://api.unsplash.com/search/photos?query=$(printf %s "$QUERY" | python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read()))')&per_page=6&orientation=landscape&content_filter=high" \
     -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY")
   # strict=False: Unsplash JSON can contain raw control chars that break strict json.
   printf '%s' "$resp" | python3 -c "
import sys,json
d=json.loads(sys.stdin.read(), strict=False)
for i,r in enumerate(d.get('results',[])[:4]):
    print('\t'.join([str(i), r['urls']['raw'], r['id'], r['user']['name'], r['user']['links']['html']]))" \
   | while IFS=$'\t' read -r i raw id name link; do
       curl -sL -o "/tmp/cand-$i.jpg" "${raw}&w=1200&h=630&fit=crop&q=80"
       echo "#$i | id=$id | author: $name | link: $link"
     done
   ```

4. **Look at each candidate with the Read tool** (`/tmp/cand-0.jpg`, `-1`, …) and pick the one
   that genuinely matches the topic and reads well as a banner. Note its `id`, author name, and
   author link from the printed list. If none fit, rerun step 3 with a different query.

   Then install your pick, enforce uniqueness, and trigger Unsplash download tracking (required
   by their API terms). Replace `N` with the chosen candidate number and `ID` with its photo id:

   ```bash
   cp "/tmp/cand-N.jpg" "public/images/$SLUG/cover.jpg"
   newsum=$(md5sum "public/images/$SLUG/cover.jpg" | cut -d' ' -f1)
   dup=$(find public/images -name 'cover.*' ! -path "public/images/$SLUG/*" -exec md5sum {} + | grep -c "^$newsum ")
   [ "$dup" -ne 0 ] && echo "WARNING: this image already covers another post — pick a different candidate"
   curl -s "https://api.unsplash.com/photos/ID/download" -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" >/dev/null
   rm -f /tmp/cand-*.jpg
   ls -la "public/images/$SLUG/cover.jpg"   # confirm >10KB
   ```

5. **Place the cover image + attribution caption** right after the `<Title>` component. Unsplash's
   API terms require crediting the photographer with the `utm_source`/`utm_medium` params shown:
   ```jsx
   <Title title={metadata.title} date={metadata.date} />

   <div style={{display: 'flex', justifyContent: 'center', margin: '2rem 0'}}>
     <img
       src="/images/<slug>/cover.jpg"
       alt="Descriptive alt text about the cover image"
       style={{maxWidth: '800px', width: '100%', height: 'auto', borderRadius: '8px'}}
     />
   </div>
   <p style={{textAlign: 'center', fontSize: '0.85rem', opacity: 0.7, marginTop: '-1rem'}}>
     Photo by <a href="<AUTHOR_LINK>?utm_source=open-blog&utm_medium=referral"><AUTHOR_NAME></a> on <a href="https://unsplash.com/?utm_source=open-blog&utm_medium=referral">Unsplash</a>
   </p>
   ```
   Substitute `<AUTHOR_LINK>` and `<AUTHOR_NAME>` with the values the helper printed.

### Images

**Handling images from reference sources is critical — follow these rules carefully:**

1. **Download images from references.** If a reference blog or article contains images, download
   them into `public/images/<slug>/`. Use `curl` or `wget` via the Bash tool. Give files
   descriptive names (e.g., `vpc-architecture.png`, not `image1.png`).

2. **Never replace reference images.** If the reference blog has a diagram as an image, keep
   that image. Do not redraw it as ASCII art or substitute it with a different image. The
   original author's diagram may contain nuances you'd lose by recreating it.

3. **Reference images in MDX** using the established patterns:

   Single centered image:
   ```jsx
   <div style={{display: 'flex', justifyContent: 'center', margin: '2rem 0'}}>
     <img
       src="/images/<slug>/filename.png"
       alt="Descriptive alt text"
       style={{maxWidth: '600px', width: '100%', height: 'auto'}}
     />
   </div>
   ```

   Multiple images side by side (e.g., logos or comparisons):
   ```jsx
   <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '2rem', margin: '2rem 0', flexWrap: 'wrap'}}>
     <img
       src="/images/<slug>/image1.png"
       alt="Description 1"
       style={{maxWidth: '250px', height: 'auto'}}
     />
     <img
       src="/images/<slug>/image2.png"
       alt="Description 2"
       style={{maxWidth: '250px', height: 'auto'}}
     />
   </div>
   ```

4. **Alt text must be descriptive.** Not "image" or "diagram" — describe what the image shows
   (e.g., "Kubernetes Pod network namespace showing veth pairs connecting to host bridge").

### Text diagrams

You can create ASCII/box-drawing diagrams to illustrate concepts that are hard to explain with
text alone. Use them to complement the content — they're a signature style of this blog.

**Rules for text diagrams:**

- Wrap in ` ```text ` code blocks (always use the `text` language tag)
- Use Unicode box-drawing characters (`┌`, `─`, `┐`, `│`, `└`, `┘`, `├`, `┤`, `┬`, `┴`, `┼`)
  for clean borders — or `+`, `-`, `|` for simpler diagrams
- Don't mix character sets within one diagram
- **Always use English for text inside diagrams.** Vietnamese diacritical characters (ổ, ự, ắ,
  etc.) have inconsistent widths in monospace fonts, which causes the right border to misalign.
  English characters are always exactly one column wide, so borders stay straight. The blog
  prose around the diagram can be in any language — this rule only applies to text inside the
  diagram box.
- **Avoid wide Unicode arrows inside diagrams.** Characters like `▶`, `▼`, `→` take 2 columns
  in monospace fonts, breaking right-border alignment. Use ASCII equivalents instead:
  `▶` → `>`, `▼` → `v`, `→` → `->`. The box-drawing border characters (`┌─┐│└┘├┤`) are fine.
- Keep borders straight and aligned (this will be verified by the review-blog skill)
- Do NOT create a text diagram to replace an image from a reference source — the image takes
  priority. You may add a supplementary text diagram alongside an image if it helps explain
  a different angle

### Tables

Use markdown tables for comparisons:

```markdown
| Feature | Option A | Option B |
|---|---|---|
| Speed | Fast | Slow |
| Cost | High | Low |
```

### Code blocks

Every code block needs a language tag — `go`, `bash`, `yaml`, `text`, `typescript`, etc.
Never use a bare ` ``` ` without a language identifier.

### Reference section

Every post ends with a reference section. This is where you credit your sources.

```markdown
## References

- [Article Title](https://example.com/article)
- [Documentation Page](https://docs.example.com/page)
```

If the user provided reference blogs or articles, they go here. If you used your own knowledge,
include links to official documentation or authoritative sources that support the content.

If the blog has related posts in the same project, add a "Related posts" subsection using
internal links:

```markdown
### Related posts

- [Container Networking from Scratch](/blog/container-networking-from-scratch) - Brief description
- [AWS VPC CNI Deep Dive](/blog/aws-vpc-cni-deep-dive) - Brief description
```

## Content quality guidelines

- **Explain the "why" before the "how."** Don't jump straight into commands or code — give the
  reader context for why this topic matters and what problem it solves.
- **Progressive complexity.** Start simple, build up. Each section should build on the previous one.
- **Practical examples.** Include runnable commands or real configs where applicable.
- **Section balance.** Don't have one section with 500 words and another with 50 — keep sections
  roughly proportional to their importance.
- **Introduction should hook.** Start with a question, a problem statement, or a clear "what
  you'll learn" roadmap.
- **Conclusion should wrap up.** Summarize key takeaways, suggest next steps, or link to related
  posts. Don't let the post just stop.

## Checklist before finishing

Before presenting the post to the user, verify:

- [ ] Language matches what the user requested
- [ ] Frontmatter has title, description, date
- [ ] Imports, metadata export, BlogJsonLd, and Title components are included
- [ ] Cover image fetched via the Unsplash API (not a memorized URL), unique (no md5 match with another post's cover), downloaded to `public/images/<slug>/cover.jpg`, placed after Title, with the photographer attribution caption underneath
- [ ] All keyword definitions use the blockquote + bold format
- [ ] Images from references are downloaded to `public/images/<slug>/`
- [ ] No reference images were replaced with text diagrams
- [ ] All code blocks have language tags
- [ ] Text diagrams (if any) use ` ```text ` and have straight borders
- [ ] Reference section exists at the end with all sources credited
- [ ] Alt text on all images is descriptive
