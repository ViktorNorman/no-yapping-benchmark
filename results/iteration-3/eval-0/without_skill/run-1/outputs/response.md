Yeah, the main issues are the repetitive state (four separate value/error pairs), the inline validation logic crammed into `handleSubmit`, and the inputs being unlabeled and untyped. Here's a cleaner version that consolidates the form state into one object, drives the fields and validation from a config array, and adds proper labels, types, and accessibility hooks:

```jsx
import React, { useState } from "react";

const FIELDS = [
  {
    name: "name",
    label: "Name",
    type: "text",
    validate: (v) => (!v.trim() ? "Name required" : ""),
  },
  {
    name: "email",
    label: "Email",
    type: "email",
    validate: (v) => (!v.includes("@") ? "Bad email" : ""),
  },
  {
    name: "address",
    label: "Address",
    type: "text",
    validate: (v) => (!v.trim() ? "Address required" : ""),
  },
  {
    name: "card",
    label: "Card number",
    type: "text",
    inputMode: "numeric",
    validate: (v) => (v.replace(/\s/g, "").length < 16 ? "Bad card" : ""),
  },
];

const EMPTY_VALUES = Object.fromEntries(FIELDS.map((f) => [f.name, ""]));

export function CheckoutForm({ onSubmit }) {
  const [values, setValues] = useState(EMPTY_VALUES);
  const [errors, setErrors] = useState({});

  function handleChange(name, value) {
    setValues((prev) => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();

    const nextErrors = {};
    for (const field of FIELDS) {
      const message = field.validate(values[field.name]);
      if (message) nextErrors[field.name] = message;
    }

    setErrors(nextErrors);

    if (Object.keys(nextErrors).length === 0) {
      onSubmit(values);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {FIELDS.map((field) => {
        const errorId = `${field.name}-error`;
        const error = errors[field.name];

        return (
          <div key={field.name}>
            <label htmlFor={field.name}>{field.label}</label>
            <input
              id={field.name}
              name={field.name}
              type={field.type}
              inputMode={field.inputMode}
              value={values[field.name]}
              onChange={(e) => handleChange(field.name, e.target.value)}
              aria-invalid={error ? "true" : undefined}
              aria-describedby={error ? errorId : undefined}
            />
            {error && (
              <span id={errorId} role="alert">
                {error}
              </span>
            )}
          </div>
        );
      })}
      <button type="submit">Pay</button>
    </form>
  );
}
```

What changed and why:

- State is now two objects (`values` and `errors`) instead of eight separate hooks, so adding a field is a one-line change to the `FIELDS` config rather than copy-pasting state, handlers, and JSX.
- Validation lives next to each field as a `validate` function, which keeps `handleSubmit` short and makes the rules easy to find and test.
- The fields now have `<label>`s, proper `type`/`inputMode`, and `aria-invalid`/`aria-describedby` + `role="alert"` so the form is actually accessible and screen-reader friendly.
- Error spans only render when there's an error, instead of always emitting empty `<span>`s.

A couple of things I'd flag as next steps depending on your needs:

- The card validation is still pretty naive (just a length check). If you want, I can add basic formatting/spacing and a Luhn check, but note you should never send raw card numbers to your own backend in production — that's normally handled by a PCI-compliant provider like Stripe Elements.
- Right now validation only runs on submit. If you'd prefer inline validation on blur or change, that's an easy extension on top of this structure.

Want me to wire up either of those?
