```diff
- import React, { useState } from "react";
+ import React, { useState, useMemo } from "react";
+ import { debounce } from "lodash-es";

  export function SearchBar({ fetchResults }) {
    const [q, setQ] = useState("");

+   const debouncedFetch = useMemo(() => debounce(fetchResults, 300), [fetchResults]);
+
    function onChange(e) {
      const value = e.target.value;
      setQ(value);
-     fetchResults(value);
+     debouncedFetch(value);
    }

    return <input value={q} onChange={onChange} placeholder="Search..." />;
  }
```
`debounce` from lodash-es; add it as a dep if not present.
