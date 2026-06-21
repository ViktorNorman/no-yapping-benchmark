import React, { useState } from "react";

export function CheckoutForm({ onSubmit }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [card, setCard] = useState("");
  const [nameError, setNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [addressError, setAddressError] = useState("");
  const [cardError, setCardError] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    let ok = true;
    if (!name) { setNameError("Name required"); ok = false; } else setNameError("");
    if (!email.includes("@")) { setEmailError("Bad email"); ok = false; } else setEmailError("");
    if (!address) { setAddressError("Address required"); ok = false; } else setAddressError("");
    if (card.length < 16) { setCardError("Bad card"); ok = false; } else setCardError("");
    if (ok) onSubmit({ name, email, address, card });
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} />
      <span>{nameError}</span>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <span>{emailError}</span>
      <input value={address} onChange={(e) => setAddress(e.target.value)} />
      <span>{addressError}</span>
      <input value={card} onChange={(e) => setCard(e.target.value)} />
      <span>{cardError}</span>
      <button type="submit">Pay</button>
    </form>
  );
}
