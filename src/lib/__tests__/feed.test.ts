import { describe, it, expect, vi } from "vitest";

import { generateFeed } from "../feed";
import type { MDXFileData } from "../blog";

vi.mock("@/config/site", () => ({
  SITE_URL: "https://example.com/",
  AUTHOR_NAME: "John Doe",
  AUTHOR_EMAIL: "john@example.com",
  AUTHOR_IMAGE_URL: "https://example.com/avatar.png",
  COPYRIGHT_YEAR: "2025",
}));

describe("generateFeed", () => {
  const mockMetadata = {
    title: "Test Blog",
    description: "A test blog",
  };

  const mockPosts: MDXFileData[] = [
    {
      slug: "test-post-1",
      metadata: {
        title: "Test Post 1",
        description: "Description for test post 1",
        date: "2024-01-15",
      },
    },
    {
      slug: "test-post-2",
      metadata: {
        title: "Test Post 2",
        description: "Description for test post 2",
        date: new Date("2024-01-20"),
      },
    },
  ];

  it("creates a feed object", () => {
    const feed = generateFeed(mockPosts, mockMetadata);
    expect(feed).toBeDefined();
  });

  it("adds all posts to the feed", () => {
    const feed = generateFeed(mockPosts, mockMetadata);
    const rssOutput = feed.rss2();
    expect(rssOutput).toContain("Test Post 1");
    expect(rssOutput).toContain("Test Post 2");
  });

  it("feed contains post descriptions", () => {
    const feed = generateFeed(mockPosts, mockMetadata);
    const rssOutput = feed.rss2();
    expect(rssOutput).toContain("Description for test post 1");
    expect(rssOutput).toContain("Description for test post 2");
  });

  it("generates valid RSS output", () => {
    const feed = generateFeed(mockPosts, mockMetadata);
    const rssOutput = feed.rss2();
    expect(rssOutput).toContain('<?xml version="1.0"');
    expect(rssOutput).toContain("<rss");
  });

  it("handles empty post array", () => {
    const feed = generateFeed([], mockMetadata);
    const rssOutput = feed.rss2();
    expect(rssOutput).toContain("Test Blog");
    expect(rssOutput).toContain("A test blog");
  });

  it("returns feed with correct config data", () => {
    const feed = generateFeed(mockPosts, mockMetadata);
    const rssOutput = feed.rss2();

    expect(rssOutput).toContain("<title>Test Blog</title>");
    expect(rssOutput).toContain("<description>A test blog</description>");
    expect(rssOutput).toContain("All rights reserved 2025, John Doe");
    expect(rssOutput).toContain("Feed for Node.js");
    expect(rssOutput).toContain("https://example.com/avatar.png");
  });
});
