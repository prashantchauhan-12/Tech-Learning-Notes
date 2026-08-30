# React Hooks — Complete Notes

## What Are Hooks?

Hooks are functions that let you use React features (state, lifecycle, context, refs, etc.) inside **functional components**.

**Story behind hooks:** Before hooks existed, only class components could hold state and use lifecycle methods. Developers found class components verbose and hard to reuse logic between. React introduced hooks so functional components could do everything class components could — in a simpler way.

> **In short:** Hooks are functions that make functional components behave like class components.

---

## 1. useState Hook

`useState` lets you add **state** (a variable that React tracks and re-renders on change) to a functional component.

### Basic Counter Example

```jsx
import React, { useState } from 'react';

const Counter = () => {
  const [counter, setCounter] = useState(0);

  const increaseCounter = () => {
    setCounter(counter + 1);
  };

  return (
    <div>
      <p>Counter: {counter}</p>
      <button onClick={increaseCounter}>Increase</button>
    </div>
  );
};

export default Counter;
```

- `useState(0)` returns an **array** with two items:
  1. The current value (`counter`)
  2. A function to update that value (`setCounter`)
- Array destructuring `const [counter, setCounter] = useState(0)` is the standard shorthand.
- You can use **multiple `useState` calls** in one component.

### Getting Value From an Input

```jsx
const [name, setName] = useState('');

<input
  type="text"
  onChange={(e) => setName(e.target.value)}
/>

<p>{name} has clicked {counter} times</p>
```

### useState With an Object

⚠️ **Common pitfall:** When state is an object, calling `setState({ counter: counter + 1 })` **replaces the entire object**, wiping out other keys (like `name`).

```jsx
const [details, setDetails] = useState({ counter: 0, name: '' });

// ❌ Wrong — this removes "name" from the object
const increaseCounter = () => {
  setDetails({ counter: details.counter + 1 });
};

// ✅ Correct — spread the previous state first
const increaseCounter = () => {
  setDetails((previous) => ({
    ...previous,
    counter: previous.counter + 1,
  }));
};
```

**Rule of thumb:** Whenever state is an object or array, spread the previous value (`...previous`) before overwriting specific keys.

### Recap

| Point | Detail |
|---|---|
| Purpose | Create state variables in functional components |
| Import | `import { useState } from 'react'` |
| Accepts | Any data type — boolean, number, string, object, array |
| Returns | `[currentValue, updateFunction]` |

---

## 2. useEffect Hook

`useEffect` is used to perform **side effects** — actions that reach outside the component, such as:
- Fetching data from an API
- Directly manipulating the DOM (`document`, `window`)
- Timers (`setTimeout`, `setInterval`)

```jsx
useEffect(callbackFunction, dependenciesArray);
```

- **First argument:** what to run (a function containing the side-effect logic)
- **Second argument (optional):** when to run it (an array of dependencies)

If you know class components, `useEffect` combines `componentDidMount`, `componentDidUpdate`, and `componentWillUnmount`.

### Variation 1 — No Dependency Array (runs on every render)

```jsx
useEffect(() => {
  document.title = `${count} new messages`;
});
```
Runs after **every** render/state change in the component.

### Variation 2 — Empty Dependency Array (runs once)

```jsx
useEffect(() => {
  document.title = `${count} new messages`;
}, []);
```
Runs **only once**, when the component first mounts. Great for one-time API calls.

### Variation 3 — Dependency Array With Variables (runs on specific changes)

```jsx
useEffect(() => {
  document.title = `${otherCount} new messages`;
}, [otherCount]);
```
Runs on first render **and** whenever `otherCount` changes. Multiple variables can be listed, separated by commas.

### Cleanup Function

Used to stop repeating side effects (like intervals or subscriptions) when the component unmounts or before the effect re-runs.

```jsx
useEffect(() => {
  const timer = setInterval(() => {
    console.log('tick');
  }, 1000);

  // cleanup — runs before the next effect execution and on unmount
  return () => {
    clearInterval(timer);
  };
}, []);
```

**Order of execution:** Every time the effect re-runs, React first calls the **previous cleanup function**, then runs the new effect callback.

```jsx
useEffect(() => {
  console.log('run effect', count);

  return () => {
    console.log('cleanup', count);
  };
}, [count]);
```

### Recap

