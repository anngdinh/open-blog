import { describe, it, expect, vi } from "vitest";

import { render, screen } from "@testing-library/react";

import Header from "../header";
import type { AnchorHTMLAttributes, ReactNode } from "react";

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
}));

describe("Header", () => {
  it("renders header element", () => {
    render(<Header />);
    const header = screen.getByRole("banner");
    expect(header).toBeDefined();
  });

  it("renders blog link to home page", () => {
    render(<Header />);
    const homeLink = screen.getByText("blog");
    expect(homeLink).toBeDefined();
    expect(homeLink.getAttribute("href")).toBe("/");
  });

  it("renders author link with GitHub URL when both author image and GitHub URL exist", () => {
    render(<Header />);
    const links = screen.getAllByRole("link");
    const authorLink = links.find((link) =>
      link.getAttribute("href")?.includes("github.com"),
    );
    expect(authorLink?.getAttribute("href")).toBe("https://github.com/johndoe");
  });

  it("renders author avatar image with correct attributes", () => {
    render(<Header />);
    const img = screen.getByRole("img");
    expect(img).toBeDefined();
    expect(img.getAttribute("src")).toBe("https://example.com/avatar.png");
    expect(img.getAttribute("loading")).toBe("eager");
  });

  it("author link opens in new tab", () => {
    render(<Header />);
    const links = screen.getAllByRole("link");
    const githubLink = links.find((link) =>
      link.getAttribute("href")?.includes("github.com"),
    );
    expect(githubLink?.getAttribute("target")).toBe("_blank");
    expect(githubLink?.getAttribute("rel")).toBe(
      "noopener noreferrer nofollow",
    );
  });
});
