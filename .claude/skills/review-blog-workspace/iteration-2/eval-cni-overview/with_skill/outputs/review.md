## Blog Review: Understanding Kubernetes CNI: How Pods Get Their Network

### Summary

This is a well-structured overview post that covers CNI fundamentals, GKE and AWS EKS networking approaches, security groups, CNI comparison, and performance benchmarking. The writing is clear and the comparison tables are effective. The post is light on ASCII diagrams (only two simple text blocks), relying mostly on images, so diagram formatting risk is low. The main areas for improvement are minor technical clarifications and a few structural items.

### Recommendations

#### Frontmatter
- [ ] No issues found. Title, description, and date (2026-04-04) are all present and valid.

#### Technical Accuracy
- [ ] **Line 70**: The claim "~254 Pod IPs per node" for a `/24` range is slightly off -- a `/24` gives 256 addresses, but usable host IPs are typically 254. In Kubernetes pod CIDR context, all 256 may be assignable since there is no broadcast/network address concern at the pod level. Consider clarifying that it is "up to 256 addresses" or keeping "~254" but noting why.
- [ ] **Lines 164-171**: The Max Pods formula `(So ENI toi da) x (So IP moi ENI - 1)` is correct (the `-1` accounts for the primary IP on each ENI). However, in the default VPC CNI configuration, the first ENI's primary IP is used for the node itself, so the actual default formula used by AWS is `(Max ENIs * (IPs per ENI - 1)) + 2`. The `+2` accounts for host networking pods (kube-proxy, aws-node). Worth double-checking against current AWS documentation and noting this nuance if desired.
- [ ] **Line 205**: `ENABLE_POD_ENI=true` is the legacy environment variable. As of VPC CNI v1.15+, AWS recommends using `POD_SECURITY_GROUP_ENFORCING_MODE` and the `enable-windows-prefix-delegation` or the newer `SecurityGroupPolicy` approach without explicitly setting `ENABLE_POD_ENI`. Worth double-checking whether this flag is still the recommended activation method.
- [ ] **Line 262**: The claim "Cilium + eBPF: Thay the hoan toan kube-proxy, performance cao nhat" is a reasonable generalization but oversimplified -- Cilium can replace kube-proxy but does not always yield the highest performance in all scenarios (e.g., single-stream TCP). Consider adding "trong da so truong hop" (in most cases).

#### Writing Quality
- [ ] The post maintains a consistent informal Vietnamese style throughout -- no tone-switching issues detected.
- [ ] **Line 43**: "Agents tren node (kubelet, system daemons) co the giao tiep voi tat ca Pod tren node do" -- this is the third requirement of the Kubernetes networking model, but the original model actually has four requirements (the third is about agents, the fourth about Services). Consider whether you want to list all four or note that this is a simplified list.
- [ ] **Section balance**: The "CNI Performance Benchmarking" section (lines 249-264) is noticeably thinner than other sections -- it mostly lists methodology steps and links to an external article. Consider either expanding with a brief summary of key benchmark results (e.g., "Cilium eBPF mode dat ~38 Gbps, Calico iptables dat ~35 Gbps") or merging it into the comparison table section to avoid a section that feels like a stub.

#### Text Diagrams
- [ ] **Lines 143-155 (Pod Network Namespace diagram)**: The diagram uses classic ASCII box-drawing characters (`+`, `-`, `|`) consistently. Border alignment is correct -- the top and bottom borders are both 38 characters wide and corners align. No corrupted characters detected. No issues found.
- [ ] **Lines 163-171 (Max Pods calculation)**: This is a plain text block, not a bordered diagram. Formatting is clean with consistent indentation. No issues found.
- [ ] **General observation**: The post has only two text-based diagrams and relies heavily on `<img>` tags for visual content (10 images total). This is fine, but it means the post's visual quality depends entirely on the referenced image files being correct and present. There is no way to verify image content from the MDX source alone.

#### Structure & MDX
- [ ] **Heading hierarchy**: The post uses `##` -> `###` properly throughout. No skipped levels. Good.
- [ ] **Code blocks**: All code blocks have language tags (`text`, `yaml`). However, the two `text` blocks (lines 143 and 163) could arguably use no language tag or keep `text` -- this is acceptable.
- [ ] **Images**: All 10 `<img>` tags reference paths under `/images/kubernetes-cni-overview/` and all have descriptive `alt` attributes. Good.
- [ ] **Links**: Internal links (`/blog/container-networking-from-scratch`, `/blog/aws-vpc-cni-deep-dive`) and external links (kubernetes.io, cni.dev, cloud.google.com, github.com/aws, docs.cilium.io, itnext.io) all appear well-formed. No broken patterns detected.
- [ ] **Word count**: Approximately 800-900 words of Vietnamese/English prose (excluding code blocks and tables). This is on the shorter side but appropriate for an overview post that uses tables and images heavily.
- [ ] **Line 105**: The blockquote "VPC-Native mode khong co nhuoc diem so voi Routes-Based" is a strong absolute claim. VPC-Native does consume more IP address space from VPC secondary ranges, which could be a concern in IP-constrained environments. Consider softening to "hau nhu khong co nhuoc diem" (almost no downsides).

#### Readability & Engagement
- [ ] **Introduction**: The post opens by defining CNI clearly and immediately scoping what it does and does not cover. This is effective, though it could benefit from one sentence explaining why a DevOps engineer should understand CNI (e.g., "Hieu CNI giup ban debug network issues va chon dung networking solution cho cluster cua ban").
- [ ] **Conclusion/summary**: The "Tong ket" section provides a good summary table and links to related posts. It does not feel abrupt.
- [ ] **Practical examples**: The post includes one YAML example (SecurityGroupPolicy CRD) and two text diagrams showing network configuration. The GKE sections lack runnable examples -- consider adding a `gcloud` command showing how to create a VPC-native cluster, e.g., `gcloud container clusters create --enable-ip-alias`.
- [ ] **Cross-reference**: Line 157 nicely links back to the "Container Networking from Scratch" post, connecting theory to hands-on practice. This is a strong engagement technique.

### Highlights

- The comparison tables (lines 97-103, 239-247, 268-276) are well-constructed and make it easy to scan differences between approaches -- this is the post's strongest feature.
- The cross-reference to the "Container Networking from Scratch" post at line 157 creates a compelling learning path and gives the reader motivation to explore hands-on content.
- The visual layout with centered images and logos is clean and professional, giving the post a polished feel despite being primarily a technical overview.
