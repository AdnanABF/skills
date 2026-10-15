---
name: frappe-api-contracts
description: Use when creating, editing, or reviewing Frappe APIs used by Flutter, Next.js, mobile apps, or external clients.
---

Follow these API contract rules strictly when working on Frappe-backed features.

## When Not To Apply

- Do not use this skill for Frappe Desk-only methods with no external consumer.
- Use it alongside, not instead of, `frappe-python.md` for endpoint implementation.

## Read Alongside

- Backend implementation: `frappe-python.md`.
- Files or images: `frappe-file-images.md`.
- External or long-running work: `frappe-async-external-apis.md`.

## When To Apply

- Apply this skill for any Frappe API that is consumed by Flutter, Next.js, or other external clients.
- Apply it alongside `frappe-python.md` for backend implementation work.

## Response Shape

- Keep API response fields stable once a frontend consumes them.
- When expanding a response, prefer additive changes over breaking shape changes.
- If create or update endpoints return records, return the same normalized field format used by the corresponding read endpoint.

## Asset URLs

- Do not return raw private file paths to clients.
- For file and image fields, return directly usable client values:
  - public files should resolve to full absolute URLs
  - public app assets such as `/assets/<app>/...` should also resolve to full absolute URLs
  - private files should resolve to signed download URLs
- Reuse shared helpers for URL normalization instead of duplicating logic per endpoint.

## Client Compatibility

- Return a readable title/name alongside every linked record's canonical `name`/ID in list, detail, create/update, and selection/search responses. Forms and selectors must display the readable text as the primary label; keep IDs for persistence, joins, API payloads, and optional secondary disambiguation only.
- Use the target DocType's `title_field` (for example Guardian `guardian_name`), not an autoname/series ID, as its display name. Configure `show_title_field_in_link` when appropriate for Desk selectors. Do not rename documents or replace stored link IDs with titles.
- Frappe `search_link` can return `label == value` when `show_title_field_in_link` is disabled even though `description` includes the readable title. Consumers must not blindly prefer that ID-valued label over readable description/title text. Preserve the selected label in forms and resolve the title for existing saved links as well.
- Respect field/document permissions when resolving titles. If no readable title is available, use a safe fallback without exposing restricted data or clearing the stored link.
- Assume Next.js and Flutter clients should not reconstruct backend file URLs on their own.
- Avoid mixing relative paths, absolute URLs, and signed URLs for the same response field across endpoints.
- Do not leave app asset paths as relative `/assets/...` values in API responses; normalize them to absolute URLs before returning.
- If an endpoint returns `image`, `cover_image`, or similar fields, keep the contract consistent across list, detail, create, and update flows.

## Shared Patterns

### Managed Device Authentication

- Frontend implementation follows `frontend-api-client.md`; headers belong in the backend-scoped client, not individual endpoints.
- For `flutter_utils` managed token login, send a random installation UUID as `device_id`, generated once and persisted per installation/browser profile. Do not use hardware identifiers or generate a new ID on each login. `device_name` is optional display metadata.
- Persist `api_key`, `api_secret`, and returned `authorization_source` together. For managed credentials, the source is `Flutter Device Credential`.
- For web applications, follow the BFF security boundary in `frontend-api-client.md`: retain this credential tuple in server-controlled storage or an authenticated-encrypted HttpOnly cookie, not browser-readable token storage. The BFF still calls Frappe in token mode; its browser cookie is not a Frappe session. Preserve a stable browser installation UUID without exposing API secrets.
- Every managed-token request sends `Authorization: token <api_key>:<api_secret>` and `Frappe-Authorization-Source: Flutter Device Credential`. Without the source header, Frappe searches User credentials and rejects a device key.
- Existing User-based tokens without a source can omit the source header where that persisted format is still supported. Do not guess that every old key is a device key.
- Login/token exchange and OTP issuance are explicitly public. `flutter_utils.api.auth.logout_device` is authenticated; do not classify access by the common auth namespace.
- Cookie-session APIs remain a distinct contract, including cookie transmission and CSRF protection. Do not silently convert them to token APIs.
- Verify login AND a subsequent authenticated read against the deployed schema. Mocked credential issuance alone cannot detect missing DocTypes or omitted request headers.

- Put reusable response-building logic in shared private helpers instead of repeating payload assembly in each whitelisted method.
- When a feature has both read and write endpoints, prefer one serializer/helper so all flows return the same normalized shape.

## Verification

- Verify a series-named linked record shows its readable name in search results, immediately after selection, and after reopening the edit form, while saving still submits its original ID. Cover duplicate titles and unavailable/restricted titles.
- Verify authenticated and unauthorized responses do not expose fields beyond the caller's permissions.
- Verify list, detail, create, and update responses use compatible field names and normalized asset URLs.
- Verify additive changes preserve existing response fields and types for active clients.
