Four changes in `auth.js`:
1. fix token refresh in `refresh()`
2. add rate limiting to `login()`
3. move `sessions` store to redis
4. better error messages (replace `throw "string"`)

Which first? (other three parked)
