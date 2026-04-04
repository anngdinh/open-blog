## Blog Review: Understanding Kubernetes CNI: How Pods Get Their Network

### Summary

This is a well-structured, informative overview of Kubernetes CNI that covers GKE, AWS EKS, and popular CNI plugins with good visual diagrams. The main issues are **missing SEO/metadata components** (no `generateBlogMetadata`, `BlogJsonLd`, or `Title` imports compared to other posts), and several corrupted characters in the ASCII diagrams that will render as garbage in the browser. The technical content is solid and the comparison tables are useful.

### Recommendations

#### Frontmatter & Metadata
- [ ] **Add `generateBlogMetadata` import and export** -- the post is missing `import { generateBlogMetadata } from "../../../lib/blog"` and the corresponding `export const metadata = generateBlogMetadata({...})` block. Compare with `clean-architecture/page.mdx` which includes this.
- [ ] **Add `BlogJsonLd` component** -- required for structured data / SEO. The `clean-architecture` post includes `<BlogJsonLd ... />` after the metadata export.
- [ ] **Add `Title` component** -- the `clean-architecture` post uses `<Title title={metadata.title} date={metadata.date} />` to render the post header consistently. This post jumps straight into `## CNI la gi?` without a title component.
- [ ] The `title` (55 chars) and `description` (144 chars) lengths are fine for SEO.

#### Technical Accuracy
- [ ] The max pods formula `(So ENI toi da) x (So IP moi ENI - 1)` is correct for the default VPC CNI configuration but does not account for **prefix delegation mode** (`ENABLE_PREFIX_DELEGATION=true`), which significantly increases pod density. Consider adding a brief note mentioning this option exists, since it has been available since VPC CNI v1.9 and is commonly used.
- [ ] The statement "VPC-Native mode khong co nhuoc diem so voi Routes-Based" is slightly strong. VPC-Native requires more IP address planning upfront (secondary ranges must be sized correctly). Consider softening to "VPC-Native has very few downsides" or noting the IP planning requirement.
- [ ] The Calico row in the comparison table lists the data plane as "iptables / eBPF" -- Calico also supports a pure Linux routing data plane (BGP + no overlay). Worth mentioning since that is one of Calico's distinguishing features.
- [ ] The benchmarking section references a 2024 article. The benchmark protocol diagram is useful but contains no actual numbers or results -- consider either summarizing key findings from the linked benchmark or noting that readers should check the link for actual numbers.

#### Writing Quality
- [ ] The post maintains a consistent, clear semi-formal Vietnamese style throughout -- no issues with tone switching.
- [ ] The section "Security Groups cho Pods" could benefit from a brief introductory sentence explaining *why* pod-level security matters before jumping into GKE vs AWS implementations.
- [ ] The "CNI Performance Benchmarking" section feels lighter than the others. It presents a methodology and some general claims ("Cilium + eBPF: bypass kube-proxy, rat nhanh") without data. Either expand with a summary of actual results or trim to a shorter "further reading" note.

#### Structure & MDX
- [ ] **Corrupted Unicode characters in ASCII diagrams** -- multiple lines contain replacement characters (U+FFFD, displayed as `?` or diamond-question-mark) that break the visual layout. Affected diagrams: the Routes-Based diagram (lines ~64, 78), the AWS VPC architecture diagram (lines ~156-172), the Firewall Rule diagram (line ~238), the Trunk ENI diagram (lines ~257-259), the Benchmark diagram (line ~337), and the summary tree (lines ~366, 370). These must be fixed -- they will render as broken characters in the browser.
- [ ] All code blocks have appropriate language tags (`text`, `yaml`) -- good.
- [ ] Heading hierarchy is clean: `##` for major sections, `###` for subsections -- no skipped levels.
- [ ] Image `alt` attributes are descriptive and meaningful (e.g., "CNI Architecture - Orchestrator, CNI Library, Plugins") -- good.
- [ ] The post is approximately 1,500-2,000 words (excluding diagrams), which is a good length for this topic.

#### Readability & Engagement
- [ ] The introduction is functional but could be stronger. It defines CNI but does not explain *why a reader should care* about understanding CNI. Consider adding 1-2 sentences about how CNI choice affects cluster performance, security, and operational complexity before diving into the definition.
- [ ] The "Tong ket" section with the summary tree diagram is a nice touch. However, there is no concluding paragraph that ties the post together or offers guidance on how to choose a CNI. A brief "when to pick what" recommendation would be very valuable.
- [ ] The cross-references to other blog posts ("Container Networking from Scratch", "AWS VPC CNI Deep Dive") are well placed and encourage readers to continue learning -- good internal linking.
- [ ] The comparison table in "So sanh cac CNI pho bien" is one of the most useful parts of the post. Consider making it more prominent or adding a sentence directing readers to it as a quick-reference.

### Highlights

1. **Excellent use of ASCII diagrams** -- the post includes diagrams for nearly every major concept (Routes-Based networking, VPC-Native, AWS ENI architecture, pod networking, trunk ENI, benchmarking methodology, and a summary tree). This is the blog's signature style and it works very well here.
2. **Strong comparative structure** -- the GKE vs AWS EKS framing, the Routes-Based vs VPC-Native table, and the CNI comparison table give readers practical decision-making context, not just theory.
3. **Good internal linking** -- the callout connecting VPC CNI's `/32` + link-local pattern back to the "Container Networking from Scratch" post rewards readers who follow the series and reinforces learning.
