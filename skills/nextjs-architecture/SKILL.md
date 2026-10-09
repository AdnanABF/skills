---
name: nextjs-architecture
description: Use when changing Next.js masarnext project structure, feature modules, API routes, shared utilities, or app architecture.
---

Follow these architecture rules strictly when working on the Next.js app (`next_apps/masarnext/`):

For networking changes, read `frontend-api-client.md` first. It owns shared transport/auth behavior; this adapter owns existing Next.js helpers and browser/server boundaries.

## Project Structure

```
src/
├── app/            # Next.js App Router (pages + API routes)
├── features/       # Feature modules (core business logic)
├── components/     # Shared layout & UI components
├── lib/            # Shared utilities (Frappe client, helpers)
├── data/           # Shared lookup data fetchers (countries, genders)
└── types/          # Global type declarations
```

## Feature Module Structure

Each feature lives in `src/features/<name>/` with this layout:

```
features/<name>/
├── components/       # React components (one per file + co-located .module.css)
├── server/           # Server-side functions (API calls to Frappe backend)
└── types.ts          # Feature-specific TypeScript types
```

- **A feature owns its own server logic.** If a feature calls a Frappe API, the function belongs in that feature's `server/` folder, not in another feature.
- **Features should not import from another feature's `server/` folder.** Cross-feature dependencies flow through shared `lib/` or `data/`.
- **Components are co-located with their CSS Modules.** Every `Component.tsx` has a `Component.module.css` beside it.

## API Routes

API routes in `src/app/api/` mirror feature boundaries:

| Route prefix | Purpose |
|---|---|
| `/api/auth/` | Login/logout (send-otp, verify-otp) |
| `/api/profile/` | Profile read & update |
| `/api/registration/` | Registration flow (status, role, sport, profile setup) |

- Do NOT put all routes under `/api/auth/`. Only authentication endpoints belong there.
- Each route file is a thin adapter: extract credentials, call the feature's server function, return the response.

## Shared Utilities (`src/lib/`)

- **`frappeClient.ts`** — Single Frappe API client. Use `callAuthedMethod` for authenticated JSON calls, `callAuthedFormData` for file uploads, `callGuestMethod` for unauthenticated calls. Never duplicate these patterns inside features.
- **`apiBaseUrl.ts`** — `getApiBaseUrl()` and `normalizeAssetUrl()`. Always import from here; never redeclare.

- Inject authentication metadata centrally in the existing client helpers, not in each feature or route. Preserve explicit guest/authenticated operations and multipart support.
- Browser clients read current credentials at dispatch time. Server clients receive credentials scoped to the incoming request; never put a user's credentials in shared mutable defaults or cross-user caches.
- Validate backend destinations and keep third-party requests separate. Apply the shared unauthorized-response rules in the browser auth layer, not through server-side global state.

## Web Token Authentication Boundary

- Follow `frontend-api-client.md` for new web token auth: browser clients call same-origin route handlers, while server-only modules read request-scoped HttpOnly session/cookie credentials and call the backend. Do not send upstream API secrets through client props or browser JSON.
- Keep credential codecs and encryption keys server-only. With encrypted cookies, use purpose-bound authenticated encryption, validate payloads and expiry, and use Secure/host-only cookies for hosted HTTPS.
- Route handlers enforce exact configured Origin/CSRF checks for cookie-authenticated mutations, including login/logout. Reject arbitrary upstream URLs and disable credential-bearing redirects.
- Protect each backend API independently; a layout or optimistic Proxy redirect is not sufficient. Validate current backend identity and roles before rendering protected content, including client/RSC navigation. Do not trust caller-supplied identity headers; overwrite internal headers at the server boundary.
- Read the installed Next.js docs before implementing cookies, route handlers or Proxy conventions. On current versions, cookie/header access is asynchronous. Keep route adapters thin, authenticated fetches uncached and runtime secrets out of `NEXT_PUBLIC_*`.
- Existing Masar direct-token helper names below describe that application's current boundary. A new application should not copy browser token persistence solely to match those names; use the BFF design and preserve upstream authentication mode/metadata.

## Shared Data (`src/data/`)

- Lookup data fetchers (countries, genders, etc.) that are used across multiple features live here.
- These are server-side functions that call guest Frappe endpoints.

## Rules

1. **No duplicate utilities.** If a helper exists in `lib/`, import it. Never copy-paste functions like `getApiBaseUrl` into feature files.
2. **Feature isolation.** Each feature manages its own types, components, server calls, and styles. Do not create "god files" that serve multiple features.
3. **Client vs Server separation.** Files using browser APIs or React hooks must have `"use client"` at the top. Server-side data fetchers and API route handlers must NOT have it.
4. **Auth flow.** Client-side authenticated requests use `postAuthedJson` or `postAuthedFormData` from `features/auth/client/authClient.ts`. Server-side routes extract credentials via `getRequestAuthCredentials` from `features/auth/server/requestAuth.ts`.
5. **Type ownership.** Each feature defines its own types in `types.ts`. Shared result types like `FrappeResult<T>` live in `lib/frappeClient.ts`.
6. **Styling.** Use CSS Modules (`.module.css`) co-located with components. Use design system CSS variables (e.g., `var(--text-primary)`, `var(--space-md)`, `var(--radius-lg)`) — never hardcode colors or spacing in component styles.
7. **Hooks before returns.** All React hooks (`useState`, `useEffect`, `useCallback`, etc.) must be called before any early return statement in a component.
8. **API route pattern.** Every API route follows the same structure: parse request → extract auth → call feature server function → return JSON response. Keep routes thin.
9. **Reuse shared empty states.** When a screen needs a standard no-data view, use `src/components/ui/EmptyState.tsx` instead of re-creating feature-local empty-state markup.
10. **Paginate listing pages.** Any listing/index page like coaches, athletes, clubs, academies, events, or programs must follow `nextjs-listing-screens.md`: fetch the first page only and expose additional results through a Load more button.

## Verification

- Run lint, type analysis/build and authentication tests against the installed Next.js version.
- Verify protected document/RSC navigation and each feature API reject invalid/revoked credentials, with no secret leakage or cross-user response caching.
- Verify cookie flags, encryption/expiry, exact-Origin rejection, backend token headers and device revocation on logout.
