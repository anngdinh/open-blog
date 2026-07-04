import "@/styles/globals.css";

import type { ReactNode } from "react";
import type { Metadata } from "next";
import { ViewTransitions } from "next-view-transitions";
import { Analytics } from "@vercel/analytics/next";

import { sans } from "@/config/fonts";
import {
  SITE_URL,
  SITE_NAME,
  SITE_DESCRIPTION,
  AUTHOR_NAME,
  TWITTER_HANDLE,
} from "@/config/site";
import { clx } from "@/lib/utils";

import Header from "../components/header";
import Footer from "../components/footer";

const titleTemplate = `%s | ${AUTHOR_NAME}`;
const defaultTitle = `${SITE_NAME} — A blog by ${AUTHOR_NAME}`;

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  alternates: {
    canonical: "/",
    types: {
      "application/atom+xml": `${SITE_URL}atom.xml`,
      "application/rss+xml": `${SITE_URL}rss.xml`,
    },
  },
  title: {
    default: defaultTitle,
    template: titleTemplate,
  },
  description: SITE_DESCRIPTION,
  openGraph: {
    title: defaultTitle,
    description: SITE_DESCRIPTION,
    url: SITE_URL,
    siteName: SITE_NAME,
    locale: "en_US",
    type: "website",
    images: [`${SITE_URL}og/home`],
  },
  robots: {
    index: true,
    follow: true,
    "max-video-preview": -1,
    "max-image-preview": "large",
    "max-snippet": -1,
  },
  twitter: {
    title: SITE_NAME,
    card: "summary_large_image",
    creator: TWITTER_HANDLE || undefined,
  },
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <ViewTransitions>
      <html
        lang="en"
        className={clx(
          "bg bg-neutral-100 text-black dark:bg-neutral-950 dark:text-white",
          sans.className,
        )}
      >
        <body className="mx-auto flex min-h-dvh max-w-2xl flex-col bg-[--bg] px-5 py-12 text-[--text]">
          <Header />
          <main className="flex-grow">{children}</main>
          <Footer />
          <Analytics />
        </body>
      </html>
    </ViewTransitions>
  );
}