| Variation | Dependency Array | Runs |
|---|---|---|
| No array | — | On every render/change |
| Empty array `[]` | `[]` | Only once, on mount |
| With variables | `[var1, var2]` | On mount + whenever listed variables change |

Cleanup is only needed when a side effect (interval, subscription, listener) must be disposed of.

---

## 3. useContext Hook

`useContext` manages **global data** across the app (theme, logged-in user, settings) without manually passing props down through every level (**prop drilling**).

### Problem It Solves

If `App → Feed → FollowingPost → SinglePost` all need `userDetails`, passing props manually through each layer is tedious. `useContext` lets any nested component access the data directly.

### 3 Steps to Use Context

**Step 1 — Create the Context**

```jsx
import { createContext } from 'react';

export const LoginContext = createContext();
```

**Step 2 — Provide the Context**

```jsx
function App() {
  return (
    <LoginContext.Provider value={true}>
      <Main />
    </LoginContext.Provider>
  );
}
```
Any component nested inside `<LoginContext.Provider>` (and its children) can access the value.

**Step 3 — Consume the Context**

```jsx
import { useContext } from 'react';
import { LoginContext } from '../App';

function SinglePost() {
  const login = useContext(LoginContext);
  console.log(login); // true
  return <div>{login ? 'Welcome back!' : 'Please log in'}</div>;
}
```

### Organizing Context (Best Practice)

Create a dedicated `context` folder with a provider component so `App.js` stays clean.

```jsx
// context/LoginContextProvider.js
import React, { createContext, useState } from 'react';

export const LoginContext = createContext();

const LoginContextProvider = (props) => {
  const [userDetails] = useState(true);

  return (
    <LoginContext.Provider value={userDetails}>
      {props.children}
    </LoginContext.Provider>
  );
};

export default LoginContextProvider;
```

```jsx
// App.js
import LoginContextProvider from './context/LoginContextProvider';

function App() {
  return (
    <LoginContextProvider>
      <Main />
    </LoginContextProvider>
  );
}
```

### Recap

- Use `useContext` for truly **global** data.
- Use plain **props** if data only needs to go to a direct child.
- 3 steps: `createContext()` → `<Context.Provider value={...}>` → `useContext(Context)`.

---

## 4. useRef Hook

`useRef` has two main uses:
1. Creating a **mutable variable** that persists across renders **without** causing a re-render.
2. Accessing **DOM elements** directly.

### Use Case 1 — Mutable Variable (Render Counter)

❌ Using `useState` for a render counter causes an **infinite loop**, because updating state triggers a re-render, which updates the counter again, forever.

```jsx
// ❌ Infinite loop
const [count, setCount] = useState(0);
useEffect(() => {
  setCount((prev) => prev + 1);
});
```

✅ `useRef` solves this because updating `.current` does **not** trigger a re-render.

```jsx
import { useRef, useEffect } from 'react';

const count = useRef(0);

useEffect(() => {
  count.current = count.current + 1;
});

// access value with count.current
```

`useRef(initialValue)` returns an object: `{ current: initialValue }`.

### Use Case 2 — Accessing DOM Elements

```jsx
import { useRef } from 'react';

const InputFocus = () => {
  const inputElement = useRef(null);

  const handleClick = () => {
    inputElement.current.style.width = '300px';
    inputElement.current.focus();
  };

  return (
    <div>
      <input ref={inputElement} type="text" />
      <button onClick={handleClick}>Style & Focus</button>
    </div>
  );
};
```

- Attach `ref={variableName}` to the JSX element.
- `inputElement.current` becomes the actual DOM node — you can call any native JS DOM method/property on it (`.style`, `.focus()`, `.value`, etc.), same as vanilla JavaScript.
- **Tip:** `console.log(inputElement)` in DevTools and expand the object to browse every available property/method on the element.

### Recap

| Feature | Detail |
|---|---|
| Purpose 1 | Mutable variable that doesn't trigger re-render |
| Purpose 2 | Direct access to DOM elements |
| Syntax | `const ref = useRef(initialValue)` |
| Access/update value | `ref.current` |

---

## 5. useReducer Hook

`useReducer` is a **state management tool** for complex state logic — useful when a component has many state variables and many ways to update them (an alternative to multiple `useState` calls).

```jsx
const [state, dispatch] = useReducer(reducerFunction, initialState);
```

