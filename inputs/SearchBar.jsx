import React, { useState } from "react";

export function SearchBar({ fetchResults }) {
  const [q, setQ] = useState("");

  function onChange(e) {
    const value = e.target.value;
    setQ(value);
    fetchResults(value);
  }

  return <input value={q} onChange={onChange} placeholder="Search..." />;
}
