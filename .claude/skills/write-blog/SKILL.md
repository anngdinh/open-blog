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

Create the post at `src/app/blog/<slug>/page.mdx` with this structure:

```
---
title: "<Post Title>"
description: "<Brief description>"
date: YYYY-MM-DD
---

import { generateBlogMetadata } from "../../../lib/blog";
import BlogJsonLd from "../../../components/blog-json-ld";
import Title from "../../../components/title";

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

[content sections here]

## References

- [Title](url)
- ...
```

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
- [ ] All keyword definitions use the blockquote + bold format
- [ ] Images from references are downloaded to `public/images/<slug>/`
- [ ] No reference images were replaced with text diagrams
- [ ] All code blocks have language tags
- [ ] Text diagrams (if any) use ` ```text ` and have straight borders
- [ ] Reference section exists at the end with all sources credited
- [ ] Alt text on all images is descriptive