- **First argument:** a reducer function that manages state transitions.
- **Second argument:** the initial state.
- **Returns:** `[currentState, dispatchFunction]` (same pattern as `useState`).

### Basic Counter Example

```jsx
import React, { useReducer } from 'react';

const initialState = { count: 0 };

const reducer = (state, action) => {
  switch (action.type) {
    case 'increase':
      return { count: state.count + 1 };
    case 'decrease':
      return { count: state.count - 1 };
    default:
      return state;
  }
};

const Counter = () => {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increase' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrease' })}>-</button>
    </div>
  );
};
```

- `dispatch({ type: 'increase' })` sends an **action** object to the reducer.
- The reducer receives `(state, action)` and returns the **new state**.
- `action.type` decides which case in the `switch` statement runs.

### Avoiding Typos With Action Constants

Hardcoding string types (`'increase'`, `'decrease'`) risks typos across files. Define them once in a constants object (commonly UPPERCASE):

```jsx
const ACTIONS = {
  INCREASE: 'increase',
  DECREASE: 'decrease',
};

const reducer = (state, action) => {
  switch (action.type) {
    case ACTIONS.INCREASE:
      return { count: state.count + 1 };
    case ACTIONS.DECREASE:
      return { count: state.count - 1 };
    default:
      return state;
  }
};

// usage
dispatch({ type: ACTIONS.INCREASE });
dispatch({ type: ACTIONS.DECREASE });
```

### Recap

| Part | Meaning |
|---|---|
| `state` (reducer param) | Current state |
| `action` (reducer param) | Object describing what happened |
| `dispatch(action)` | Triggers the reducer to compute new state |
| Best for | Multiple related state values / complex update logic |

---

## 6. useLayoutEffect Hook

`useLayoutEffect` works exactly like `useEffect`, but differs in **timing**:

| Hook | Runs |
|---|---|
| `useLayoutEffect` | **Before** the browser paints the DOM (synchronous) |
| `useEffect` | **After** the browser paints the DOM (asynchronous) |

**Execution order:** React calculates the component → `useLayoutEffect` runs → DOM is painted → `useEffect` runs.

Use `useLayoutEffect` when you need to measure or adjust layout (element height/width) **before** the user sees it — otherwise you may see a visual flicker/jump.

### Example — Measuring an Element Before Paint

```jsx
import { useRef, useLayoutEffect } from 'react';

const TextBox = () => {
  const textRef = useRef(null);

  useLayoutEffect(() => {
    if (textRef.current !== null) {
      const dimension = textRef.current.getBoundingClientRect();
      textRef.current.style.paddingTop = `${dimension.height}px`;
    }
  });

  return <p ref={textRef}>Some text</p>;
};
```

Using `useEffect` here would cause a brief visible "jump" because the DOM already painted before the padding was applied. `useLayoutEffect` applies the change **before** paint, avoiding the flicker.

### Recap

- Same syntax and behavior as `useEffect`, only the timing differs.
- `useLayoutEffect` is **synchronous**; `useEffect` is **asynchronous**.
- Use `useEffect` by default (99% of cases). Switch to `useLayoutEffect` only if you see layout flicker with `useEffect`.

---

## 7. useMemo Hook

`useMemo` applies **memoization** — caching the result of an expensive calculation so it doesn't re-run on every render unless its dependencies change.

```jsx
const memoizedValue = useMemo(callbackFunction, dependenciesArray);
```

### Problem

```jsx
const expensiveCalculation = (num) => {
  console.log('loop started');
  for (let i = 0; i < 1000000000; i++) {} // simulate heavy work
  return num;
};

const calculation = expensiveCalculation(number); // runs on EVERY render
```
Even toggling an unrelated `dark` mode state causes this expensive function to re-run, slowing down the whole component.

### Solution

```jsx
import { useMemo, useState } from 'react';

const [number, setNumber] = useState(0);
const [dark, setDark] = useState(false);

const expensiveCalculation = (num) => {
  console.log('loop started');
  for (let i = 0; i < 1000000000; i++) {}
  return num;
};

const memoCalculation = useMemo(() => {
  return expensiveCalculation(number);
}, [number]); // only re-runs when "number" changes
```

Now toggling `dark` mode no longer triggers the expensive function — only changing `number` does.

### useMemo vs useEffect

