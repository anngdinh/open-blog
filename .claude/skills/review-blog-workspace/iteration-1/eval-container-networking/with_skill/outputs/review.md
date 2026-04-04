## Blog Review: Container Networking from Scratch: Hands-On Guide

### Summary

This is an excellent hands-on tutorial that progressively builds container networking concepts from veth pairs up to CNI plugins and advanced Docker networking techniques. The technical content is accurate, well-structured, and includes runnable commands at every step. The main gaps are missing SEO/metadata components (compared to other blog posts in the project) and a few minor technical and editorial items.

### Recommendations

#### Frontmatter & Metadata
- [ ] **Missing `generateBlogMetadata` import and export.** The clean-architecture post imports `generateBlogMetadata` from `../../../lib/blog` and exports `metadata`. This post has none of that, which means it will lack proper Open Graph tags, canonical URL, and other SEO metadata.
- [ ] **Missing `BlogJsonLd` component.** The clean-architecture post includes a `<BlogJsonLd>` component for structured data (JSON-LD). Adding this improves search engine understanding of the article.
- [ ] **Missing `Title` component.** The clean-architecture post uses `<Title title={metadata.title} date={metadata.date} />` to render the post header consistently. This post relies only on markdown headings.
- [ ] **Description length is borderline.** The `description` field is approximately 145 characters in Vietnamese, which is fine but close to the 160-character SEO limit. No action needed, just be aware if you edit it.

#### Technical Accuracy
- [ ] **CNI plugins version v1.5.0**: As of early 2026, the latest CNI plugins release may be newer than v1.5.0 (released mid-2024). Worth double-checking the latest version at https://github.com/containernetworking/plugins/releases and updating the download URL if a newer stable release is available.
- [ ] **`iptables -P FORWARD ACCEPT` is overly permissive.** In sections 2 and 4, the post sets the default FORWARD policy to ACCEPT. This is fine for a learning exercise, but a brief note warning readers not to do this in production would be valuable, since it disables all firewall filtering on forwarded traffic.
- [ ] **Section 6.1: `host_ip` extraction may produce empty result.** The command `ip -4 addr show veth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'` will return empty if veth0 has no IP assigned (and in this section, no IP is explicitly assigned to veth0). The comment suggests using the host's real IP as a fallback, but the flow could confuse readers. Consider either assigning an IP to veth0 explicitly or clarifying what IP to use and why.
- [ ] **Section 4 uses a hardcoded IP `192.168.56.12`.** This is fine as an example, but a brief note telling readers to replace it with their own host IP would help avoid confusion when reproducing.
- [ ] **`CNI_PATH` usage**: The `CNI_PATH` environment variable is set but the CNI bridge binary is invoked directly as `./cni-bin/bridge`. The `CNI_PATH` variable is used by some CNI libraries for plugin chaining/delegation -- the current usage is correct for a single plugin call, but worth noting that in a real CNI setup `CNI_PATH` is used to locate the binary by name.

#### Writing Quality
- [ ] **Consistent use of bold for key terms.** The post does a good job bolding key terms in most places, but some important terms like "IPAM", "SNAT", "Layer 2" are not bolded on first use. Minor consistency improvement.
- [ ] **Section 6 title says "Ky thuat nang cao" (advanced techniques) but section 6.1 is actually more of a workaround than an advanced technique.** Consider renaming 6.1 to something like "Understanding Docker's hidden namespaces" to better reflect what it teaches.
- [ ] **The variable name `ndIP` in section 6.2 is unclear.** It likely stands for "secondary IP" but `secondaryIP` or `podIP` would be more readable and self-documenting.
- [ ] **No issues with grammar or typos** -- the Vietnamese text reads naturally and technical English terms are used correctly throughout.

#### Structure & MDX
- [ ] **All code blocks have language tags** -- good, no issues found.
- [ ] **ASCII diagrams render correctly** -- the box-drawing characters are well-aligned and consistent across all diagrams.
- [ ] **Post starts with `##` headings instead of using a `#` top-level heading.** Other posts in the project (e.g., clean-architecture) use a `# Title` heading rendered via the `<Title>` component. If the metadata components are added, this would naturally be addressed.
- [ ] **Approximate word count: ~2,500 words** (excluding code blocks). This is a healthy length for a tutorial post -- thorough but not excessive.
- [ ] **External links at the bottom all point to legitimate, well-known sources** (cni.dev, kubernetes.io, itnext.io). No issues found.

#### Readability & Engagement
- [ ] **The introduction is effective** -- it hooks the reader with a question, sets expectations, and shows the learning roadmap upfront as an ASCII diagram. No changes needed.
- [ ] **The conclusion/summary section is strong** -- the stacked diagram showing the full networking stack and the Kubernetes mapping table tie everything together well.
- [ ] **Consider adding a brief "Prerequisites" note** at the top specifying that readers need a Linux machine (or VM) with root access, `jq` installed, and Docker installed for sections 5-6. This avoids frustration mid-tutorial.
- [ ] **Section 2 could benefit from a brief diagram showing the routing path.** The text says "traffic di: netns1 -> host (forward) -> netns2" but a small ASCII diagram showing the packet flow through the host would reinforce the concept visually.

### Highlights

1. **Progressive complexity is masterfully done.** Each section builds directly on the previous one, and the post explicitly calls out what is new ("day la diem khac biet!"). The reader never feels lost because the foundation was laid in earlier sections.

2. **Every section includes cleanup commands.** This is a detail many tutorials skip, but it is essential for a hands-on guide where readers are running commands on real systems. Excellent practice.

3. **The bridge between theory and real-world tools is clear.** The post consistently maps low-level concepts to their real-world counterparts (bridge = docker0, DNAT = NodePort, /32 + link-local = AWS VPC CNI). The summary table at the end reinforces this mapping perfectly.
