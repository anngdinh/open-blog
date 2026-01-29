import type { ReactNode, AnchorHTMLAttributes } from "react";
import { describe, it, expect, vi } from "vitest";

import { render, screen } from "@testing-library/react";

import Footer from "../footer";

// Mock the next-view-transitions Link component
vi.mock("next-view-transitions", () => ({
  Link: ({
    children,
    href,
    ...props
  }: AnchorHTMLAttributes<HTMLAnchorElement> & {
    href: string;
    children: ReactNode;
  }) => (
    <a href={href} {...props}>
      {children}
    </a>
  ),
}));

vi.mock("@/config/site", () => ({
  AUTHOR_NAME: "John Doe",
  AUTHOR_IMAGE_URL: "https://example.com/avatar.png",
  GITHUB_URL: "https://github.com/johndoe",
  LINKEDIN_URL: "https://linkedin.com/in/johndoe",
}));

describe("Footer", () => {
  it("renders footer element", () => {
    render(<Footer />);
    const footer = screen.getByRole("contentinfo");
    expect(footer).toBeDefined();
  });

  it("renders github link when GITHUB_URL is set", () => {
    render(<Footer />);
    const githubLink = screen.getByText("github");
    expect(githubLink).toBeDefined();
    expect(githubLink.getAttribute("href")).toBe("https://github.com/johndoe");
  });

  it("renders linkedin link when LINKEDIN_URL is set", () => {
    render(<Footer />);
    const linkedinLink = screen.getByText("linkedin");
    expect(linkedinLink).toBeDefined();
    expect(linkedinLink.getAttribute("href")).toBe(
      "https://linkedin.com/in/johndoe",
    );
  });

  it("links open in new tab", () => {
    render(<Footer />);
    const links = screen.getAllByRole("link");
    links.forEach((link) => {
      expect(link.getAttribute("target")).toBe("_blank");
      expect(link.getAttribute("rel")).toBe("noopener noreferrer nofollow");
    });
  });
});