| | `useEffect` | `useMemo` |
|---|---|---|
| Returns a value directly? | No (must use a separate state variable) | Yes — can store the return value in a variable |
| Purpose | Run side effects | Cache/memoize a calculated value |

### Recap

- Use `useMemo` for **expensive calculations**, use `useEffect` for **side effects**.
- Syntax mirrors `useEffect`: `(callback, dependencies)`.
- The callback **returns** a value which is stored directly in a variable.

---

## 8. useCallback Hook

`useCallback` returns a **memoized function** (instead of a memoized value like `useMemo`), preventing functions from being recreated on every re-render.

> **Key difference:** `useMemo` returns a memoized **value**. `useCallback` returns a memoized **function**.

### Problem

```jsx
const calculateTable = (num) => {
  console.log('print table runs');
  const table = [];
  for (let i = 1; i <= 5; i++) {
    table.push(`${num} * ${i} = ${num * i}`);
  }
  return table;
};

// Passed as a prop to a child component
<PrintTable calculateTable={calculateTable} />
```
Even if `calculateTable`'s logic and output are identical, React creates a **new function instance** on every render. A child component that receives this function as a prop sees it as "changed" and re-renders unnecessarily — even for unrelated state changes (like toggling a theme).

### Solution

```jsx
import { useCallback, useState } from 'react';

const [number, setNumber] = useState(0);

const calculateTable = useCallback((value = 0) => {
  const newNumber = number + value;
  const table = [];
  for (let i = 1; i <= 5; i++) {
    table.push(`${newNumber} * ${i} = ${newNumber * i}`);
  }
  return table;
}, [number]); // only recreated when "number" changes
```

Now the function reference stays the same across re-renders unless `number` changes, so the child component (`PrintTable`) doesn't re-render unnecessarily.

- `useCallback` can accept parameters when called (e.g. `calculateTable(2)`), unlike `useMemo`.

### Recap

| | `useMemo` | `useCallback` |
|---|---|---|
| Returns | Memoized value | Memoized function |
| Syntax | `useMemo(fn, deps)` | `useCallback(fn, deps)` |
| Accepts extra params on call? | No | Yes |
| Purpose | Cache a calculated result | Prevent function recreation on re-render |

---

## 9. Custom Hooks

Custom hooks are **your own reusable functions** built from one or more built-in hooks, used to avoid repeating the same logic across multiple components. Naming convention: always start with **`use`** (e.g. `useFetch`).

### Problem: Repeating API-Fetch Logic

```jsx
// Repeated in every component that needs data
const [response, setResponse] = useState([]);

useEffect(() => {
  fetch('https://randomuser.me/api/?results=5')
    .then((res) => res.json())
    .then((data) => setResponse(data.results));
}, []);
```
Copy-pasting this into 10–12 components is bad practice.

### Solution: Extract Into a Custom Hook

```jsx
// customHooks/useFetch.js
import { useState, useEffect } from 'react';

const useFetch = (url) => {
  const [response, setResponse] = useState([]);

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((data) => setResponse(data.results));
  }, [url]);

  return response;
};

export default useFetch;
```

### Using the Custom Hook

```jsx
import useFetch from './customHooks/useFetch';

const App = () => {
  const data = useFetch('https://randomuser.me/api/?results=5');

  return (
    <div>
      {data.map((user, index) => (
        <p key={index}>{user.name.first}</p>
      ))}
    </div>
  );
};
```

### Recap

- Custom hooks = your own logic, packaged as a reusable function, built on top of built-in hooks.
- Organize them in a dedicated folder (e.g. `customHooks/`).
- Always prefix the name with `use`.
- Reusable across multiple components **and** multiple projects.

---

## Full Summary Table

| Hook | Purpose |
|---|---|
| `useState` | Add state to a functional component |
| `useEffect` | Perform side effects (API calls, DOM/timer manipulation) after paint |
| `useContext` | Share global data without prop drilling |
| `useRef` | Persist mutable values without re-render / access DOM elements directly |
| `useReducer` | Manage complex state with a reducer + dispatch pattern |
| `useLayoutEffect` | Like `useEffect`, but runs synchronously before paint |
| `useMemo` | Memoize an expensive **calculated value** |
| `useCallback` | Memoize a **function** to prevent unnecessary re-creation |
| Custom Hooks | Your own reusable functions built from built-in hooks |
