---
name: review-blog
description: >
  Review a blog post (MDX) for technical accuracy, writing quality, text diagram formatting,
  and structure, then output actionable recommendations. Diagram quality is the top priority —
  check that ASCII/box-drawing diagrams have straight borders, aligned columns, and no corrupted
  characters. Use this skill whenever the user finishes writing or editing a blog post and wants
  feedback — trigger on phrases like "review this blog", "check my post", "review the blog I
  just wrote", or any request to improve/critique a blog post. Also trigger when the user creates
  a new MDX blog post and asks for a review or recommendations.
---

# Blog Post Reviewer

You are reviewing a blog post for the **open-blog** project — a Next.js MDX blog focused on
DevOps, infrastructure, and backend engineering topics. Posts are primarily written in Vietnamese
with English technical terms.

## How to run a review

1. **Identify the target post.** If the user doesn't specify a file, look for recently modified
   `.mdx` files under `src/app/blog/*/page.mdx` (check git status or file modification times).
2. **Read the full post** — every line matters for a thorough review. **For multi-file posts**
   (those with a `_sections/` directory), read `page.mdx` AND every section file. Check for
   section files with: `ls src/app/blog/<slug>/_sections/` — if the directory exists, the post
   is multi-file and you need to review all of them. Run the diagram check script on each
   section file individually.
3. **Run through each review dimension** below and collect findings.
4. **Output a single recommendations report** using the format at the bottom. For multi-file
   posts, prefix each finding with the filename (e.g., `_sections/03-core-concept.mdx: Line 45`).

## Review dimensions

### 1. Frontmatter (quick check)

Just verify the basics are present — don't spend time on SEO optimization:

- `title` — present and descriptive
- `description` — present
- `date` — present and valid format (YYYY-MM-DD)

### 2. Technical accuracy

- **Commands and configs**: verify shell commands, YAML configs, Dockerfiles, and code snippets
  are syntactically correct and use current/non-deprecated options.
- **Conceptual claims**: flag statements that are misleading or overly simplified without
  acknowledging nuance. Use your knowledge to verify, but be honest when something is outside
  your confidence — say "worth double-checking" rather than making something up.
- **Version references**: if the post mentions specific versions of tools (Kubernetes, AWS CLI,
  Go, etc.), note whether those versions are current or outdated.

### 3. Writing quality

The blog is written in Vietnamese with English technical terms mixed in. Review for:

- **Clarity** — are explanations easy to follow? Is the logical flow coherent?
- **Consistency** — does the post maintain a consistent style throughout? (e.g., not switching
  between formal and informal Vietnamese randomly)
- **Grammar/typos** — catch obvious Vietnamese or English typos and grammar issues
- **Section balance** — are some sections disproportionately long or short compared to their
  importance?

### 4. Text Diagrams (high priority)

This blog relies heavily on ASCII/box-drawing diagrams. Diagram quality is critical — broken
diagrams look unprofessional and confuse readers.

**Do not eyeball diagram alignment.** Human counting of spaces is unreliable — off-by-one
errors are invisible when reading but obvious when rendered. Instead, run the verification
script to programmatically check every diagram:

```bash
python3 .claude/skills/review-blog/scripts/check_diagrams.py <path-to-mdx-file>
```

The script measures the actual display width of each line using Unicode `east_asian_width`
and reports any lines that don't match the expected width. It also flags Vietnamese characters
and wide Unicode arrows inside diagrams. Include the script output in your review.

In addition to running the script, visually check for:

- **Corrupted characters** — look for U+FFFD replacement characters (�) or other garbled Unicode.
- **Consistent character set** — don't mix thin (`─`, `│`) and thick (`━`, `┃`) box-drawing
  characters within the same diagram. Also watch for regular dashes (`-`) or pipes (`|`) mixed
  with Unicode box-drawing characters.
- **English only inside diagrams** — Vietnamese diacritical characters cause misalignment.
  The script checks for this automatically.
- **No wide Unicode arrows** — `▶`, `▼`, `→` take 2 columns in monospace. Use `>`, `v`, `->`.
  The script checks for this automatically.
- **Closing boxes** — every opened box (`┌`) must be properly closed (`┘`).

When you find a broken diagram, report the specific line numbers and describe what's wrong.
If a diagram is complex (>15 lines), suggest a corrected version when the fix isn't obvious.

### 5. Structure & MDX quality

- **Heading hierarchy** — should follow a logical progression (## → ### → ####), no skipped levels
- **Code blocks** — every code block should have a language tag (```go, ```bash, ```yaml, etc.)
- **Images** — verify `<img>` tags reference paths under `/images/<slug>/` and that the `alt`
  attribute is meaningful (not empty or generic)
- **Links** — if there are external links, flag any that look suspicious or broken patterns
- **Length** — note the approximate word count; if the post is very short (<500 words) or very
  long (>5000 words), mention it as something to consider

### 6. Readability & engagement

- **Introduction** — does the post hook the reader and explain what they'll learn?
- **Conclusion/summary** — does the post wrap up or just stop abruptly?
- **Diagrams vs text ratio** — this blog uses ASCII diagrams heavily, which is great. If a
  section has dense explanation without any visual aid, suggest where a diagram could help.
- **Practical examples** — does the post include runnable commands or real-world examples
  the reader can try?

## Output format

Present findings as a structured recommendation report. Group by dimension, lead with the
most impactful items. Use this template:

```
## Blog Review: <post title>

### Summary
<2-3 sentence overall assessment — what's good, what needs work>

### Recommendations

#### Frontmatter
- [ ] <recommendation>

#### Technical Accuracy
- [ ] <recommendation>
- [ ] ...

#### Writing Quality
- [ ] <recommendation>
- [ ] ...

#### Text Diagrams
- [ ] <recommendation with line numbers and suggested fix>
- [ ] ...

#### Structure & MDX
- [ ] <recommendation>
- [ ] ...

#### Readability & Engagement
- [ ] <recommendation>
- [ ] ...

### Highlights
<Call out 2-3 things the post does well — good reviews aren't only about problems>
```

Keep recommendations specific and actionable. Instead of "improve the introduction", say
"The introduction jumps straight into technical details — consider adding 1-2 sentences
explaining why the reader should care about this topic."

If a dimension has no issues, say "No issues found" rather than inventing nitpicks. A clean
section is a good sign, not a gap to fill.
