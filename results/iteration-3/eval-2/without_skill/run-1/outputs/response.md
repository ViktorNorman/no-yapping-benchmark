Here's how to add a 300ms debounce to the search input. The key is to keep updating the input value immediately (so the field stays responsive) while delaying only the `fetchResults` call.

```jsx
import React, { useState, useEffect, useRef } from "react";

export function SearchBar({ fetchResults }) {
  const [q, setQ] = useState("");
  const timeoutRef = useRef(null);

  function onChange(e) {
    const value = e.target.value;
    setQ(value);

    clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      fetchResults(value);
    }, 300);
  }

  // Clear any pending request on unmount
  useEffect(() => {
    return () => clearTimeout(timeoutRef.current);
  }, []);

  return <input value={q} onChange={onChange} placeholder="Search..." />;
}
```

What changed:
- A `useRef` holds the pending timeout ID so it survives re-renders without triggering one.
- On each keystroke, the previous pending request is cancelled and a new 300ms timer is scheduled, so `fetchResults` only fires once the user pauses typing.
- The `useEffect` cleanup clears any in-flight timer on unmount, avoiding a fetch (and a state update) after the component is gone.

If you use debouncing in more places, it might be worth extracting a `useDebouncedCallback` hook or pulling in lodash's `debounce`, but for a single input this is all you need.
