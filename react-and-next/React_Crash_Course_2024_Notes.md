# React 2024 Crash Course — Full Revision Notes
### Source video: React Crash Course 2024 (Job Listings App w/ React Router + JSON Server)
Video link: https://www.youtube.com/watch?v=LDB4uaJ87e0

These notes follow the video timeline exactly, expand every concept in detail, and include reconstructed code for every part of the project (Navbar, Hero, Cards, Job Listings, Router, Forms, CRUD with JSON Server, Toastify, Spinners, Production Build). Use this as a single revision reference — everything you need to rebuild the project from scratch is here.

---

## Table of Contents
1. [Intro](#1-000---intro)
2. [What Is React?](#2-155---what-is-react)
3. [Why React?](#3-343---why-react)
4. [What Are Components?](#4-719---what-are-components)
5. [What Is State?](#5-821---what-is-state)
6. [What Are Hooks?](#6-1000---what-are-hooks)
7. [What Is JSX?](#7-1117---what-is-jsx)
8. [SPA, SSR, SSG](#8-1242---spa-ssr-ssg)
9. [Vite](#9-1538---vite)
10. [Project Demo](#10-1630---project-demo)
11. [Setup React With Vite](#11-1953---setup-react-with-vite)
12. [File Explanation](#12-2229---file-explanation)
13. [Boilerplate Cleanup](#13-2511---boilerplate-cleanup)
14. [Tailwind CSS Setup](#14-2648---tailwind-css-setup)
15. [JSX Crash Course](#15-3024---jsx-crash-course)
16. [Start Homepage](#16-3937---start-homepage)
17. [Navbar Component](#17-4200---navbar-component)
18. [Image Import](#18-4356---image-import)
19. [Hero Component](#19-4524---hero-component)
20. [Props](#20-4617---props)
21. [Default Props](#21-4800---default-props)
22. [Wrapper Components](#22-4851---wrapper-components)
23. [JobListings Component](#23-5514---joblistings-component)
24. [Create Lists With map()](#24-5850---create-lists-with-map)
25. [Single JobListing Component](#25-10320---single-joblisting-component)
26. [Limit Jobs to 3](#26-10549---limit-jobs-to-3)
27. [useState() Hook & Description Toggle](#27-10750---usestate-hook--desc-toggle)
28. [Creating an Event](#28-11307---creating-an-event)
29. [Updating Component State](#29-11420---updating-component-state)
30. [React Icons Package](#30-11600---react-icons-package)
31. [React Router Setup](#31-11800---react-router-setup)
32. [Create Routes From Elements](#32-12021---create-routes-from-elements)
33. [Router Provider](#33-12136---router-provider)
34. [Homepage Component/Route](#34-12236---homepage-componentroute)
35. [Layouts](#35-12440---layouts)
36. [Jobs Page Component/Route](#36-12906---jobs-page-componentroute)
37. [Link Component](#37-13050---link-component)
38. [Custom 404 Page](#38-13420---custom-404-page)
39. [Active Links With NavLink](#39-13655---active-links-with-navlink)
40. [Conditional Rendering](#40-14100---conditional-rendering)
41. [JSON Server Setup](#41-14310---json-server-setup)
42. [useEffect() & Data Fetching](#42-14700---useeffect--data-fetching)
43. [Loading Spinner](#43-15307---loading-spinner)
44. [Conditional Fetching](#44-15106---conditional-fetching)
45. [Proxying](#45-15945---proxying)
46. [Single Job Page](#46-20338---single-job-page)
47. [useParams() to Get ID](#47-20904---useparams-to-get-id)
48. [Data Loaders](#48-21225---data-loaders)
49. [Single Job Output](#49-21636---single-job-output)
50. [Add Job Page](#50-22200---add-job-page)
51. [Working With Forms](#51-22340---working-with-forms)
52. [Form Submission](#52-23005---form-submission)
53. [Pass Function as Prop](#53-23527---pass-function-as-prop)
54. [POST Request to Add Job](#54-23932---post-request-to-add-job)
55. [Delete Job Button/Function](#55-24145---delete-job-buttonfunction)
56. [DELETE Request to Remove Job](#56-24512---delete-request-to-remove-job)
57. [React Toastify Package](#57-24650---react-toastify-package)
58. [Edit Job Page/Form](#58-25008---edit-job-pageform)
59. [Update Form Submission](#59-25605---update-form-submission)
60. [PUT Request to Update Job](#60-25854---put-request-to-update-job)
61. [Build Static Assets For Production](#61-30210---build-static-assets-for-production)
62. [Full Cheat Sheet / Quick Reference](#62-full-cheat-sheet--quick-reference)

---

## 1. [0:00] - Intro

- This is a **beginner-focused React crash course**, built as a recurring "every 2-3 years" refresher series the instructor does for major frameworks.
- Project built: a **front-end for a job listing website**.
- Concepts covered: **components, props, state, hooks, data fetching**, and **React Router** (for multi-page/SPA routing).
- Backend: **JSON Server** is used to create a **mock REST API** so the app has real data to fetch/post/put/delete against.
- **React 19 note:** at time of recording, React 19 was not yet released. React 19's headline feature is a **compiler** that converts React code to plain JS (similar in spirit to Svelte), potentially doubling performance and removing the need for some manual optimization. The course uses **React 18**, but core concepts (components, props, state, hooks) remain unchanged between 18 and 19.

> 💡 Revision tip: Know that React's fundamentals (components/props/state/hooks) are considered **stable knowledge** — regardless of React version, these are the transferable skills.

---

## 2. [1:55] - What Is React? (Slide)

- **React** = a **JavaScript library** for building user interfaces (UIs), built from **components**.
- Created and maintained by **Facebook (Meta)** + a large community of developers/companies.
- **Library vs. Framework:**
  - A **framework** (e.g., Angular) is a *complete solution* — includes router, HTTP client, state management, etc. out of the box.
  - React is technically a **UI library**, not a framework — but it's often *called* a framework because it's commonly paired with other libraries (React Router, etc.) to become a full solution, and because it competes directly with frameworks like Angular.
- React is the **most popular** of the major front-end options: **React, Vue.js, Angular, Svelte**.
- React's ecosystem is huge — it powers:
  - **SPAs** (Single Page Applications)
  - **SSR** apps (via meta-frameworks like Next.js, Remix)
  - **Static sites** (via Gatsby, Astro)

---

## 3. [3:43] - Why React? (Slide)

**History / motivation:**
- Old web: fully static, every click = full page refresh.
- **AJAX** arrived: allowed fetching data *without* refreshing the page → enabled SPAs with dynamic UX.
- Problem: vanilla JS SPAs become **hard to maintain** as they scale — code gets messy without structure.
- **React (and other frameworks)** solve this by giving structure or a way to build complex, dynamic UIs in a maintainable, scalable way.

**Under the hood (React 18 and earlier):**
- React traditionally uses a **Virtual DOM** — a lightweight in-memory copy of the real DOM.
- When component **state changes**, the Virtual DOM updates first, then React **diffs** (compares) the virtual DOM against the real DOM and updates *only the parts that changed* (efficient reconciliation).
- **React 19** is set to replace this mechanism with a **compiler**, making updates faster and automating optimizations that devs used to do manually (e.g., `useMemo`, `useCallback`).

**Why React specifically (vs Vue/Svelte)?**
- Instructor's honest take: the #1 reason to pick React is **job market demand** — there are far more React jobs than Vue/Svelte jobs.
- Ecosystem: React Native (mobile), Next.js/Remix (SSR meta-frameworks).
- Instructor's personal opinion (flagged as opinion, not fact): Vue and Svelte are *more straightforward* to write code in; React "over-complicates" some things. If you don't care about job-market and are a freelancer/indie builder, it's worth exploring Vue/Svelte too.
- Good news: **the frameworks are conceptually similar** — components, props, state — so skills transfer; only syntax changes.

---

## 4. [7:19] - What Are Components? (Slide)

- A **component** = a reusable piece of code used to build a piece of UI. Think of components as **custom HTML elements**.
- Components can be broken into smaller components — called **composition**. This lets you decompose complex UIs into small, manageable, maintainable pieces.
- Two types historically:
  - **Class components** — the old way (has lifecycle methods). Rarely used today.
  - **Functional components** — the modern/standard way. **This course uses functional components exclusively.**
- Components can accept **props** (like function arguments/attributes) and can hold their own **state** (internal data).

---

## 5. [8:21] - What Is State? (Slide)

- **State** = data that a component manages internally; it can change over time in response to user interaction or other factors.
- Typical uses of state: user input, fetched API data, UI toggles (e.g., is a modal open/closed).
- In a **functional component**, you declare state using the **`useState` hook**.
  - `useState` returns an **array with two elements**: `[currentValue, updaterFunction]`.
- **Global State**: state relevant to the whole app, not just one component (e.g., data fetched once and shared across many components). Options to manage it:
  1. Keep it in a top-level/parent component and **pass it down via props**.
  2. **React Context API** (not covered in depth in this course — noted as "beyond scope").
  3. Third-party libraries like **Redux** (also not covered).
- This course sticks to local component state + props drilling + React Router's data loaders for "global-ish" data.

---

## 6. [10:00] - What Are Hooks? (Slide)

- **Hooks** = special functions that let **functional components** use state and other React features **without writing a class**.
- Historically, class components had **lifecycle methods** (e.g., `componentDidMount`) — functional components don't have these because they aren't classes, so **hooks replace that functionality**.
- The **two essential hooks** for beginners: `useState` and `useEffect`.
- All hooks start with the word **`use`** (naming convention, also enforced by React's rules of hooks).
- You can create **custom hooks** to encapsulate reusable logic (not covered in depth here, but mentioned as possible).
- Note: a few hooks are being phased out/replaced in React 19 (not detailed further in this course).

---

## 7. [11:17] - What Is JSX? (Slide)

- **JSX** = JavaScript XML/Syntax Extension — HTML-like syntax written directly inside JavaScript. This is what a component **returns**.
- Example shown on slide (a `Hero` component with props and a default value):

```jsx
function Hero({ title = 'Become a React Dev', subtitle = 'Find the React job that fits your skill set' }) {
  return (
    <section>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </section>
  );
}
```

- JSX is **dynamic** — "HTML if it were a programming language." You can embed:
  - **Expressions**: `{someVariable}`
  - **Loops**: via `.map()`
  - **Conditionals**: via ternary (`? :`) or `&&`
- **Key differences from HTML:**
  - `class` → `className` (because `class` is a reserved JS keyword)
  - `for` (on `<label>`) → `htmlFor`
  - Attributes are generally **camelCase** (e.g., `onClick`, `onChange`)

---

## 8. [12:42] - SPA, SSR, SSG (Slide)

| Type | How it works | Pros | Cons | Frameworks |
|---|---|---|---|---|
| **SPA** (Single Page Application) | Loads one `index.html` + one JS bundle; JS renders everything client-side, including "page" changes | Fast, highly interactive | Slower initial load, weaker SEO (content loaded via JS) | React (plain), Vue, etc. |
| **SSR** (Server-Side Rendered) | Initial page rendered on the **server**, then hydrated client-side | Better SEO, faster initial paint | Needs an actual server to deploy (not just static hosting) | Next.js, Remix |
| **SSG** (Static Site Generation) | HTML files generated **at build time** | Great performance & SEO, cheap hosting | Not ideal for highly dynamic/personalized content | Gatsby, Astro |

- Important clarification from the instructor: **React itself doesn't generate static HTML** — it's the **meta-framework** (Gatsby, Next.js, etc.) that does SSR/SSG; React is the UI layer underneath all of them.
- This course builds a **plain SPA** with Vite (no meta-framework).

---

## 9. [15:38] - Vite (Slide)

- **Vite** = a modern build tool/dev server used to scaffold and run React projects.
- Built on **esbuild** (a very fast JS bundler).
- Advantages over the older **Create React App (CRA)**:
  - CRA is bloated, slower, and **no longer actively recommended/maintained**.
  - Vite has a faster, better dev experience, and built-in **Hot Module Replacement (HMR)**.
- Setup command used later:

```bash
npm create vite@latest
```

---

## 10. [16:30] - Project Demo

- Instructor walks through the finished app in the browser before building it, so you know the target:
  - Homepage with **Navbar**, **Hero** section, home info **Cards**, and a **"Recent Jobs"** preview (limited to 3).
  - **Jobs page** — lists *all* jobs (from JSON Server).
  - **Single Job page** — `/jobs/:id` route, shows full job + company details, Edit/Delete buttons.
  - **Add Job page** — a form that POSTs a new job to the mock API.
  - **Edit Job page** — pre-filled form that PUTs updates to the mock API.
  - **Custom 404 page** for unmatched routes.
  - Styled entirely with **Tailwind CSS**.

---

## 11. [19:53] - Setup React With Vite

```bash
npm create vite@latest

# Prompts:
# ✔ Project name: … react-course
# ✔ Select a framework: › React
# ✔ Select a variant: › JavaScript

cd react-course
npm install
npm run dev
```

- This scaffolds a full Vite + React project with hot reload dev server (usually `http://localhost:5173`).

---

## 12. [22:29] - File Explanation

Key files/folders created by Vite:

```
react-course/
├── index.html          # single HTML page, has <div id="root"> and script tag pointing to main.jsx
├── package.json         # scripts (dev, build, preview) + dependencies
├── vite.config.js        # Vite configuration (plugins, proxy, etc.)
├── src/
│   ├── main.jsx          # entry point — mounts <App /> into #root using ReactDOM.createRoot
│   ├── App.jsx            # main/root component
│   ├── App.css / index.css
│   └── assets/            # static assets (images, svgs)
└── public/               # static files served as-is
```

`main.jsx` (typical Vite boilerplate):

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

- `index.html` has the `<div id="root"></div>` where the whole React app mounts, plus `<script type="module" src="/src/main.jsx"></script>`.

---

## 13. [25:11] - Boilerplate Cleanup

- Delete the default Vite starter content: the counter button, the spinning logos, extra CSS.
- Common shortcut used throughout the course: the **`rafce`** / **`rafc`** VS Code snippet (from the "ES7+ React/Redux/React-Native snippets" extension):
  - `rafce` = **R**eact **A**rrow **F**unction **C**omponent **E**xport (named export at bottom)
  - `rafc` = same but with default export inline

```jsx
// rafce output example
import React from 'react';

const App = () => {
  return (
    <div>App</div>
  );
};

export default App;
```

- Clean `App.jsx` down to just this minimal shell before rebuilding the homepage.

---

## 14. [26:48] - Tailwind CSS Setup

Standard Tailwind + Vite install (as used in the video, Tailwind v3 style):

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This creates `tailwind.config.js` and `postcss.config.js`.

`tailwind.config.js` — set the `content` glob so Tailwind scans your files for class names:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Add Tailwind directives to `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

Make sure `index.css` is imported in `main.jsx`, then use classes directly in JSX, e.g. `className="bg-gray-100 p-4"`.

---

## 15. [30:24] - JSX Crash Course

A focused mini-lesson on JSX mechanics using a scratch component:

**1. Rendering variables/expressions:**

```jsx
const name = 'John';
return <h1>Hello {name}</h1>;
```

**2. Lists with `.map()` need a unique `key` prop:**

```jsx
const people = ['John', 'Sara', 'Mike'];

<ul>
  {people.map((person, index) => (
    <li key={index}>{person}</li>
  ))}
</ul>
```
> If no unique ID exists in your data, use the array **index** as the key (not ideal for reorderable lists, but fine here).

**3. Conditionals — JSX can't contain `if` statements directly (must be expressions), so use:**

- **Ternary** (if/else):
```jsx
{loggedIn ? <h1>Hello member</h1> : <h1>Hello guest</h1>}
```
- **Logical AND `&&`** (if-only, renders nothing when false):
```jsx
{loggedIn && <h1>Hello member</h1>}
```
- Or, do the `if` **above** the `return` and have **early/different returns**:
```jsx
if (loggedIn) {
  return <h1>Hello member</h1>;
}
return <div>...normal content...</div>;
```

**4. Inline styles** (camelCase properties, values in double braces `{{ }}`):

```jsx
<h1 style={{ color: 'red', fontSize: '24px' }}>Hello John</h1>
```

Or store styles in a variable:

```jsx
const styles = { color: 'red', fontSize: '55px' };
<h1 style={styles}>Hello John</h1>
```

> Note: this project uses **Tailwind classes** instead of inline styles for actual project code — the inline style demo is just for teaching JSX.

**5. HTML → JSX gotchas:**
- `class` → `className`
- `for` (label) → `htmlFor`
- HTML comments inside JSX must be JS-style: `{/* comment */}` or simply removed, or you'll get a syntax error.
- Self-closing tags must actually self-close in JSX (e.g., `<img />`, `<input />`).

---

## 16. [39:37] - Start Homepage

Workflow used: **copy the static HTML theme file → paste into `App.jsx` → convert to JSX → then split into components.**

1. Open the provided static `index.html` theme file, copy everything inside `<body>` **except** the closing `<script>` tag.
2. Since a component can only return **one root element**, wrap everything in a **Fragment**:

```jsx
const App = () => {
  return (
    <>
      <nav>...</nav>
      <section className="hero">...</section>
      {/* ...home cards, job listings, etc... */}
    </>
  );
};

export default App;
```

3. Fix issues:
   - Replace all `class="..."` with `className="..."` (VS Code: select one instance → `Cmd/Ctrl+Shift+L` to select all matches → retype).
   - Remove/convert HTML comments to JSX comment syntax `{/* ... */}` or delete them (raw HTML comments break JSX parsing).

---

## 17. [42:00] - Navbar Component

1. Create `src/components/Navbar.jsx` → run `rafce`.
2. Cut the entire `<nav>...</nav>` block out of `App.jsx`, paste into `Navbar.jsx`'s `return`.
3. Import and use it in `App.jsx`:

```jsx
// App.jsx
import Navbar from './components/Navbar';

const App = () => {
  return (
    <>
      <Navbar />
      {/* rest of homepage */}
    </>
  );
};
```

```jsx
// components/Navbar.jsx
const Navbar = () => {
  return (
    <nav className="bg-indigo-700 border-b border-indigo-500">
      {/* logo, nav links */}
    </nav>
  );
};

export default Navbar;
```

- Verified in **React DevTools → Components tab** — you can see the component tree (`App > Navbar`) and inspect its props/state.

---

## 18. [43:56] - Image Import

- Delete the default Vite `react.svg`.
- Add an `images` folder inside `src/assets/` and drop in `logo.png`.
- Import and use the image like a JS module (Vite handles bundling/URLs automatically):

```jsx
import logo from '../assets/images/logo.png';

// inside JSX:
<img src={logo} alt="Logo" />
```

---

## 19. [45:24] - Hero Component

1. Cut the hero `<section>` out of `App.jsx`.
2. Create `src/components/Hero.jsx` → `rafce` → paste section into `return`.
3. Import into `App.jsx`:

```jsx
import Hero from './components/Hero';

<Hero />
```

Now the component tree shows `App > Navbar, Hero`.

---

## 20. [46:17] - Props

- **Props** = attributes passed into a component (like function arguments).

**Passing props from parent:**
```jsx
<Hero title="Test Title" subtitle="This is the subtitle" />
```

**Receiving via the `props` object:**
```jsx
const Hero = (props) => {
  return (
    <section>
      <h1>{props.title}</h1>
      <p>{props.subtitle}</p>
    </section>
  );
};
```

**Destructuring props (preferred/cleaner style):**
```jsx
const Hero = ({ title, subtitle }) => {
  return (
    <section>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </section>
  );
};
```

---

## 21. [48:00] - Default Props

Assign default values directly in the destructuring:

```jsx
const Hero = ({
  title = 'Become a React Dev',
  subtitle = 'Find the React job that fits your skill set',
}) => {
  return (
    <section>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </section>
  );
};
```

- If the parent **doesn't pass a value**, the default is used.
- If the parent **does pass a value**, it **overrides** the default.

---

## 22. [48:51] - Wrapper Components

Concept: a **wrapper/children component** wraps arbitrary content passed between its opening/closing tags.

**`Card.jsx` — a generic reusable wrapper:**
```jsx
const Card = ({ children, bg = 'bg-gray-100' }) => {
  return (
    <div className={`${bg} p-6 rounded-lg shadow-md`}>
      {children}
    </div>
  );
};

export default Card;
```

- `children` is a **special prop** — it represents whatever JSX is nested **inside** the component tags.

**`HomeCards.jsx` — using `Card` twice with different background colors passed as props:**
```jsx
import Card from './Card';

const HomeCards = () => {
  return (
    <section className="py-4">
      <div className="container-xl lg:container m-auto grid md:grid-cols-2 gap-6">
        <Card bg="bg-gray-100">
          <h2 className="text-2xl font-bold">For Developers</h2>
          <p className="mt-2 mb-4">
            Browse our React jobs and start your career today.
          </p>
          <a
            href="/jobs.html"
            className="inline-block bg-black text-white rounded-lg px-4 py-2 hover:bg-gray-700"
          >
            Browse Jobs
          </a>
        </Card>

        <Card bg="bg-indigo-100">
          <h2 className="text-2xl font-bold">For Employers</h2>
          <p className="mt-2 mb-4">
            List your job to find the perfect developer for the role.
          </p>
          <a
            href="/add-job.html"
            className="inline-block bg-indigo-500 text-white rounded-lg px-4 py-2 hover:bg-indigo-600"
          >
            Add Job
          </a>
        </Card>
      </div>
    </section>
  );
};

export default HomeCards;
```

```jsx
// App.jsx
import HomeCards from './components/HomeCards';
<HomeCards />
```

---

## 23. [55:14] - JobListings Component

Create `src/components/JobListings.jsx`. Initially uses a **local JSON file** (`jobs.json`) before switching to the JSON Server API later.

```jsx
import JobListing from './JobListing';
import jobs from '../jobs.json'; // temporary, later replaced by fetch

const JobListings = () => {
  return (
    <section className="bg-blue-50 px-4 py-10">
      <div className="container-xl lg:container m-auto">
        <h2 className="text-3xl font-bold text-indigo-500 mb-6 text-center">
          Recent Jobs
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {jobs.map((job) => (
            <JobListing key={job.id} job={job} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default JobListings;
```

---

## 24. [58:50] - Create Lists With map()

- `.map()` transforms each item of an array into a JSX element.
- **Always add a unique `key`** — React uses this internally to efficiently track/re-render list items.
- Prefer a **stable unique ID** from your data (`job.id`) over array index when the list can be reordered/filtered.

```jsx
{jobs.map((job) => (
  <JobListing key={job.id} job={job} />
))}
```

---

## 25. [1:03:20] - Single JobListing Component

`src/components/JobListing.jsx` — receives a single `job` object as a prop and renders a card:

```jsx
import { useState } from 'react';
import { FaMapMarker } from 'react-icons/fa';

const JobListing = ({ job }) => {
  const [showFullDescription, setShowFullDescription] = useState(false);

  let description = job.description;
  if (!showFullDescription) {
    description = description.substring(0, 90) + '...';
  }

  return (
    <div className="bg-white rounded-xl shadow-md relative">
      <div className="p-4">
        <div className="mb-6">
          <div className="text-gray-600 my-2">{job.type}</div>
          <h3 className="text-xl font-bold">{job.title}</h3>
        </div>

        <div className="mb-5">{description}</div>

        <button
          onClick={() => setShowFullDescription((prevState) => !prevState)}
          className="text-indigo-500 mb-5 hover:text-indigo-600"
        >
          {showFullDescription ? 'Less' : 'More'}
        </button>

        <h3 className="text-indigo-500 mb-2">{job.salary} / Year</h3>

        <div className="border border-gray-100 mb-5"></div>

        <div className="flex flex-col lg:flex-row justify-between mb-4">
          <div className="text-orange-700 mb-3">
            <FaMapMarker className="inline text-lg mb-1 mr-1" />
            {job.location}
          </div>
          <a
            href={`/jobs/${job.id}`}
            className="h-[36px] bg-indigo-500 hover:bg-indigo-600 text-white px-3 py-2 rounded-lg text-sm text-center"
          >
            Read More
          </a>
        </div>
      </div>
    </div>
  );
};

export default JobListing;
```

---

## 26. [1:05:49] - Limit Jobs to 3

On the homepage, only show a *preview* (3 jobs) rather than the whole list. Approach evolves over the video into an `isHome` boolean prop:

```jsx
const JobListings = ({ isHome = false }) => {
  const jobListings = isHome ? jobs.slice(0, 3) : jobs;

  return (
    <section className="bg-blue-50 px-4 py-10">
      <div className="container-xl lg:container m-auto">
        <h2 className="text-3xl font-bold text-indigo-500 mb-6 text-center">
          {isHome ? 'Recent Jobs' : 'Browse Jobs'}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {jobListings.map((job) => (
            <JobListing key={job.id} job={job} />
          ))}
        </div>
      </div>
    </section>
  );
};
```
Usage:
```jsx
// HomePage.jsx
<JobListings isHome={true} />

// JobsPage.jsx
<JobListings />  {/* isHome defaults to false */}
```

> Later (section 44), this same "3 vs all" idea is re-implemented at the **API/fetch level** using a `?_limit=3` query string instead of `.slice()`.

---

## 27. [1:07:50] - useState() Hook & Desc Toggle

- `useState(initialValue)` returns `[value, setValue]`.
- Used here to toggle between truncated and full job description text.

```jsx
const [showFullDescription, setShowFullDescription] = useState(false);
```

- When `showFullDescription` is `true` → show full text & button says "Less".
- When `false` → show truncated text & button says "More".
- **Key insight demonstrated:** changing state value re-renders **only that instance** of the component — clicking "More" on one job card doesn't affect other job cards, because each has its **own independent state**.

---

## 28. [1:13:07] - Creating an Event

- React events are **camelCase** (`onClick`, `onChange`, `onSubmit`) — unlike vanilla JS/HTML's all-lowercase attributes.
- **Never call the state setter directly during render** — wrap it in a function reference or arrow function, or it fires immediately on every render instead of on click:

```jsx
// ❌ WRONG - calls immediately on render
<button onClick={setShowFullDescription(!showFullDescription)}>

// ✅ CORRECT - only calls when clicked
<button onClick={() => setShowFullDescription(!showFullDescription)}>
```

---

## 29. [1:14:20] - Updating Component State

Two ways to update state with a setter function:

**1. Direct new value:**
```jsx
setShowFullDescription(!showFullDescription);
```

**2. Functional updater (safer — receives the previous state):**
```jsx
setShowFullDescription((prevState) => !prevState);
```

> The **functional updater form is recommended** for toggles/increments because it guarantees you're operating on the latest state, avoiding stale-state bugs (especially important when multiple state updates could batch together).

---

## 30. [1:16:00] - React Icons Package

```bash
npm install react-icons
```

- Gives access to Font Awesome, Material Icons, and many other icon sets as React components.
- Icons are imported per-set, e.g. Font Awesome icons come from `react-icons/fa`.

```jsx
import { FaMapMarker } from 'react-icons/fa';

<FaMapMarker className="inline text-lg mb-1 mr-1 text-orange-700" />
```

---

## 31. [1:18:00] - React Router Setup

```bash
npm install react-router-dom
```

> **Important: it's `react-router-dom`, not `react-router`**, for web apps.

- React Router provides multi-page routing capability that React itself (a library, not a framework) doesn't include out of the box.
- Key imports used throughout: `createBrowserRouter`, `createRoutesFromElements`, `RouterProvider`, `Route`, `Outlet`, `Link`, `NavLink`, `useParams`, `useNavigate`, `useLoaderData`.

---

## 32. [1:20:21] - Create Routes From Elements

In `App.jsx`, build the router above the `return`:

```jsx
import {
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
  Route,
} from 'react-router-dom';

const App = () => {
  const router = createBrowserRouter(
    createRoutesFromElements(
      <Route path="/" element={<h1>My App</h1>} />
    )
  );

  return <RouterProvider router={router} />;
};

export default App;
```

- `path="/about"` would render for `/about`, etc. — routes map a **URL path** to an **element** (a component).

---

## 33. [1:21:36] - Router Provider

- `RouterProvider` is what actually **activates** the router created via `createBrowserRouter` — without it, routes won't render at all.
- The `App` component's entire `return` becomes just:

```jsx
return <RouterProvider router={router} />;
```

---

## 34. [1:22:36] - Homepage Component/Route

- Create a `src/pages/` folder (separate from `src/components/`) — pages are still components, but organized separately since they represent whole routes/screens.

```jsx
// pages/HomePage.jsx
const HomePage = () => {
  return <div>Homepage</div>;
};

export default HomePage;
```

```jsx
// App.jsx
import HomePage from './pages/HomePage';

<Route index element={<HomePage />} />
```

> `index` is used instead of `path="/"` for the default/root route of its parent.

Then build out `HomePage.jsx` with the actual homepage content:

```jsx
// pages/HomePage.jsx
import Hero from '../components/Hero';
import HomeCards from '../components/HomeCards';
import JobListings from '../components/JobListings';

const HomePage = () => {
  return (
    <>
      <Hero />
      <HomeCards />
      <JobListings isHome={true} />
    </>
  );
};

export default HomePage;
```

---

## 35. [1:24:40] - Layouts

Elements you want on **every page** (Navbar, Footer) shouldn't be manually imported into every single page — use a **layout** with a parent route + `<Outlet />`.

```jsx
// layouts/MainLayout.jsx
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';

const MainLayout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
    </>
  );
};

export default MainLayout;
```

```jsx
// App.jsx
import MainLayout from './layouts/MainLayout';

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<MainLayout />}>
      <Route index element={<HomePage />} />
      {/* nested (child) routes go here */}
    </Route>
  )
);
```

- **`<Outlet />`** is where React Router injects whichever **child route's element** matches the current URL.
- Any route nested *inside* the `path="/"` route now automatically renders inside `MainLayout` (with the Navbar showing above it).

---

## 36. [1:29:06] - Jobs Page Component/Route

```jsx
// pages/JobsPage.jsx
import JobListings from '../components/JobListings';

const JobsPage = () => {
  return (
    <section className="bg-blue-50 px-4 py-6">
      <JobListings />
    </section>
  );
};

export default JobsPage;
```

```jsx
// App.jsx
import JobsPage from './pages/JobsPage';

<Route path="/jobs" element={<JobsPage />} />
```

- Since `isHome` defaults to `false` in `JobListings`, this page automatically shows **all** jobs, titled "Browse Jobs".

---

## 37. [1:30:50] - Link Component

- Never use plain `<a href="...">` for internal navigation in a React Router app — it causes a **full page reload**. Use React Router's `<Link>` instead for **client-side navigation** (no reload, keeps SPA fast).

```jsx
import { Link } from 'react-router-dom';

<Link to="/jobs">Jobs</Link>
```

- Update the "Read More" button and nav links from `<a href>` to `<Link to>` throughout `Navbar`, `JobListing`, `HomeCards`, etc.

---

## 38. [1:34:20] - Custom 404 Page

```jsx
// pages/NotFoundPage.jsx
const NotFoundPage = () => {
  return (
    <div className="text-center py-20">
      <h1 className="text-6xl font-bold mb-4">404 Not Found</h1>
      <p className="text-xl mb-5">This page does not exist</p>
      <Link to="/" className="text-indigo-500 hover:text-indigo-600">
        Go Back
      </Link>
    </div>
  );
};

export default NotFoundPage;
```

```jsx
// App.jsx — catch-all route
<Route path="*" element={<NotFoundPage />} />
```

- `path="*"` matches any URL that didn't match an earlier route.

---

## 39. [1:36:55] - Active Links With NavLink

- `NavLink` behaves like `Link` but **automatically knows if it matches the current route**, letting you conditionally style the "active" page link (e.g., highlight current nav item).

```jsx
import { NavLink } from 'react-router-dom';

const linkClass = ({ isActive }) =>
  isActive
    ? 'bg-black text-white rounded-md px-3 py-2'
    : 'text-white rounded-md px-3 py-2 hover:bg-gray-900 hover:text-white';

<NavLink to="/" className={linkClass}>Home</NavLink>
<NavLink to="/jobs" className={linkClass}>Jobs</NavLink>
<NavLink to="/add-job" className={linkClass}>Add Job</NavLink>
```

- `className` can accept a **function** that receives `{ isActive }` and returns the class string conditionally — cleaner than duplicating the ternary on every link.

---

## 40. [1:41:00] - Conditional Rendering

Recap/applied summary of JSX conditionals used across the app so far:
- Ternary `cond ? A : B` for either/or UI (e.g., isHome title text, NavLink active class).
- `&&` for show/hide UI (e.g., loading spinner).
- Both patterns rely on JSX expressions being embedded in `{ }`.

---

## 41. [1:43:10] - JSON Server Setup

**JSON Server** = a library that spins up a **fake full REST API** (GET/POST/PUT/PATCH/DELETE) from a single JSON file — no real backend code required.

1. Format your data file (`jobs.json`) as an **object with a named array** (not just a bare array), since JSON Server needs a "resource name":

```json
{
  "jobs": [
    {
      "id": "1",
      "title": "Senior React Developer",
      "type": "Full-Time",
      "description": "We are seeking a talented Front-End Developer...",
      "location": "Boston, MA",
      "salary": "$70K - $80K",
      "company": {
        "name": "NewTek Solutions",
        "description": "NewTek Solutions is a leading technology solutions provider...",
        "contactEmail": "contact@newteksolutions.com",
        "contactPhone": "555-555-5555"
      }
    }
  ]
}
```

2. Install as a **dev dependency**:
```bash
npm install -D json-server
```

3. Add an npm script in `package.json`:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "server": "json-server --watch data/jobs.json --port 8000"
  }
}
```

4. Run it in a **separate terminal** (alongside the Vite dev server):
```bash
npm run server
```
- This gives a live REST endpoint, e.g. `http://localhost:8000/jobs` (list) and `http://localhost:8000/jobs/1` (single item).
- Full CRUD works instantly: GET, POST, PUT, DELETE all hit this file — writes actually mutate the JSON file on disk.

---

## 42. [1:47:00] - useEffect() & Data Fetching

Replace the static `import jobs from '../jobs.json'` with a **real fetch** inside `JobListings.jsx`.

```jsx
import { useState, useEffect } from 'react';
import JobListing from './JobListing';
import Spinner from './Spinner';

const JobListings = ({ isHome = false }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJobs = async () => {
      const apiUrl = isHome
        ? '/api/jobs?_limit=3'
        : '/api/jobs';
      try {
        const res = await fetch(apiUrl);
        const data = await res.json();
        setJobs(data);
      } catch (error) {
        console.log('Error fetching data', error);
      } finally {
        setLoading(false);
      }
    };

    fetchJobs();
  }, []); // empty dependency array = run once, on mount

  return (
    <section className="bg-blue-50 px-4 py-10">
      <div className="container-xl lg:container m-auto">
        <h2 className="text-3xl font-bold text-indigo-500 mb-6 text-center">
          {isHome ? 'Recent Jobs' : 'Browse Jobs'}
        </h2>

        {loading ? (
          <Spinner loading={loading} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {jobs.map((job) => (
              <JobListing key={job.id} job={job} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
};

export default JobListings;
```

**`useEffect` mechanics explained:**
- Signature: `useEffect(functionToRun, dependencyArray)`.
- The dependency array controls **when** the effect re-runs:
  - `[]` (empty array) → run **once**, when the component first mounts.
  - `[name]` → re-run **whenever `name` changes**.
  - **Omitted entirely** → runs after **every** render (usually **not** what you want — risk of infinite loops, especially if the effect itself changes state that's a dependency).
- You **cannot** mark the `useEffect` callback itself `async` directly (`useEffect(async () => {...})` is invalid) — instead, **define a separate async function inside** the effect and **call it**.
- **try/catch/finally pattern** is the recommended way to fetch:
  - `try` → do the fetch + set data state
  - `catch` → log/handle errors
  - `finally` → always turn off `loading`, whether success or failure

---

## 43. [1:53:07] - Loading Spinner

```bash
npm install react-spinners
```

```jsx
// components/Spinner.jsx
import ClipLoader from 'react-spinners/ClipLoader';

const override = {
  display: 'block',
  margin: '100px auto',
};

const Spinner = ({ loading }) => {
  return (
    <ClipLoader
      color="#4338ca"
      loading={loading}
      cssOverride={override}
      size={150}
    />
  );
};

export default Spinner;
```

Usage (already shown above in `JobListings.jsx`):
```jsx
{loading ? <Spinner loading={loading} /> : ( ...jobs grid... )}
```

> Gotcha noted in the video: if the spinner doesn't visually center, check that the wrapping `<div>` (e.g., the grid container) isn't interfering — the override's `margin: 100px auto` needs the spinner's parent to be a normal block-level container, not something like `display: grid` fighting the centering.

---

## 44. [1:51:06] - Conditional Fetching

To show **3 jobs on Home** vs **all jobs on the Jobs page**, but *not* duplicate logic with `.slice()`, do it at the **API URL level** using JSON Server's built-in `_limit` query param:

```jsx
const apiUrl = isHome ? '/api/jobs?_limit=3' : '/api/jobs';
```

- This way, JSON Server itself only returns 3 records for the homepage request, and all records for `/jobs`.

---

## 45. [1:59:45] - Proxying

Problem: hardcoding `http://localhost:8000` in every fetch call breaks once deployed (there's no `localhost:8000` in production).

**Solution: configure a dev-server proxy in `vite.config.js`** so any request to `/api/...` gets forwarded to the JSON Server backend during development:

```js
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});
```

- Now every fetch call in the app just uses the **relative path** `/api/jobs` (as shown in the `useEffect` code above) instead of the full `http://localhost:8000/jobs` URL.
- When you eventually deploy with a real backend, you'd only need to update the **one place** doing the actual production API base URL (or your hosting config), not every fetch call in the app.

---

## 46. [2:03:38] - Single Job Page

```jsx
// pages/JobPage.jsx
const JobPage = () => {
  return <div>Job Page</div>;
};

export default JobPage;
```

```jsx
// App.jsx
import JobPage from './pages/JobPage';

<Route path="/jobs/:id" element={<JobPage />} />
```

- `:id` in the path is a **dynamic segment/param** — `:` signals "this part of the URL is a variable, not a literal string."
- Update the "Read More" link in `JobListing.jsx` to point to `/jobs/${job.id}`.

---

## 47. [2:09:04] - useParams() to Get ID

**First approach shown: `useEffect` + `useParams` (later replaced by a data loader in the next section):**

```jsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Spinner from '../components/Spinner';

const JobPage = () => {
  const { id } = useParams();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const res = await fetch(`/api/jobs/${id}`);
        const data = await res.json();
        setJob(data);
      } catch (error) {
        console.log('Error fetching job', error);
      } finally {
        setLoading(false);
      }
    };
    fetchJob();
  }, []);

  return (
    <>
      {!loading && job ? (
        <h1>{job.title}</h1>
      ) : (
        <Spinner loading={loading} />
      )}
    </>
  );
};

export default JobPage;
```

- `useParams()` returns an object of all dynamic segments in the current matched route — here `{ id: '3' }` for a URL like `/jobs/3`.

---

## 48. [2:12:25] - Data Loaders

React Router (not React itself) provides **loaders** — a way to fetch data **before** a route renders, avoiding the `useState`/`useEffect` boilerplate entirely, and letting you **export/reuse the fetch logic** in other routes too (e.g., the Edit page reuses the Job page's loader).

```jsx
// pages/JobPage.jsx
import { useParams, useLoaderData } from 'react-router-dom';

const JobPage = () => {
  const { id } = useParams(); // still handy if needed elsewhere
  const job = useLoaderData();

  return (
    <>
      {/* full job details JSX using `job` */}
    </>
  );
};

// Loader function — a React Router feature, defined & exported from this file
const jobLoader = async ({ params }) => {
  const res = await fetch(`/api/jobs/${params.id}`);
  const data = await res.json();
  return data;
};

export { JobPage as default, jobLoader };
```

```jsx
// App.jsx
import JobPage, { jobLoader } from './pages/JobPage';

<Route
  path="/jobs/:id"
  element={<JobPage />}
  loader={jobLoader}
/>
```

- The route config passes the loader in via the `loader` prop.
- Inside the component, `useLoaderData()` retrieves whatever the loader function **returned**.
- Net effect: **no `useState`, no `useEffect`, no manual loading spinner needed** for this page — React Router handles data-fetching timing (it won't render the route element until the loader resolves).

---

## 49. [2:16:36] - Single Job Output

Full `JobPage.jsx` rendering real data (icons + Link for back/edit buttons):

```jsx
import { Link, useLoaderData } from 'react-router-dom';
import { FaArrowLeft, FaMapMarker } from 'react-icons/fa';

const JobPage = () => {
  const job = useLoaderData();

  return (
    <>
      <section>
        <div className="container m-auto py-6 px-6">
          <Link
            to="/jobs"
            className="text-indigo-500 hover:text-indigo-600 flex items-center"
          >
            <FaArrowLeft className="mr-2" /> Back to Job Listings
          </Link>
        </div>
      </section>

      <section className="bg-indigo-50">
        <div className="container m-auto py-10 px-6 grid grid-cols-1 md:grid-cols-70/30 gap-6">
          <main>
            <div className="bg-white p-6 rounded-lg shadow-md text-center md:text-left">
              <div className="text-gray-500 mb-4">{job.type}</div>
              <h1 className="text-3xl font-bold mb-4">{job.title}</h1>
              <div className="text-orange-700 mb-4 flex align-middle justify-center md:justify-start">
                <FaMapMarker className="text-orange-700 mr-1" />
                <p>{job.location}</p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md mt-6">
              <h3 className="text-indigo-800 text-lg font-bold mb-6">
                Job Description
              </h3>
              <p className="mb-4">{job.description}</p>
              <h3 className="text-indigo-800 text-lg font-bold mb-2">
                Salary
              </h3>
              <p className="mb-4">{job.salary} / Year</p>
            </div>
          </main>

          <aside>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-bold mb-6">Company Info</h3>
              <h2 className="text-2xl">{job.company.name}</h2>
              <p className="my-2">{job.company.description}</p>
              <hr className="my-4" />
              <h3 className="text-xl">Contact Email:</h3>
              <p className="my-2 bg-indigo-100 p-2 font-bold">
                {job.company.contactEmail}
              </p>
              <h3 className="text-xl">Contact Phone:</h3>
              <p className="my-2 bg-indigo-100 p-2 font-bold">
                {job.company.contactPhone}
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md mt-6">
              <h3 className="text-xl font-bold mb-6">Manage Job</h3>
              <Link
                to={`/edit-job/${job.id}`}
                className="bg-indigo-500 hover:bg-indigo-600 text-white text-center font-bold py-2 px-4 rounded-full w-full inline-block"
              >
                Edit Job
              </Link>
              <button className="bg-red-500 hover:bg-red-600 text-white text-center font-bold py-2 px-4 rounded-full w-full mt-4 block">
                Delete Job
              </button>
            </div>
          </aside>
        </div>
      </section>
    </>
  );
};

export default JobPage;
```

- All hardcoded HTML (e.g., "senior React developer", static location, static company info) is replaced with `job.title`, `job.location`, `job.company.name`, `job.company.description`, `job.company.contactEmail`, `job.company.contactPhone`, etc.

---

## 50. [2:22:00] - Add Job Page

```jsx
// pages/AddJobPage.jsx
const AddJobPage = () => {
  return <div>Add Job Page</div>;
};

export default AddJobPage;
```

```jsx
// App.jsx
import AddJobPage from './pages/AddJobPage';

<Route path="/add-job" element={<AddJobPage />} />
```

- The theme's static `add-job.html` form markup is copied in, all `class` → `className`, and all `for="..."` label attributes → `htmlFor="..."`.

---

## 51. [2:23:40] - Working With Forms

**Core pattern used: one `useState` per form field** (a "controlled component" for every input) — instead of a single big state object, for simplicity in this course.

```jsx
import { useState } from 'react';

const AddJobPage = () => {
  const [title, setTitle] = useState('');
  const [type, setType] = useState('Full-Time');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [salary, setSalary] = useState('Under $50K');
  const [companyName, setCompanyName] = useState('');
  const [companyDescription, setCompanyDescription] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [contactPhone, setContactPhone] = useState('');

  return (
    <section className="bg-indigo-50">
      <div className="container m-auto max-w-2xl py-24">
        <div className="bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0">
          <form>
            <h2 className="text-3xl text-center font-semibold mb-6">Add Job</h2>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">
                Job Type
              </label>
              <select
                className="border rounded w-full py-2 px-3"
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                <option value="Full-Time">Full-Time</option>
                <option value="Part-Time">Part-Time</option>
                <option value="Remote">Remote</option>
                <option value="Internship">Internship</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Job Listing Name</label>
              <input
                type="text"
                className="border rounded w-full py-2 px-3 mb-2"
                placeholder="eg. Beautiful Apartment In Miami"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Description</label>
              <textarea
                className="border rounded w-full py-2 px-3"
                rows="4"
                placeholder="Add any job duties, expectations, requirements, etc"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              ></textarea>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Salary</label>
              <select
                className="border rounded w-full py-2 px-3"
                value={salary}
                onChange={(e) => setSalary(e.target.value)}
              >
                <option value="Under $50K">Under $50K</option>
                <option value="$50K - $60K">$50K - $60K</option>
                <option value="$60K - $70K">$60K - $70K</option>
                <option value="$70K - $80K">$70K - $80K</option>
                <option value="$80K - $90K">$80K - $90K</option>
                <option value="$90K - $100K">$90K - $100K</option>
                <option value="$100K - $125K">$100K - $125K</option>
                <option value="$125K - $150K">$125K - $150K</option>
                <option value="$150K - $175K">$150K - $175K</option>
                <option value="$175K - $200K">$175K - $200K</option>
                <option value="Over $200K">Over $200K</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Location</label>
              <input
                type="text"
                className="border rounded w-full py-2 px-3 mb-2"
                placeholder="Company Location"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                required
              />
            </div>

            <h3 className="text-2xl mb-5">Company Info</h3>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Company Name</label>
              <input
                type="text"
                className="border rounded w-full py-2 px-3"
                placeholder="Company Name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Company Description</label>
              <textarea
                className="border rounded w-full py-2 px-3"
                rows="4"
                placeholder="What does your company do?"
                value={companyDescription}
                onChange={(e) => setCompanyDescription(e.target.value)}
              ></textarea>
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Contact Email</label>
              <input
                type="email"
                className="border rounded w-full py-2 px-3"
                placeholder="Email address for applicants"
                value={contactEmail}
                onChange={(e) => setContactEmail(e.target.value)}
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-bold mb-2">Contact Phone</label>
              <input
                type="tel"
                className="border rounded w-full py-2 px-3"
                placeholder="Optional phone for applicants"
                value={contactPhone}
                onChange={(e) => setContactPhone(e.target.value)}
              />
            </div>

            <div>
              <button
                className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded-full w-full focus:outline-none focus:shadow-outline"
                type="submit"
              >
                Add Job
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
};

export default AddJobPage;
```

- **Controlled input pattern:** every input's `value` is tied to a piece of state, and every input has an `onChange` handler that calls the setter with `e.target.value`.
- If you set `value={...}` **without** `onChange`, React throws a console warning: *"You provided a `value` prop to a form field without an `onChange` handler."*
- **Select defaults:** if you want a `<select>` to show a default option, the initial `useState` value must **exactly match** one of the `<option value="...">` strings.
- 💡 Tip mentioned: the **"Multiple Cursor Case Preserve"** VS Code extension helps when using multi-cursor renaming (`Cmd/Ctrl+Shift+L`) so that case (upper/lower) is preserved correctly across all matches.

---

## 52. [2:30:05] - Form Submission

```jsx
<form onSubmit={submitForm}>
```

```jsx
const submitForm = (e) => {
  e.preventDefault(); // stop default browser form POST/page reload

  const newJob = {
    title,
    type,
    location,
    description,
    salary,
    company: {
      name: companyName,
      description: companyDescription,
      contactEmail,
      contactPhone,
    },
  };

  addJobSubmit(newJob); // passed down from parent as a prop (see below)
};
```

- `e.preventDefault()` is required — otherwise the browser tries to submit the form the "old" HTML way (full page reload / navigation).
- The `newJob` object is **shaped to match the API's expected structure** — flat top-level fields, plus a nested `company` object (mirroring `jobs.json`'s schema).

---

## 53. [2:35:27] - Pass Function as Prop

Pattern used throughout the CRUD flow: **keep all fetch/network requests centralized in `App.jsx`**, and pass down handler functions as props into each page, which then call them.

```jsx
// App.jsx
const addJob = async (newJob) => {
  const res = await fetch('/api/jobs', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newJob),
  });
  return;
};
```

```jsx
<Route
  path="/add-job"
  element={<AddJobPage addJobSubmit={addJob} />}
/>
```

```jsx
// pages/AddJobPage.jsx
const AddJobPage = ({ addJobSubmit }) => {
  // ...
  const submitForm = (e) => {
    e.preventDefault();
    const newJob = { /* ...as above... */ };
    addJobSubmit(newJob);
    return navigate('/jobs');
  };
  // ...
};
```

- Conceptually: the **child page** ("down" in the tree) receives a function reference from the **parent App** ("up" in the tree) as a prop, and **calls** it when the form submits — this lets the parent own the actual network logic/state while the child just triggers it.
- Instructor's honest note: this "lifting state up" / "passing callbacks down" pattern can be confusing at first, but it's a fundamental React pattern for **child-to-parent communication**.
- For a small app like this, centralizing requests in `App.jsx` is a lightweight alternative to introducing **Context API** or **Redux** — those would be preferable at larger scale.

---

## 54. [2:39:32] - POST Request to Add Job

Full working `addJob` implementation:

```jsx
// App.jsx
const addJob = async (newJob) => {
  const res = await fetch('/api/jobs', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(newJob),
  });
  return;
};
```

```jsx
// pages/AddJobPage.jsx
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

const submitForm = (e) => {
  e.preventDefault();
  const newJob = { title, type, location, description, salary,
    company: { name: companyName, description: companyDescription, contactEmail, contactPhone } };

  addJobSubmit(newJob);

  return navigate('/jobs');
};
```

- **`useNavigate()`** (from `react-router-dom`) returns a `navigate` function used for **programmatic redirects** (as opposed to `<Link>`, which is for clickable navigation).
- After a successful POST, the user is redirected to `/jobs` where the new listing now appears (since JSON Server persisted it to the actual `jobs.json` file on disk).

---

## 55. [2:41:45] - Delete Job Button/Function

Centralize the delete handler in `App.jsx`, pass it down to `JobPage`, and wire up a confirmation dialog:

```jsx
// App.jsx
const deleteJob = async (id) => {
  const res = await fetch(`/api/jobs/${id}`, {
    method: 'DELETE',
  });
  return;
};
```

```jsx
<Route
  path="/jobs/:id"
  element={<JobPage deleteJob={deleteJob} />}
  loader={jobLoader}
/>
```

```jsx
// pages/JobPage.jsx
import { useNavigate } from 'react-router-dom';

const JobPage = ({ deleteJob }) => {
  const navigate = useNavigate();
  const job = useLoaderData();

  const onDeleteClick = (jobId) => {
    const confirm = window.confirm(
      'Are you sure you want to delete this listing?'
    );
    if (!confirm) return;

    deleteJob(jobId);
    toast.success('Job deleted successfully'); // see Toastify section below
    navigate('/jobs');
  };

  return (
    <>
      {/* ...job details... */}
      <button
        onClick={() => onDeleteClick(job.id)}
        className="bg-red-500 hover:bg-red-600 text-white text-center font-bold py-2 px-4 rounded-full w-full mt-4 block"
      >
        Delete Job
      </button>
    </>
  );
};
```

- **`window.confirm(message)`** is a native browser API — returns `true`/`false` based on user's OK/Cancel choice. Used here as a simple safety check before destructive actions.

---

## 56. [2:45:12] - DELETE Request to Remove Job

Final `deleteJob` function in `App.jsx` (as shown above):

```jsx
const deleteJob = async (id) => {
  const res = await fetch(`/api/jobs/${id}`, {
    method: 'DELETE',
  });
  return;
};
```

- Uses the **`DELETE` HTTP method** — no `headers`/`body` needed (unlike POST/PUT), since you're just targeting a resource by its URL/ID.
- JSON Server removes the matching object from the underlying `jobs.json` file.

---

## 57. [2:46:50] - React Toastify Package

```bash
npm install react-toastify
```

**Global setup — add the container once, in the layout (so toasts can appear from any page):**

```jsx
// layouts/MainLayout.jsx
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const MainLayout = () => {
  return (
    <>
      <Navbar />
      <Outlet />
      <ToastContainer />
    </>
  );
};

export default MainLayout;
```

**Usage anywhere you need a toast — import `toast` and call it:**

```jsx
import { toast } from 'react-toastify';

toast.success('Job added successfully');
toast.success('Job deleted successfully');
toast.error('Something went wrong'); // for errors
```

- `ToastContainer` is positioned `absolute` by default (renders in a corner) — position/behavior is configurable via props if needed.
- Used after **Add** (in `AddJobPage`, right before the redirect) and after **Delete** (in `JobPage`, right before the redirect) to give users visible confirmation feedback.

---

## 58. [2:50:08] - Edit Job Page/Form

```jsx
// pages/EditJobPage.jsx
```

```jsx
// App.jsx — reuse the SAME jobLoader used for JobPage, since editing needs the same data
import EditJobPage from './pages/EditJobPage';

<Route
  path="/edit-job/:id"
  element={<EditJobPage updateJobSubmit={updateJob} />}
  loader={jobLoader}
/>
```

Full component — copy the Add Job form, but **pre-fill state from `useLoaderData()`**:

```jsx
import { useState } from 'react';
import { useNavigate, useParams, useLoaderData } from 'react-router-dom';
import { toast } from 'react-toastify';

const EditJobPage = ({ updateJobSubmit }) => {
  const job = useLoaderData();

  const [title, setTitle] = useState(job.title);
  const [type, setType] = useState(job.type);
  const [location, setLocation] = useState(job.location);
  const [description, setDescription] = useState(job.description);
  const [salary, setSalary] = useState(job.salary);
  const [companyName, setCompanyName] = useState(job.company.name);
  const [companyDescription, setCompanyDescription] = useState(job.company.description);
  const [contactEmail, setContactEmail] = useState(job.company.contactEmail);
  const [contactPhone, setContactPhone] = useState(job.company.contactPhone);

  const { id } = useParams();
  const navigate = useNavigate();

  const submitForm = (e) => {
    e.preventDefault();

    const updatedJob = {
      id,
      title,
      type,
      location,
      description,
      salary,
      company: {
        name: companyName,
        description: companyDescription,
        contactEmail,
        contactPhone,
      },
    };

    updateJobSubmit(updatedJob);
    toast.success('Job updated successfully');
    return navigate(`/jobs/${id}`);
  };

  return (
    <section className="bg-indigo-50">
      <div className="container m-auto max-w-2xl py-24">
        <div className="bg-white px-6 py-8 mb-4 shadow-md rounded-md border m-4 md:m-0">
          <form onSubmit={submitForm}>
            <h2 className="text-3xl text-center font-semibold mb-6">
              Update Job
            </h2>
            {/* same fields as AddJobPage, wired to the state above */}
          </form>
        </div>
      </div>
    </section>
  );
};

export default EditJobPage;
```

- Because this route also has `loader={jobLoader}`, `useLoaderData()` gives it the existing job's data — used to **initialize every field's state** with the current values, so the form opens pre-filled.
- `useParams()` is still needed here (separately from the loader) to grab the `id` for constructing the `updatedJob` object and for the PUT request URL.

---

## 59. [2:56:05] - Update Form Submission

- Reuses the same submit pattern as Add Job, but:
  - Includes the job's **`id`** in the payload (needed for the PUT URL).
  - Calls **`updateJobSubmit(updatedJob)`** (passed as a prop) instead of `addJobSubmit`.
  - Shows a **"Job updated successfully"** toast.
  - **Redirects to `/jobs/${id}`** (the single job page) instead of `/jobs`, so the user immediately sees their update.

```jsx
const submitForm = (e) => {
  e.preventDefault();
  const updatedJob = { id, title, type, location, description, salary,
    company: { name: companyName, description: companyDescription, contactEmail, contactPhone } };

  updateJobSubmit(updatedJob);
  toast.success('Job updated successfully');
  return navigate(`/jobs/${id}`);
};
```

---

## 60. [2:58:54] - PUT Request to Update Job

```jsx
// App.jsx
const updateJob = async (job) => {
  const res = await fetch(`/api/jobs/${job.id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(job),
  });
  return;
};
```

```jsx
<Route
  path="/edit-job/:id"
  element={<EditJobPage updateJobSubmit={updateJob} />}
  loader={jobLoader}
/>
```

- **`PUT`** = the correct REST method for a full update/replace of an existing resource (contrast with `POST` for create, `DELETE` for remove).
- The URL includes the specific job's ID: `` `/api/jobs/${job.id}` ``.
- At this point the app has **full CRUD**: Create (POST), Read (GET, both list & single via loaders/fetch), Update (PUT), Delete (DELETE) — the only thing explicitly out of scope is **authentication**.

---

## 61. [3:02:10] - Build Static Assets For Production

```bash
npm run build
```

- Runs Vite's production build → outputs a `dist/` folder containing optimized, minified static assets (this is what you deploy).
- You can verify build mode via React DevTools — the extension icon/banner will say the page is using the **development build** while running `npm run dev`, vs the **production build** once served from `dist/`.

**Preview the production build locally:**
```bash
npm run preview
```
- Runs on a different port (e.g., `4173`) and serves the actual `dist/` build — confirms React DevTools shows "production build."

**Deployment notes:**
- The `dist/` folder can be deployed to **any static host** (Netlify, Vercel, GitHub Pages, S3, etc.) since this is a plain SPA.
- **Caveat:** deploying as-is won't show real job data, because `json-server` is only running **locally** — for a real production app you'd need an actual backend (Express, Django, Laravel, or any REST API), but **none of the front-end React code changes** — it's designed to work identically against JSON Server or a real REST API, since both just expose standard REST endpoints.

---

## 62. Full Cheat Sheet / Quick Reference

### Hooks used in this project
| Hook | Purpose |
|---|---|
| `useState` | Local component state (form fields, toggles, fetched data, loading flags) |
| `useEffect` | Side effects (data fetching on mount) — superseded by loaders for route-level data in this app |
| `useParams` | Read dynamic route segments (`:id`) |
| `useNavigate` | Programmatic redirect after an action (submit, delete) |
| `useLoaderData` | Access data returned by a route's `loader` function |

### React Router pieces
| Piece | Purpose |
|---|---|
| `createBrowserRouter` | Creates the router instance |
| `createRoutesFromElements` | Lets you define routes using JSX `<Route>` elements |
| `RouterProvider` | Activates the router — replaces the app's whole `return` |
| `<Route path index element loader>` | Defines a route: URL, optional index flag, component, optional data loader |
| `<Outlet />` | Placeholder in a layout where the matched child route renders |
| `<Link to="...">` | Client-side navigation link (no full reload) |
| `<NavLink to="..." className={fn}>` | Like `Link`, but knows if it's the active route |

### npm packages installed during the course
```bash
npm install react-router-dom
npm install react-icons
npm install react-spinners
npm install react-toastify
npm install -D json-server
npm install -D tailwindcss postcss autoprefixer
```

### npm scripts (final `package.json`)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "server": "json-server --watch data/jobs.json --port 8000"
  }
}
```

### Folder structure (final)
```
src/
├── assets/images/
├── components/
│   ├── Navbar.jsx
│   ├── Hero.jsx
│   ├── Card.jsx
│   ├── HomeCards.jsx
│   ├── JobListings.jsx
│   ├── JobListing.jsx
│   └── Spinner.jsx
├── layouts/
│   └── MainLayout.jsx
├── pages/
│   ├── HomePage.jsx
│   ├── JobsPage.jsx
│   ├── JobPage.jsx        (exports jobLoader too)
│   ├── AddJobPage.jsx
│   ├── EditJobPage.jsx
│   └── NotFoundPage.jsx
├── App.jsx                 (router config + centralized CRUD fetch functions)
├── main.jsx
└── index.css
data/
└── jobs.json
```

### CRUD request map
| Action | Method | Endpoint | Where called from |
|---|---|---|---|
| List jobs (home, limited) | GET | `/api/jobs?_limit=3` | `JobListings` (`isHome=true`) |
| List jobs (all) | GET | `/api/jobs` | `JobListings` (`isHome=false`) |
| Get single job | GET | `/api/jobs/:id` | `jobLoader` (used by `JobPage` & `EditJobPage`) |
| Create job | POST | `/api/jobs` | `addJob` in `App.jsx`, called from `AddJobPage` |
| Update job | PUT | `/api/jobs/:id` | `updateJob` in `App.jsx`, called from `EditJobPage` |
| Delete job | DELETE | `/api/jobs/:id` | `deleteJob` in `App.jsx`, called from `JobPage` |

### Key JSX rules to remember
- `class` → `className`, `for` → `htmlFor`
- Comments: `{/* like this */}`
- All events camelCase: `onClick`, `onChange`, `onSubmit`
- Lists need a `key` prop
- Conditionals must be **expressions**: ternary (`? :`) or `&&`, not raw `if` blocks inline
- A component can only return **one root element** (use `<>...</>` Fragments to group siblings)

### Final summary of concepts covered
Components • Props (+ defaults, + children/wrapper components) • State (`useState`) • Hooks (`useEffect`, `useParams`, `useNavigate`, `useLoaderData`) • JSX • React Router (routes, layouts, links, active links, dynamic params, data loaders, 404s) • Controlled forms • REST CRUD against a mock API (JSON Server) • Dev-server proxying • Third-party packages (icons, spinners, toasts) • Production build & deployment considerations.

> Not covered (explicitly flagged as out of scope): Context API, Redux, authentication, TypeScript, React Suspense, React Query/SWR.
