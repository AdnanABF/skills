---
name: frontend-api-client
description: Use when adding, changing, or reviewing frontend API calls, shared HTTP clients, authentication headers, credential persistence, or session-expiration handling on any platform.
---

# Frontend API Client

## When To Use

Apply to browser, mobile, desktop, and server-rendered frontend applications. Read this before the platform networking adapter. This skill owns shared transport and authentication behavior; adapters own library syntax, storage mechanisms, and project paths.

- Flutter implementation: `flutter-networking.md`.
- Next.js implementation: `nextjs-architecture.md`.
- Browser fetch implementation: [Browser client reference](references/browser-client.md).
- Frappe authentication contracts: `frappe-api-contracts.md`.
- Independent remote loads: `api-parallelization.md`.
- Connecting existing prototype screens to real backend data: required companion `frontend-design-consistency.md` for preserving the working UI. This does not make a transport-only client change a visual-audit task.

## Client Boundary

- Use one configured client per backend/security boundary. Feature modules use that client, not direct transport calls or feature-local client instances.
- Centralize base URL resolution, authentication headers, credential policy, cancellation propagation, and session-expiration effects. A header helper that every endpoint must remember to invoke is not sufficient.
- Keep endpoint payloads, typed response parsing, and business-specific errors in repositories or feature API modules.
- Do not replace an established HTTP library merely to add interceptors. Do not patch global networking functions.
- Restrict authenticated requests to the intended backend. Validate resolved destinations; prevent redirects from forwarding credentials to other services. Third-party SDKs, signed assets, and payment providers have separate security boundaries.

## Authentication Modes

- Declare authenticated, public, and cookie-session requests explicitly. Do not infer public access from a broad URL prefix: login and authenticated logout may share a namespace.
- Read current credentials at dispatch time. Do not capture tokens once during client construction.
- Persist all authentication metadata required by the backend contract, not just the primary token. Retain legacy behavior only when actual persisted credentials or shipped consumers require it.
- Merge caller headers centrally and case-insensitively. Authentication headers are client-owned and cannot be overridden by feature code.
- Public calls must not carry stored tokens; cookie transmission must follow the explicit mode. Cookie-session writes retain the backend's CSRF requirements.
- Keep server-side credentials scoped to the incoming request. Never mutate a shared server client's defaults with a user's token or cache authenticated responses across users.
- Never log credentials, authorization headers, secrets, or sensitive authentication payloads.

## Web Application Credential Security

- For new web application token authentication, prefer a same-origin backend-for-frontend (BFF). Keep upstream API secrets, refresh tokens and authentication-source metadata on the server; browser JavaScript calls application endpoints, not the upstream token API.
- Store credentials in a server-side session keyed by an opaque HttpOnly cookie, or in an authenticated-encrypted HttpOnly cookie. Do not expose token secrets in client props, JSON responses, localStorage, sessionStorage or JavaScript-readable cookies. An HttpOnly cookie alone is not encryption; never place plaintext API secrets in it.
- Use Secure cookies on hosted HTTPS, an explicit SameSite policy, host-only scope, bounded expiry and purpose-bound authenticated encryption when using cookie payloads. Keep encryption/signing keys in private runtime configuration; never commit them or expose them through public environment variables. An HTTP localhost development exception must not weaken hosted settings.
- Cookie-authenticated BFF mutations need CSRF protection even when the upstream uses token mode. Check the exact configured browser Origin for login, logout and other writes; enforce the expected content type or use a CSRF token. Do not trust caller-selected forwarding destinations or upstream redirects.
- Validate credentials and current authorization server-side for protected routes and each feature API. Cookie presence and client route guards are not authorization. Return only minimal user metadata and mark authenticated responses no-store.
- Keep browser-to-BFF cookie authentication distinct from BFF-to-backend token authentication. Preserve all backend-required token headers. Stable browser installation IDs may be persisted as non-secret metadata; native clients retain their platform-specific secure storage contract.
- Logout must revoke upstream device/refresh credentials where the backend supports it, then clear browser authentication. Clearly distinguish local-only logout or failed revocation. Do not silently claim revocation when the backend is unreachable.
- For an existing direct-token browser application, do not silently break shipped consumers. Document any justified exception and plan a deliberate migration to the BFF boundary.

## Failures And Concurrency

- Centralize authentication-expiration side effects and leave routing to the existing auth/UI layer. Individual endpoints must not emit duplicate logout events.
- Expire only the credentials used by the failed request. A delayed unauthorized response must not erase a newer login. Compare a credential snapshot or authentication generation before changing local state.
- Collapse concurrent unauthorized failures into one expiration event for that login. Public-login failures do not invalidate a separate stored session.
- Do not treat every forbidden response as an expired login; authorization denial and authentication failure are distinct.
- Preserve cancellation, request bodies, and timeout semantics. Aborted/network-failed requests must not automatically sign the user out.
- Do not introduce automatic mutation retries, refresh loops, or hidden serialization. Refresh/retry requires a documented backend contract and bounded behavior.

## Payloads And Errors

- Support JSON, form-encoded bodies, multipart uploads, and any response types needed by the application.
- Do not force a JSON content type on every request. Let the transport generate multipart boundaries.
- Keep a clear error contract: either return the response for feature parsing or throw a normalized error, following the established platform pattern. Do not consume response bodies before feature parsing without preserving them.

## Verification

- For web token auth, test that secrets never reach browser-readable storage or response bodies, cookie tampering/expiry fail closed, hosted cookies are Secure/HttpOnly, cross-origin writes fail, and live logout revokes the upstream credential.

- Test latest credential injection, auxiliary authentication metadata, header merging, and caller-override prevention.
- Test public/session modes, missing credentials, and rejection of unrelated destinations before transmission.
- Test multipart uploads, cancellation propagation, and unchanged endpoint payloads.
- Test one expiration event for concurrent failures and preservation of newer credentials after a stale failure.
- Test existing persisted credential formats where compatibility is required.
- Search application sources for direct backend transport calls outside the shared client; third-party SDK calls remain separate.
- Run platform tests, lint, type analysis/build, and representative login followed by authenticated reads when live access permits. Report unverified live behavior separately from mocked tests.
