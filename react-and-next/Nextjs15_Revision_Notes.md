# Next.js 15 — Complete Revision Notes

> Condensed, code-first revision notes based on a full Next.js 15 (App Router) course.
> Covers: fundamentals → routing → layouts → rendering → data fetching/mutations → auth (Clerk) → deployment.

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Setup & Project Structure](#2-setup--project-structure)
3. [React Server Components (RSC) Basics](#3-react-server-components-rsc-basics)
4. [Routing Fundamentals](#4-routing-fundamentals)
5. [Dynamic, Nested-Dynamic & Catch-all Routes](#5-dynamic-nested-dynamic--catch-all-routes)
6. [Custom 404 / notFound()](#6-custom-404--notfound)
7. [File Colocation, Private Folders, Route Groups](#7-file-colocation-private-folders-route-groups)
8. [Layouts](#8-layouts)
9. [Metadata & SEO](#9-metadata--seo)
10. [Linking & Navigation](#10-linking--navigation)
11. [Special Files: template, loading, error](#11-special-files-template-loading-error)
12. [Parallel Routes](#12-parallel-routes)
13. [Conditional Routes](#13-conditional-routes)
14. [Intercepting Routes](#14-intercepting-routes)
15. [Route Handlers (API Routes)](#15-route-handlers-api-routes)
16. [Middleware](#16-middleware)
17. [Rendering: CSR, SSR, Hydration, RSC](#17-rendering-csr-ssr-hydration-rsc)
18. [Static, Dynamic & Streaming Rendering](#18-static-dynamic--streaming-rendering)
19. [Server / Client Component Composition Patterns](#19-server--client-component-composition-patterns)
20. [Data Fetching](#20-data-fetching)
21. [Data Mutations & Server Actions](#21-data-mutations--server-actions)
22. [Authentication with Clerk](#22-authentication-with-clerk)
23. [Deployment (Vercel)](#23-deployment-vercel)
24. [Quick-Reference Cheat Sheet](#24-quick-reference-cheat-sheet)

---

## 1. Introduction

**What is Next.js?**
- Next.js is a **React framework** for building full-stack, production-ready web apps.
- React itself is only a UI library (the "view" layer). It doesn't ship routing, data fetching, bundling, compiling, etc.
- Next.js adds all of this **out of the box**, following strong conventions built from years of production React experience.

**Key features:**
| Feature | Benefit |
|---|---|
| File-based routing | No manual router config |
| API routes (Route Handlers) | Full-stack in one project |
| Rendering flexibility | SSR + CSR + Static, mix per route |
| Built-in async/await data fetching | No extra data-fetching library required |
| Flexible styling | CSS Modules, Tailwind, CSS-in-JS |
| Image / font / script optimization | Better Core Web Vitals |
| Optimized dev & prod build system | Zero-config bundling |

**Prerequisites:** HTML, CSS, JavaScript, and core React concepts (function components, props, state, JSX, hooks).

**Node requirement:** Node.js **v18.18+**.

---

## 2. Setup & Project Structure

### Create a new app
```bash
npx create-next-app@latest
```
Prompts (recommended answers used throughout the course):
- Project name → e.g. `hello-world`
- TypeScript → **Yes**
- ESLint → **Yes**
- Tailwind CSS → **Yes**
- `src/` directory → **Yes**
- App Router → **Yes**
- Turbopack → optional (stable in v15, course opts out)
- Custom import alias → keep default (`@/*`)

### Run it
```bash
cd hello-world
npm run dev     # http://localhost:3000
```

### Folder/file structure
```
hello-world/
├── node_modules/        # installed deps (gitignored)
├── .next/                # build output, created by dev/build (gitignored)
├── public/                # static assets (images, svgs, etc.)
├── src/
│   └── app/                # the App Router — most of your time is spent here
│       ├── favicon.ico
│       ├── globals.css
│       ├── layout.tsx     # ROOT layout — required, wraps everything
│       └── page.tsx       # maps to "/" (homepage)
├── package.json           # deps + scripts (dev/build/start/lint)
├── next.config.ts
├── tsconfig.json
├── eslint.config.js
└── tailwind.config.ts
```

**How rendering starts:**
`npm run dev` → executes `package.json` → renders `layout.tsx` (root layout) → for `/`, finds `page.tsx` in `app/` → renders that component as `children` inside the root layout.

---

## 3. React Server Components (RSC) Basics

React Server Components introduce **two types of components**:

| | Server Component (default) | Client Component |
|---|---|---|
| Where it runs | On the server | In the browser (also SSR'd first) |
| Can read files / hit DB directly | ✅ | ❌ |
| Can use hooks (`useState`, `useEffect`...) | ❌ | ✅ |
| Can handle browser events (`onClick`...) | ❌ | ✅ |
| How to opt in | default — nothing needed | add `"use client"` at top of file |

```tsx
"use client";
// now this file (and everything it imports) is a Client Component
```

**Rule of thumb:** Next.js treats **every component as a Server Component by default**. You only add `"use client"` when you need interactivity, hooks, or browser-only APIs.

---

## 4. Routing Fundamentals

Next.js uses **file-system based routing**. Three conventions:

1. All routes live inside the `app/` folder.
2. A route file must be named `page.tsx` (or `page.js`).
3. Each **folder** represents a URL **segment**.

### Root route
```tsx
// app/page.tsx
export default function Home() {
  return <h1>Welcome home</h1>;
}
```
→ maps to `/`

### Simple nested routes
```tsx
// app/about/page.tsx  → "/about"
export default function About() {
  return <h1>About me</h1>;
}

// app/profile/page.tsx → "/profile"
export default function Profile() {
  return <h1>My profile</h1>;
}
```

### Deeper nested routes
```
app/blog/page.tsx          → /blog
app/blog/first/page.tsx    → /blog/first
app/blog/second/page.tsx   → /blog/second
```

- Visiting a URL with **no matching folder/page.tsx** (e.g. `/dashboard` with nothing defined) automatically returns a **404** — no extra code needed.
- **Favoring convention over configuration**: no router library to install/configure.

---

## 5. Dynamic, Nested-Dynamic & Catch-all Routes

### Dynamic segments — `[param]`
Instead of creating a folder per product, use square brackets:
```
app/products/page.tsx           → /products (list)
app/products/[productId]/page.tsx → /products/1, /products/2, /products/100 ...
```
```tsx
// app/products/[productId]/page.tsx
type Props = { params: Promise<{ productId: string }> };

export default async function ProductDetails({ params }: Props) {
  const { productId } = await params;
  return <h1>Details about product {productId}</h1>;
}
```
> In the App Router, `params` (and `searchParams`) are **Promises** — you must `await` them inside an `async` Server Component.

### Nested dynamic segments
```
app/products/[productId]/reviews/[reviewId]/page.tsx
```
```tsx
type Props = {
  params: Promise<{ productId: string; reviewId: string }>;
};

export default async function ReviewDetails({ params }: Props) {
  const { productId, reviewId } = await params;
  return <h1>Review {reviewId} for product {productId}</h1>;
}
```

### Catch-all segments — `[...slug]`
Handles **any number** of path segments with one file. Great for docs sites.
```
app/docs/[...slug]/page.tsx
```
matches `/docs/feature1`, `/docs/feature1/concept1`, `/docs/feature1/concept1/example1`, etc.
```tsx
type Props = { params: Promise<{ slug?: string[] }> };

export default async function Docs({ params }: Props) {
  const { slug } = await params;

  if (slug?.length === 2) {
    return <h1>Viewing docs for feature {slug[0]}, concept {slug[1]}</h1>;
  } else if (slug?.length === 1) {
    return <h1>Viewing docs for feature {slug[0]}</h1>;
  }
  return <h1>Docs homepage</h1>;
}
```
Visiting bare `/docs` (no slug at all) → **404** unless you use an **optional catch-all**.

### Optional catch-all — `[[...slug]]`
```
app/docs/[[...slug]]/page.tsx
```
Same as catch-all, but also matches the parent route itself (`/docs`).

**When to use which:**
- Same UI regardless of URL → plain `page.tsx` in the folder.
- Different UI per URL depth → catch-all / optional catch-all route.

---

## 6. Custom 404 / notFound()

### Global custom 404 page
```tsx
// app/not-found.tsx  (file name must be exactly this)
export default function NotFound() {
  return (
    <div>
      <h2>Page Not Found</h2>
      <p>Could not find requested resource</p>
    </div>
  );
}
```

### Programmatic 404 with `notFound()`
```tsx
import { notFound } from "next/navigation";

export default async function ReviewDetails({ params }: Props) {
  const { reviewId } = await params;
  if (parseInt(reviewId) > 1000) {
    notFound();
  }
  // ...
}
```

### Segment-specific not-found pages
Place another `not-found.tsx` inside a nested folder (e.g. `reviews/[reviewId]/not-found.tsx`) — Next.js uses the **most specific** `not-found.tsx` it finds.

> `not-found.tsx` does **not** accept props. To customize the message dynamically, use the `usePathname` hook — but that requires `"use client"` since hooks only work in Client Components.
```tsx
"use client";
import { usePathname } from "next/navigation";

export default function NotFound() {
  const pathname = usePathname();
  const productId = pathname.split("/")[2];
  const reviewId = pathname.split("/")[4];
  return <h1>Review {reviewId} not found for product {productId}</h1>;
}
```

### `redirect()` (as an alternative to notFound)
```tsx
import { redirect } from "next/navigation";

if (parseInt(reviewId) > 1000) {
  redirect("/products");
}
```

---

## 7. File Colocation, Private Folders, Route Groups

### File colocation
You can freely place non-route files (components, utils, charts) inside any folder in `app/` — a folder only becomes a **public route** once it has a `page.tsx`.
```
app/dashboard/
  ├── LineChart.tsx     ← NOT a route (no page.tsx alongside... unless...)
  └── page.tsx          ← THIS makes /dashboard accessible
```
Only the **default export of `page.tsx`** is served; other collocated files are invisible to the router.

### Private folders — `_folderName`
Prefix a folder with `_` to exclude it (and all subfolders) from routing.
```
app/_lib/formatDate.ts   → NOT routable, /​_lib is a 404
```
Use cases: separate UI logic from routing logic, organize internal utilities, avoid future naming collisions with Next.js conventions.
> Pro tip: to have a literal underscore in a URL segment, use `%5F` (URL-encoded underscore).

### Route groups — `(folderName)`
Wrap a folder name in parentheses to **organize routes/files without affecting the URL**.
```
app/(auth)/register/page.tsx   → /register   (NOT /auth/register)
app/(auth)/login/page.tsx      → /login
app/(auth)/forgot-password/page.tsx → /forgot-password
```
- Route groups are the **only way** to share a layout between routes **without** affecting the URL.
- Can be nested inside each other for more organization.

---

## 8. Layouts

A layout is **UI shared across multiple pages**. Export a default React component from `layout.tsx`, accepting a `children` prop.

### Root layout (mandatory)
Every app must have `app/layout.tsx`. If deleted, Next.js **regenerates it automatically**.
```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header style={{ background: "lightblue", padding: "1rem" }}>
          <p>Header</p>
        </header>
        {children}
        <footer style={{ background: "whitesmoke", padding: "1rem" }}>
          <p>Footer</p>
        </footer>
      </body>
    </html>
  );
}
```
The header/footer persist across every route — only `children` (the matched `page.tsx`) changes.

### Nested layouts
Add a `layout.tsx` inside any subfolder to create a layout scoped to that segment and its children.
```tsx
// app/products/[productId]/layout.tsx
export default function ProductDetailsLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <h2>Featured Products</h2>
    </>
  );
}
```
Render order for `/products/1`: RootLayout → (children = ProductsIdLayout) → (children = page.tsx content).

### Excluding header/footer from certain pages (multiple root layouts)
Route groups let you define **separate root layouts** for different sections (e.g. auth pages vs the main app) — each route group folder gets its own `layout.tsx` containing its own `<html>`/`<body>`, so pages like login/register don't inherit the main header/footer.

---

## 9. Metadata & SEO

Two ways to set metadata from `layout.tsx` or `page.tsx`:

### Static metadata object
```tsx
// app/about/page.tsx
export const metadata = {
  title: "About | Code Evolution",
};
```
- Both layout and page can export metadata; **page metadata wins** for overlapping keys.
- Metadata **merges** top-down (root → nested); deeper segments override shallower ones for matching fields.
- You **cannot** use both `metadata` object and `generateMetadata` in the **same** segment — pick one.

### Dynamic metadata — `generateMetadata`
```tsx
import type { Metadata } from "next";

type Props = { params: Promise<{ productId: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { productId } = await params;
  // could fetch real data here
  return { title: `Product ${productId}` };
}
```

### Metadata + Client Components
`metadata`/`generateMetadata` **cannot** be exported from a file marked `"use client"`. Fix: extract the interactive logic into its **own** client component and keep `page.tsx` as a Server Component that only exports metadata + renders the client component.
```tsx
// app/counter/Counter.tsx
"use client";
export function Counter() { /* useState, onClick, etc. */ }

// app/counter/page.tsx
export const metadata = { title: "Counter" };
import { Counter } from "./Counter";
export default function Page() { return <Counter />; }
```

### Advanced `title` field (object form)
```tsx
// app/layout.tsx
export const metadata: Metadata = {
  title: {
    default: "Next.js Tutorial - Code Evolution", // fallback if child has none
    template: "%s | Code Evolution",              // wraps child titles
  },
};

// app/blog/page.tsx
export const metadata = { title: "Blog" }; // → "Blog | Code Evolution"

// To break out of the template entirely:
export const metadata = { title: { absolute: "Blog" } }; // → just "Blog"
```

---

## 10. Linking & Navigation

### `<Link>` component (declarative, client-side navigation)
```tsx
import Link from "next/link";
<Link href="/about">About</Link>
```

### `useRouter` (programmatic navigation — client components only)
```tsx
"use client";
import { useRouter } from "next/navigation";

export default function OrderProduct() {
  const router = useRouter();
  const handleClick = () => {
    console.log("placing your order");
    router.push("/");       // navigate, adds history entry
    // router.replace("/"); // navigate, replaces current history entry
    // router.back();
    // router.forward();
  };
  return <button onClick={handleClick}>Place order</button>;
}
```

### `redirect()` (server-side / server actions)
```tsx
import { redirect } from "next/navigation";
redirect("/products");
```

### `params` and `searchParams`
- `params` → dynamic route segment values (e.g. `[productId]`).
- `searchParams` → query string values (`?query=...`), available as a `Promise` on `page.tsx`.
```tsx
type Props = { searchParams: Promise<{ query?: string }> };
export default async function ProductsDBPage({ searchParams }: Props) {
  const { query } = await searchParams;
  const products = await getProducts(query);
  // ...
}
```

---

## 11. Special Files: template, loading, error

### `template.tsx`
Like `layout.tsx` but **remounts on every navigation** (fresh component instance, state reset, effects re-run). Use for enter/exit animations or per-navigation effects. Both `layout.tsx` and `template.tsx` can coexist — layout renders first, then template.

```tsx
// app/(auth)/template.tsx
"use client";
import { useState } from "react";
export default function AuthTemplate({ children }: { children: React.ReactNode }) {
  const [input, setInput] = useState("");
  return (
    <>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      {children}
    </>
  );
}
```
(With `layout.tsx`, input state persists across `/register` ↔ `/login`. With `template.tsx`, it resets on every navigation.)

### `loading.tsx`
Automatically wraps `page.tsx` and nested children in a **React Suspense boundary** — shown instantly during navigation.
```tsx
// app/blog/loading.tsx
export default function Loading() {
  return <h1>Loading...</h1>;
}
```
Benefits: instant feedback on navigation, and shared layouts stay interactive while content loads.

### `error.tsx`
Automatically wraps the segment in a **React Error Boundary**. **Must be a Client Component.**
```tsx
// app/products/[productId]/reviews/[reviewId]/error.tsx
"use client";
export default function ErrorBoundary({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```
- `error` prop → the thrown error (`error.message`).
- `reset` prop → attempts to re-render the segment without a full reload (client-side retry only).

**Server-side recovery on retry** (using `startTransition` + `router.refresh`):
```tsx
"use client";
import { useRouter } from "next/navigation";
import { startTransition } from "react";

export default function ErrorBoundary({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();
  const reload = () => {
    startTransition(() => {
      router.refresh();
      reset();
    });
  };
  return <button onClick={reload}>Try again</button>;
}
```

**Key nested-route error behavior:**
- Errors **bubble up** to the nearest parent `error.tsx`. Placing `error.tsx` higher up catches more; placing it deeper isolates the blast radius to just that segment.
- `error.tsx` **does NOT catch errors thrown inside `layout.tsx` of the same segment** (the layout sits above the error boundary in the component tree). To catch layout errors, move `error.tsx` up to the **parent** segment.

**Component hierarchy inside a route segment (outer → inner):**
```
layout.tsx
 └─ template.tsx
     └─ error.tsx (Error Boundary)
         └─ loading.tsx (Suspense Boundary)
             └─ not-found.tsx (Error Boundary)
                 └─ page.tsx
```

---

## 12. Parallel Routes

Render **multiple pages simultaneously** in the same layout, each in its own independently-navigable "slot," using the `@folder` convention.

```
app/complex-dashboard/
  ├── @children (implicit, page.tsx directly in the folder)
  ├── @users/page.tsx
  ├── @revenue/page.tsx
  ├── @notifications/page.tsx
  └── layout.tsx
```
```tsx
// app/complex-dashboard/layout.tsx
export default function DashboardLayout({
  children, users, revenue, notifications,
}: {
  children: React.ReactNode;
  users: React.ReactNode;
  revenue: React.ReactNode;
  notifications: React.ReactNode;
}) {
  return (
    <div>
      {children}
      {users}
      {revenue}
      {notifications}
    </div>
  );
}
```
Each slot is passed as a **named prop** to the layout matching the folder name (`@users` → `users` prop).

**Sub-navigation** inside a slot: a slot can contain its own regular nested route (e.g. `@notifications/archived/page.tsx`) with its own `<Link>` — navigating within a slot only re-renders that slot.

**Unmatched routes & `default.tsx`:**
- Client-side navigation: Next.js keeps showing whatever was last rendered in unmatched slots.
- **Full page reload**: Next.js needs a `default.tsx` fallback in each slot that doesn't match the current URL, or you get a 404.
```tsx
// app/complex-dashboard/@revenue/default.tsx
export default function Default() {
  return <p>Revenue metrics (default)</p>;
}
```

---

## 13. Conditional Routes

Use parallel routes (`@slot`) to conditionally show different UI in the same layout position — e.g. showing a login form vs. dashboard in the same spot based on auth state, without changing the URL structure or duplicating layout code.

---

## 14. Intercepting Routes

Lets you load a route from another part of the app **within the current layout**, while masking the URL (e.g. opening a photo in a modal from a feed, while the URL updates to the photo's real URL). Uses the `(.)`, `(..)`, `(..)(..)`, `(...)` folder-naming convention:

| Convention | Meaning |
|---|---|
| `(.)folder` | match segment on the **same** level |
| `(..)folder` | match segment **one level above** |
| `(..)(..)folder` | match segment **two levels above** |
| `(...)folder` | match segment from the **root** `app/` directory |

Typically combined with **Parallel Routes** to render the intercepted content as a modal overlay while a direct visit/refresh renders the full page normally.

---

## 15. Route Handlers (API Routes)

Route Handlers let you build custom request handlers (a backend API) for a route, replacing the old Pages Router `pages/api`. Defined in `route.ts` (or `route.js`) inside `app/`.

### Basic handler
```ts
// app/hello/route.ts
export async function GET() {
  return new Response("Hello World");
}
```
→ `GET /hello`

- Supported exports (named after HTTP verbs): `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`.
- Calling an unsupported method → automatic **405 Method Not Allowed**.
- Can be nested like page routes: `app/dashboard/route.ts`, `app/dashboard/users/route.ts`.

### ⚠️ Conflict with `page.tsx`
A `route.ts` **at the same segment level** as `page.tsx` wins — the page won't be served. Fix: nest the route handler under an `api` subfolder.
```
app/profile/page.tsx        → UI at /profile
app/profile/api/route.ts    → API at /profile/api
```

### GET example (returning JSON)
```ts
// app/comments/route.ts
import comments from "./data";

export async function GET() {
  return Response.json(comments);
}
```

### Dynamic route segments in handlers
```ts
// app/comments/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const comment = comments.find((c) => c.id === Number(id));
  return Response.json(comment);
}
```

### Headers
```ts
// Reading via the request parameter
import type { NextRequest } from "next/server";
export async function GET(request: NextRequest) {
  const requestHeaders = new Headers(request.headers);
  console.log(requestHeaders.get("Authorization"));
}

// Reading via next/headers helper
import { headers } from "next/headers";
export async function GET() {
  const headerList = await headers(); // async in Next.js 15
  console.log(headerList.get("Authorization"));
}
```
Headers from `next/headers` are **read-only**. To send custom **response** headers, return a `new Response()` with a `headers` option:
```ts
return new Response("<h1>Profile API data</h1>", {
  headers: { "Content-Type": "text/html" },
});
```

### Cookies
```ts
// Set via Set-Cookie response header
return new Response("...", { headers: { "Set-Cookie": "theme=dark" } });

// Read via request.cookies
const theme = request.cookies.get("theme");

// Using the built-in cookies() helper (async in Next 15)
import { cookies } from "next/headers";
export async function GET() {
  const cookieStore = await cookies();
  cookieStore.set("resultsPerPage", "20");   // set
  const value = cookieStore.get("resultsPerPage"); // read
}
```

### Caching
- `GET` route handlers are **cached by default** in the App Router for **static** routes (build-time). Use other verbs, dynamic functions (`headers()`, `cookies()`), or `export const dynamic = "force-dynamic"` to opt out of caching.

---

## 16. Middleware

Middleware (`middleware.ts` in `src/` or project root) runs **before a request is completed**, letting you rewrite, redirect, modify headers/cookies, or run auth checks. Covered in depth in the [Clerk section](#22-authentication-with-clerk), which uses `clerkMiddleware()` to protect routes.

---

## 17. Rendering: CSR, SSR, Hydration, RSC

### Client-Side Rendering (CSR) — plain React SPA
1. Server sends a near-empty HTML shell.
2. Browser downloads/parses/executes JS.
3. React renders content in the browser.

**Drawbacks:** poor SEO (crawlers may not execute JS), poor perceived performance (blank screen until JS loads).

### Server-Side Rendering (SSR)
Server renders full HTML for each request → browser shows content immediately → but the page isn't **interactive** until:
- **Hydration**: React reconstructs the component tree in-browser using the server HTML as a blueprint, then attaches event handlers/state.

**3 SSR problems (traditional, pre-React-18):**
1. Can't start rendering until **all** data is fetched (all-or-nothing waterfall).
2. Can't hydrate until **all** JS for the whole page has loaded.
3. Hydration happens in a **single pass** — nothing is interactive until everything is hydrated.

### React 18 Suspense SSR Architecture (fixes the above)
Enables two features:
1. **HTML streaming on the server** — wrap slow parts in `<Suspense>`; the rest of the HTML streams immediately, slow parts stream in when ready.
2. **Selective hydration on the client** — components hydrate independently and in priority order (e.g., based on user interaction) rather than waiting for the whole tree.

### React Server Components (RSC) rendering lifecycle (Next.js)
1. **Initial load**: Next.js + React render the server component tree on the server; output streamed to the browser as HTML + a serialized RSC payload; client hydrates interactive (client) parts.
2. **Subsequent navigation**: Browser requests a re-fetch of the route; Next matches server components, React renders them; instead of new HTML, Next.js streams back a special **RSC JSON-like format**; React **reconciles** this with what's on screen, preserving UI state (scroll position, input values, etc.).

---

## 18. Static, Dynamic & Streaming Rendering

Next.js supports **3 server rendering strategies**:

### a) Static Rendering (default)
- HTML generated **at build time** (production) — cacheable by CDN, shared across users, extremely fast.
- **Default** strategy for all routes in the App Router — no config needed.
- In **development**, pages are pre-rendered **on every request** (so you always see the latest code) rather than once at build.
- Ideal for: blogs, product listings, docs, marketing pages.
- Next dev shows a **static route indicator**.
- Build output (`npm run build`) shows a table with `Route`, `Size`, `First Load JS`, and a legend symbol (○ = static).

```bash
npm run build   # creates optimized .next production build
npm run start   # serve the production build
```

### b) Dynamic Rendering
Opt-in when content must be generated **per-request** (e.g. personalized, cookie/header-dependent, or search-param dependent content).

Trigger dynamic rendering by using:
- Dynamic functions: `cookies()`, `headers()`, `searchParams` (in some cases)
- `export const dynamic = "force-dynamic"`

`generateStaticParams` — pre-render specific dynamic route params at build time:
```tsx
// app/products/[productId]/page.tsx
export async function generateStaticParams() {
  const products = await fetch("https://.../products").then((r) => r.json());
  return products.map((p: { id: string }) => ({ productId: p.id }));
}
```
Any dynamic param **not** in the returned list is generated **on-demand at runtime** the first time it's visited, then cached as a static HTML file (visible in `.next/server/app/products/<id>.html`).

`dynamicParams` — controls behavior for params **not** included by `generateStaticParams`:
```tsx
export const dynamicParams = true;  // default: render on-demand for any other param
// export const dynamicParams = false; // 404 for params not pre-rendered
```
- `true` → good for e-commerce (pre-render popular products, allow access to the rest on-demand).
- `false` → good for a fixed blog (unknown slugs get a clean 404 immediately).

### c) Streaming
Breaks work into chunks streamed to the client as they're ready — improves initial load and unblocks slow data fetches from holding up the whole route. Implemented with `<Suspense>`:
```tsx
import { Suspense } from "react";
import Product from "@/components/Product";     // slow: 2s delay
import Reviews from "@/components/Reviews";      // slow: 4s delay

export default function ProductReviewsPage() {
  return (
    <div>
      <h1>Product Reviews</h1>
      <Suspense fallback={<p>Loading product details...</p>}>
        <Product />
      </Suspense>
      <Suspense fallback={<p>Loading reviews...</p>}>
        <Reviews />
      </Suspense>
    </div>
  );
}
```
The `<h1>` renders instantly; `Product` streams in after 2s; `Reviews` streams in after 4s — each independently, without blocking the others. (This is what `loading.tsx` does automatically at the page/segment level.)

---

## 19. Server / Client Component Composition Patterns

**Server components — best for:**
- Fetching data
- Accessing backend resources directly (files, DB)
- Keeping secrets/sensitive logic off the client
- Large dependencies that shouldn't ship to the browser

**Client components — best for:**
- Interactivity, event listeners
- State & lifecycle effects (`useState`, `useEffect`)
- Browser-only APIs
- Custom hooks / class components

### Pattern 1 — Server-only code
Some modules must **never** be bundled for the client (e.g. code with secret env vars, DB clients). Use the `server-only` package to get a build-time error if such a module is ever imported into client code.
```bash
npm install server-only
```
```ts
// lib/data.ts
import "server-only";
export async function getSecretData() { /* ... */ }
```

### Pattern 2 — Third-party components that use hooks
If a 3rd-party component internally uses hooks/context but doesn't declare `"use client"`, wrap it yourself in a small client component before using it inside a server component tree, or the build will error.

### Pattern 3 — Context Providers
Context (`createContext`, `useContext`) only works in Client Components — create a dedicated `providers.tsx` client component that wraps `children`, and use it inside the (server) root layout:
```tsx
// app/providers.tsx
"use client";
import { createContext } from "react";
export const ThemeContext = createContext("light");
export function Providers({ children }: { children: React.ReactNode }) {
  return <ThemeContext.Provider value="dark">{children}</ThemeContext.Provider>;
}

// app/layout.tsx (server component)
import { Providers } from "./providers";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html><body><Providers>{children}</Providers></body></html>
  );
}
```

### Pattern 4 — "Client component islands"
Keep as much of the tree as **server components** as possible; push `"use client"` **down** to the smallest leaf component that truly needs interactivity (e.g. just a submit button), rather than marking whole pages as client. This minimizes the client-side JS bundle.

---

## 20. Data Fetching

### a) Client-side fetching (in a Client Component)
Familiar React pattern with `useState` + `useEffect`.
```tsx
"use client";
import { useEffect, useState } from "react";

type User = { id: number; name: string; username: string; email: string; phone: string };

export default function UsersClient() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchUsers() {
      try {
        const res = await fetch("https://jsonplaceholder.typicode.com/users");
        if (!res.ok) throw new Error("Failed to fetch users");
        const data = await res.json();
        setUsers(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An unknown error occurred");
      } finally {
        setLoading(false);
      }
    }
    fetchUsers();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name} — {u.username} — {u.email} — {u.phone}</li>
      ))}
    </ul>
  );
}
```
> Use client-side fetching only when truly needed (realtime data, client-only interactions). Otherwise **prefer server components**.

### b) Server-side fetching (in a Server Component)
RSC architecture supports `async`/`await` directly in components.
```tsx
// app/users-server/page.tsx
type User = { id: number; name: string; username: string; email: string; phone: string };

export default async function UsersServer() {
  const res = await fetch("https://jsonplaceholder.typicode.com/users");
  const users: User[] = await res.json();

  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name} — {u.username} — {u.email} — {u.phone}</li>
      ))}
    </ul>
  );
}
```
Much simpler — no state, no loading/error boilerplate needed in the component itself (handled via `loading.tsx` / `error.tsx`).

### Loading & error states for data fetching
Use the special files:
- `loading.tsx` → shown automatically while the async server component resolves (Suspense boundary).
- `error.tsx` → catches thrown errors during fetch/render (Error Boundary — must be a client component).

### Sequential vs. Parallel data fetching
**Sequential** (waterfall — each `await` blocks the next):
```tsx
export default async function Page() {
  const user = await getUser();          // waits
  const posts = await getPosts(user.id); // then waits again
  // ...
}
```
**Parallel** (kick off simultaneously with `Promise.all`):
```tsx
export default async function Page() {
  const [user, posts] = await Promise.all([getUser(), getPosts()]);
  // both requests fire at the same time — faster overall
}
```
Use sequential fetching only when a later call genuinely **depends** on an earlier result.

### Fetching directly from a database (Prisma example)
```ts
// prisma/db.ts
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

export async function getProducts(query?: string) {
  if (query) {
    return prisma.product.findMany({
      where: {
        OR: [
          { title: { contains: query } },
          { description: { contains: query } },
        ],
      },
    });
  }
  return prisma.product.findMany();
}
export async function getProduct(id: number) {
  return prisma.product.findUnique({ where: { id } });
}
export async function addProduct(data: { title: string; price: number; description?: string }) {
  return prisma.product.create({ data });
}
export async function updateProduct(id: number, data: { title: string; price: number; description?: string }) {
  return prisma.product.update({ where: { id }, data });
}
export async function deleteProduct(id: number) {
  return prisma.product.delete({ where: { id } });
}
```
```tsx
// app/products-db/page.tsx — server component queries the DB directly, no API layer needed
import { getProducts } from "@/prisma/db";

export default async function ProductsDBPage() {
  const products = await getProducts();
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.title} — {p.description} — ${p.price}</li>
      ))}
    </ul>
  );
}
```

---

## 21. Data Mutations & Server Actions

### Traditional (pre-Server-Actions) approach
Client form → `useState` for fields → `onSubmit` handler → calls a custom API route → API route does the DB write → client handles loading state & redirect manually. Lots of boilerplate (form state, an API endpoint, fetch call, loading UI, redirect).

### Server Actions — the modern, streamlined way
An `async` function marked `"use server"`, callable directly from server **or** client components to handle mutations, without hand-rolling an API route.

**When to use:** secure DB writes, less API boilerplate, progressive enhancement, better performance (less client JS).

```tsx
// app/products-db/create/page.tsx (Server Component)
import { redirect } from "next/navigation";
import { addProduct } from "@/prisma/db";

export default function AddProductPage() {
  async function createProduct(formData: FormData) {
    "use server";
    const title = formData.get("title") as string;
    const price = Number(formData.get("price"));
    const description = formData.get("description") as string;

    await addProduct({ title, price, description });
    redirect("/products-db");
  }

  return (
    <form action={createProduct}>
      <input type="text" name="title" placeholder="Title" />
      <input type="text" name="price" placeholder="Price" />
      <input type="text" name="description" placeholder="Description" />
      <button type="submit">Add product</button>
    </form>
  );
}
```
- `"use server"` at the top of the function (or top of a whole file) marks it/its exports as Server Actions.
- Assign it directly to the form's `action` attribute — the form data is passed automatically as `FormData`.
- Runs **on the server only** — never shipped to the client bundle. Effectively an inline API endpoint.

**Benefits recap:**
1. Simplifies code (no separate API route / client state for the form).
2. More secure — sensitive logic stays server-side.
3. Better performance — less client JS.
4. **Progressive enhancement** — the form still works even with JavaScript disabled in the browser (native HTML form submission fallback).

### `useFormStatus` — pending state for the submit button
Must be used inside a **child** client component of the `<form>` (not the page itself, to avoid converting the whole server component page to a client component).
```tsx
// components/SubmitButton.tsx
"use client";
import { useFormStatus } from "react-dom";

export function SubmitButton() {
  const { pending } = useFormStatus();
  return <button type="submit" disabled={pending}>{pending ? "Submitting..." : "Add product"}</button>;
}
```
`useFormStatus()` returns `{ pending, data, method, action }`.

### `useActionState` — form state + validation + pending across submissions
```tsx
// actions/products.ts
"use server";
export type FormState = { errors: { title?: string[]; price?: string[]; description?: string[] } };

export async function createProduct(prevState: FormState, formData: FormData): Promise<FormState> {
  // validate, e.g. with zod...
  const title = formData.get("title") as string;
  if (!title) return { errors: { title: ["Title is required"] } };
  // ... await addProduct(...)
  redirect("/products-db");
}
```
```tsx
// in a client component
"use client";
import { useActionState } from "react";
import { createProduct } from "@/actions/products";

export function ProductForm() {
  const [state, formAction] = useActionState(createProduct, { errors: {} });
  return (
    <form action={formAction}>
      <input name="title" />
      {state.errors.title && <p>{state.errors.title[0]}</p>}
      {/* ... */}
    </form>
  );
}
```

### Passing extra arguments to a Server Action (e.g. an ID for update/delete)
Use `.bind()` instead of a hidden `<input>` (avoids exposing the ID unencoded in HTML):
```tsx
// Update
const editProductWithId = editProduct.bind(null, product.id);
const [state, formAction] = useActionState(editProductWithId, { errors: {} });

// Server action signature receives the bound arg FIRST:
export async function editProduct(id: number, prevState: FormState, formData: FormData) {
  // ...
  await updateProduct(id, { title, price, description });
}
```
```tsx
// Delete
<form action={removeProduct.bind(null, product.id)}>
  <button type="submit">Delete</button>
</form>
```

### `revalidatePath` — refresh cached data after a mutation
```ts
"use server";
import { revalidatePath } from "next/cache";

export async function removeProduct(id: number) {
  await deleteProduct(id);
  await revalidatePath("/products-db"); // re-fetches data for that route
}
```
Without this, the listing page won't reflect deletions/updates until manually refreshed.

### `useOptimistic` — instant UI feedback before the server responds
```tsx
"use client";
import { useOptimistic } from "react";
import { removeProduct } from "@/actions/products";

export function ProductDetail({ products }: { products: Product[] }) {
  const [optimisticProducts, setOptimisticProducts] = useOptimistic(
    products,
    (currentProducts, productId: number) =>
      currentProducts.filter((p) => p.id !== productId)
  );

  async function removeProductById(productId: number) {
    setOptimisticProducts(productId); // instantly updates UI
    await removeProduct(productId);   // actual deletion happens in background
  }

  return (
    <ul>
      {optimisticProducts.map((p) => (
        <li key={p.id}>
          {p.title}
          <form action={removeProductById.bind(null, p.id)}>
            <button type="submit">Delete</button>
          </form>
        </li>
      ))}
    </ul>
  );
}
```
> `useOptimistic` is a hook → must live in a **client component**. Split data-fetching (server component `page.tsx`) from mutation UI (client component) and pass fetched data down as a prop.

### The `<Form>` component (`next/form`)
Extends the native `<form>` element with:
- Automatic **prefetching** of the loading UI for the destination route.
- **Client-side navigation** on submit (instead of full reload) — form data becomes URL search params for GET-style forms.
- **Progressive enhancement** (still works without JS).
- Also supports Server Actions directly.
```tsx
import Form from "next/form";

export function Search() {
  return (
    <Form action="/products-db">
      <input type="text" name="query" placeholder="Search products" />
      <button type="submit">Submit</button>
    </Form>
  );
}
```

---

## 22. Authentication with Clerk

Three fundamentals of user-facing apps: **identity** (authentication), **sessions** (session management), **access** (authorization). Next.js protects three surfaces: client code, server code, API routes. Next.js's own docs recommend using an auth **library** rather than rolling your own. This course uses **Clerk** (free up to 10,000 MAU).

### Setup (4 steps)
```bash
npm install @clerk/nextjs
```
1. **Env vars** — create `.env.local`:
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
CLERK_SECRET_KEY=...
```
2. **Middleware** — `src/middleware.ts`:
```ts
import { clerkMiddleware } from "@clerk/nextjs/server";

export default clerkMiddleware();

export const config = {
  matcher: [
    "/((?!_next|[^?]*\\.(?:html?|css|js|...)).*)",
    "/(api|trpc)(.*)",
  ],
};
```
3. **Wrap the app** with `<ClerkProvider>` in the root layout:
```tsx
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en"><body>{children}</body></html>
    </ClerkProvider>
  );
}
```
4. Start building sign-in/out UI.

### Sign in / Sign out / User button (prebuilt components)
```tsx
// components/Navigation.tsx
import { SignInButton, SignUpButton, SignOutButton, UserButton, SignedIn, SignedOut } from "@clerk/nextjs";

export const Navigation = () => (
  <nav>
    <h1>Next.js App</h1>
    <SignedOut>
      <SignInButton mode="modal" />
      <SignUpButton mode="modal" />
    </SignedOut>
    <SignedIn>
      <UserButton /> {/* dropdown: Sign out / Manage account */}
    </SignedIn>
  </nav>
);
```
- `<SignedIn>` / `<SignedOut>` conditionally render children based on auth state — Clerk handles the logic.
- `mode="modal"` opens a modal instead of navigating to a hosted page.

### Custom-styled buttons
```tsx
<SignInButton mode="modal">
  <button className="bg-blue-500 text-white px-4 py-2 rounded">Sign in</button>
</SignInButton>
```

### Dedicated profile page (embedding `<UserProfile>`)
```tsx
// app/user-profile/[[...user-profile]]/page.tsx  (optional catch-all!)
import { UserProfile } from "@clerk/nextjs";

export default function UserProfilePage() {
  return (
    <div className="flex justify-center items-center p-8">
      <UserProfile path="/user-profile" />
    </div>
  );
}
```

### Protecting routes via middleware
```ts
// src/middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher(["/user-profile(.*)"]);

export default clerkMiddleware(async (auth, request) => {
  if (isProtectedRoute(request)) {
    await auth.protect(); // auto-redirects to sign-in if not authenticated
  }
});
```
**Inverse pattern** — protect everything except a public allow-list:
```ts
const isPublicRoute = createRouteMatcher(["/", "/sign-in(.*)", "/sign-up(.*)"]);

export default clerkMiddleware(async (auth, request) => {
  if (!isPublicRoute(request)) {
    await auth.protect();
  }
});
```
**Manual control (custom logic before redirect):**
```ts
export default clerkMiddleware(async (auth, request) => {
  const { userId, redirectToSignIn } = await auth();
  if (!userId && !isPublicRoute(request)) {
    return redirectToSignIn();
  }
});
```

### Reading user/session data

**In Server Components / Route Handlers** — `auth()` and `currentUser()`:
```tsx
import { auth, currentUser } from "@clerk/nextjs/server";

export default async function DashboardPage() {
  const authObject = await auth();       // userId, sessionId, sessionClaims, redirectToSignIn...
  const userObject = await currentUser(); // full backend user object (email, name, image, etc.)
  console.log(authObject, userObject);
  return <h1>Dashboard</h1>;
}
```

**In Client Components** — `useAuth()` and `useUser()` hooks:
```tsx
"use client";
import { useAuth, useUser } from "@clerk/nextjs";

export const Counter = () => {
  const { isLoaded, userId } = useAuth();
  const { isLoaded: userLoaded, isSignedIn, user } = useUser();

  if (!isLoaded || !userId) return null; // hide if signed out

  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((c) => c + 1)}>Count: {count}</button>;
};
```
- Use `useAuth()` if you only need `userId` for personalization/data association.
- Use `useUser()` when you need the full user object.

### Custom sign-in / sign-up pages (instead of hosted/modal)
```tsx
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from "@clerk/nextjs";
export default function SignUpPage() {
  return <div className="flex justify-center items-center p-8"><SignUp /></div>;
}

// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from "@clerk/nextjs";
export default function SignInPage() {
  return <div className="flex justify-center items-center p-8"><SignIn /></div>;
}
```
Ensure both routes are marked **public** in middleware. Then in `.env.local`:
```
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```
Restart the dev server after editing env vars.

### Redirect behavior after auth
- By default, Clerk remembers where the user came from via a `redirect_url` query param and returns them there after sign-in.
- **Fallback URLs** (used only if no `redirect_url` present):
```
NEXT_PUBLIC_CLERK_SIGN_UP_FALLBACK_REDIRECT_URL=/onboarding
NEXT_PUBLIC_CLERK_SIGN_IN_FALLBACK_REDIRECT_URL=/dashboard
```
- **Force redirects** (always redirect here, ignoring where the user came from):
```
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/onboarding
NEXT_PUBLIC_CLERK_SIGN_IN_FORCE_REDIRECT_URL=/dashboard
```

### Role-Based Access Control (RBAC)

**Step 1 — expose `publicMetadata` in the session token** (Clerk Dashboard → Sessions → Customize session token):
```json
{ "metadata": "{{user.public_metadata}}" }
```

**Step 2 — global TypeScript types:**
```ts
// types/global.d.ts
export {};
export type Roles = "admin" | "moderator";

declare global {
  interface CustomJwtSessionClaims {
    metadata?: { role?: Roles };
  }
}
```

**Step 3 — assign a role** to a user manually via Clerk Dashboard (Users → select user → Public metadata → `{ "role": "admin" }`), or programmatically (see Step 5).

**Step 4 — protect an admin route in middleware:**
```ts
import { NextResponse } from "next/server";
const isAdminRoute = createRouteMatcher(["/admin"]);

export default clerkMiddleware(async (auth, request) => {
  if (isAdminRoute(request) && (await auth()).sessionClaims?.metadata?.role !== "admin") {
    const url = new URL("/", request.url);
    return NextResponse.redirect(url);
  }
});
```

**Step 5 — server actions to manage roles:**
```ts
// app/admin/actions.ts
"use server";
import { auth, clerkClient } from "@clerk/nextjs/server";
import { revalidatePath } from "next/cache";
import { Roles } from "@/types/globals";

export async function setRole(formData: FormData) {
  const { sessionClaims } = await auth();
  if (sessionClaims?.metadata?.role !== "admin") throw new Error("Not authorized");

  const client = await clerkClient();
  const id = formData.get("id") as string;
  const role = formData.get("role") as Roles;

  try {
    await client.users.updateUser(id, { publicMetadata: { role } });
    revalidatePath("/admin");
  } catch {
    throw new Error("Failed to set role");
  }
}

export async function removeRole(formData: FormData) {
  const { sessionClaims } = await auth();
  if (sessionClaims?.metadata?.role !== "admin") throw new Error("Not authorized");

  const client = await clerkClient();
  const id = formData.get("id") as string;

  try {
    await client.users.updateUser(id, { publicMetadata: { role: null } });
    revalidatePath("/admin");
  } catch {
    throw new Error("Failed to remove role");
  }
}
```
```tsx
// app/admin/page.tsx (fetch and list users; buttons call the server actions)
import { clerkClient } from "@clerk/nextjs/server";
import { setRole, removeRole } from "./actions";

export default async function AdminPage() {
  const client = await clerkClient();
  const users = (await client.users.getUserList()).data;

  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>
          {u.firstName} {u.lastName} — {u.emailAddresses[0]?.emailAddress} — role: {(u.publicMetadata as any).role}
          <form action={setRole}>
            <input type="hidden" name="id" value={u.id} />
            <input type="hidden" name="role" value="admin" />
            <button type="submit">Make admin</button>
          </form>
          <form action={setRole}>
            <input type="hidden" name="id" value={u.id} />
            <input type="hidden" name="role" value="moderator" />
            <button type="submit">Make moderator</button>
          </form>
          <form action={removeRole}>
            <input type="hidden" name="id" value={u.id} />
            <button type="submit">Remove role</button>
          </form>
        </li>
      ))}
    </ul>
  );
}
```
> For larger apps, Clerk also offers a built-in **Organizations** feature with its own roles/permissions system — worth exploring beyond a custom RBAC setup.

---

## 23. Deployment (Vercel)

1. Push your project to **GitHub**.
2. Sign up / log in at **vercel.com** (e.g., with GitHub).
3. **Add New Project** → import your GitHub repo → select the correct **root directory** if it's a monorepo/subfolder → framework preset: **Next.js**.
4. Expand **Environment Variables** → paste in all required keys (e.g., the 4 Clerk variables from `.env.local`).
5. Click **Deploy** — Vercel builds and deploys automatically.
6. You get a `<project>.vercel.app` URL; you can later attach a custom domain.

---

## 24. Quick-Reference Cheat Sheet

| Convention file | Purpose |
|---|---|
| `page.tsx` | Makes a route segment publicly accessible |
| `layout.tsx` | Shared UI wrapper; persists across navigation; needs `children` prop |
| `template.tsx` | Like layout, but remounts fresh on every navigation |
| `loading.tsx` | Automatic Suspense fallback for a segment |
| `error.tsx` | Automatic Error Boundary (must be Client Component); props: `error`, `reset` |
| `not-found.tsx` | Custom 404 UI; trigger manually with `notFound()` |
| `route.ts` | Route Handler (API endpoint); export `GET/POST/PUT/PATCH/DELETE` |
| `default.tsx` | Fallback UI for unmatched parallel-route slot on full reload |
| `middleware.ts` | Runs before request completes (auth, redirects, rewrites) |

| Folder convention | Meaning |
|---|---|
| `[param]` | Dynamic segment |
| `[...param]` | Catch-all segment (1+ segments) |
| `[[...param]]` | Optional catch-all (0+ segments) |
| `(group)` | Route group — organizes without affecting URL |
| `_folder` | Private folder — excluded from routing |
| `@slot` | Parallel route slot |
| `(.)folder`, `(..)folder`, `(...)folder` | Intercepting route |

| Hook / API | Where | Purpose |
|---|---|---|
| `useRouter()` | Client | `push/replace/back/forward` |
| `usePathname()` | Client | Current path string |
| `redirect()` | Server | Server-side redirect |
| `notFound()` | Server | Trigger 404 |
| `useFormStatus()` | Client (child of `<form>`) | `{ pending, data, method, action }` |
| `useActionState()` | Client | Form state + server action wiring |
| `useOptimistic()` | Client | Optimistic UI updates |
| `revalidatePath()` | Server | Bust cache for a path after mutation |
| `generateStaticParams()` | Server | Pre-render dynamic params at build time |
| `generateMetadata()` | Server | Dynamic `<title>`/meta tags |
| `auth()`, `currentUser()` | Server (Clerk) | Session/user data |
| `useAuth()`, `useUser()` | Client (Clerk) | Session/user data |

**Server vs Client Component decision:**
- Default to **Server Component**.
- Add `"use client"` only when you need: hooks (`useState`, `useEffect`, etc.), event handlers, browser APIs, or context providers/consumers.
- Push `"use client"` as **far down** the tree as possible (small islands, not whole pages).

**Rendering strategy decision:**
- Static (default) → content is the same for everyone, doesn't change often.
- Dynamic (`force-dynamic`, or using `cookies()`/`headers()`) → personalized/per-request content.
- Streaming (`<Suspense>` / `loading.tsx`) → speed up perceived load when parts of a page are slow.
