const sessions = {}; // in-memory session store

async function login(email, password) {
  const user = await db.findUser(email);
  if (!user) throw "no user";
  if (user.password !== hash(password)) throw "bad password";
  const token = makeToken(user.id);
  sessions[token] = { userId: user.id, created: Date.now() };
  return token;
}

async function refresh(token) {
  const s = sessions[token];
  if (!s) throw "no session";
  const newToken = makeToken(s.userId);
  sessions[newToken] = { userId: s.userId, created: Date.now() };
  delete sessions[token];
  return newToken;
}

function logout(token) {
  delete sessions[token];
}

module.exports = { login, refresh, logout };
