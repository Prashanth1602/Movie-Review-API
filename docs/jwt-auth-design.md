# Designing JWT Authentication in Movie Review API

This document describes the authentication design used in the Movie Review API. 
The system needed to support authenticated users with different roles while remaining stateless, scalable, and simple to integrate across clients.

## Why JWT? (The Decision Process)

When designing the authentication layer, I considered several common approaches: Session-based Authentication, OAuth2, and JWT.

### 1. JWT vs. Session-based Authentication
Traditional session-based auth stores the user's state (Session ID) on the server (memory/Redis/DB) and sends it to the client as a cookie.
- **Scalability**: Sessions are stateful. Scaling horizontally requires sticky sessions or a centralized session store (like Redis), adding infrastructure complexity. JWTs are stateless, token contains all necessary info.
- **Cross-Platform**: JWTs are easier to use across different clients (Web, Mobile App, IoT) where cookies might be tricky to manage natively.
- **CSRF**: JWTs, when sent via Authorization headers instead of cookies, significantly reduce CSRF risk, shifting the primary threat model toward XSS.

### 2. JWT vs. OAuth2
- OAuth2 is a protocol for authorization (delegated access), often using JWTs as the format for tokens. It is excellent for allowing third-party apps to access user data (Login with Google).
- However, for a first-party application authenticating its own users, full OAuth2 flows (like Authorization Code Grant) can be complex. I adopted the JWT Bearer Token pattern, which gives us the benefits of OAuth-style tokens without the complexity of the full protocol redirects.

I chose JWT for its stateless nature (easing scalability), flexibility across client types, and industry-standard security patterns.

---

## High-Level Implementation

### The Architecture
We utilize a Dual-Token System to balance security and user experience:

1.  **Access Token**: Short-lived (e.g., 15-30 minutes). Used to access protected API endpoints.
2.  **Refresh Token**: Long-lived (e.g., 7 days). Stored in the database and used to obtain new Access Tokens when the old one expires.

### The Flow
1.  **Registration**: User signs up; Password is hashed using Bcrypt before storage.
2.  **Login**: User sends credentials. Server validates hash. If valid, generates an Access Token and a Refresh Token.
3.  **Storage**: 
    - The Refresh Token is stored in the database, linked to the user. We can revoke access by deleting/flagging this DB entry.
    - Tokens are returned to the client.
4.  **Access**: Client sends Authorization: Bearer <access_token> header for requests.
5.  **Verification**: 
    - Middleware decodes the JWT signature.
    - Security Check: It also verifies the user exists in the DB on every request. This adds a database hit but ensures that banned/deleted users are locked out immediately, rather than waiting for the token to expire.

---

## Trade-offs and Mitigations

No system is perfect. Here are the trade-offs and how we mitigate them:

### 1. Token Invalidation (The "Logout" Problem)
**Issue**: True stateless JWTs cannot be invalidated before they expire. If stolen, a hacker has access until expiry.
**Mitigation**: 
- We use Short-lived Access Tokens. The window of opportunity for a stolen access token is small.
- We use Stateful Refresh Tokens. We can revoke a user's session immediately by revoking the Refresh Token in the database. When the access token expires, the attacker cannot get a new one.

### 2. Payload Size
**Issue**: JWTs are larger than simple Session IDs because they carry data.
**Mitigation**: We keep the payload minimal, storing only essential data like sub (user ID) and exp (expiry).

### 3. XSS vs CSRF
**Issue**: Storing tokens in localStorage (common frontend pattern) makes them vulnerable to XSS (Cross-Site Scripting).
**Mitigation**: We implement HttpOnly, Secure Cookies to mitigate XSS attacks.

---

## Practiced Best Practices

1.  **Strong Hashing**: We never store plain-text passwords. We use Bcrypt which is slow by design to resist brute-force attacks.
2.  **Algorithm choice**: HS256 is used since both signing and verification occur within the same backend service. For distributed systems or multi-service verification, an asymmetric algorithm like RS256 would be more appropriate.
3.  **Environment Variables**: The SECRET_KEY is loaded from environment variables, never hardcoded in the source.
4.  **Token Rotation**: Our current implementation re-issues tokens upon login. We also delete refresh token from database when user logs out.

---

## Future Improvements

To further harden security, the following improvements are recommended:

1.  **HttpOnly Cookies**:
    - Currently, tokens are returned in the response body. Moving Refresh Tokens to HttpOnly, Secure Cookies would effectively eliminate the risk of them being stolen via XSS, as JavaScript cannot read them.
2.  **Rate Limiting**:
    - Implementing rate limiting on the Login and Refresh endpoints to prevent brute-force attacks on credentials or token guessing.
