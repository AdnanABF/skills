---
name: setup-frappe-realtime
description: Use when setting up or connecting Frappe Socket.IO realtime for a frontend served from a different domain, including the nginx /socket.io reverse proxy.
---

# Setup Frappe Realtime

Use this skill when wiring, repairing, or explaining how a browser frontend (Flutter web, Next.js, React) or a native app connects to Frappe Socket.IO realtime, especially when the frontend is served from a domain different from the Frappe backend.

Read with:

- `frappe-realtime-updates.md` for event emission and general realtime semantics.
- `flutter-networking.md` (or the target platform adapter) for client implementation.
- `flutter-web-deployment.md` or `nextjs-deployment.md` for vhost provisioning.
- `project-connections.md` for the project's hostnames and connections.

## When To Apply

- A browser frontend served from its own domain must reach Frappe realtime.
- Adding, updating, or removing a frontend vhost's `/socket.io` reverse proxy.
- Migrating an app's socket base host from the backend domain to the frontend domain.
- Diagnosing `blocked by CORS policy`, `Access-Control-Allow-Origin ... not equal to the supplied origin`, or realtime `404` / `Invalid origin` / `Invalid namespace` errors.

## Architecture

Frappe's realtime middleware (`apps/frappe/realtime/middlewares/authenticate.js`) requires `get_hostname(host) == get_hostname(origin)` and the Socket.IO namespace to equal the site name (resolved from `X-Frappe-Site-Name`). The Node server enables `cors: { origin: true }`, so it reflects whichever `Origin` reaches it.

A browser connecting directly to the backend from the frontend origin sends a mismatched `Host`/`Origin`, and the backend answers with its own host in `Access-Control-Allow-Origin`, so the browser blocks the response. Frappe REST `allow_cors` is a separate mechanism and never fixes Socket.IO CORS.

The fix is to connect same-origin and reverse-proxy:

```
browser → https://<frontend>/socket.io/... → frontend nginx → http://127.0.0.1:9000/socket.io
```

with `Host`, `Origin`, and `X-Frappe-Site-Name` rewritten to the backend site.

## Server Setup

Use `.agents/scripts/add_socketio_proxy.sh`:

```bash
.agents/scripts/add_socketio_proxy.sh \
  --frontend employee-dev.xealth.ca \
  --backend backend-dev.xealth.ca \
  --ssh-key ~/.ssh/id_ed25519
```

Options and modes:

- `--ssh-user`, `--ssh-key`, `--ssh-port`, `--config NAME`, `--server-name NAME`, `--socket-target URL`.
- `--dry-run` prints the diff; `--check` reports present/absent; `--remove` strips the block.
- `--test` / `--reload` run nginx checks/reload; `--config-file PATH` edits a local file without SSH.
- The script backs up the vhost, installs the block, runs `nginx -t`, and reloads; on failure it restores the backup.

`.agents/scripts/socketio_proxy_config.py apply|remove|check` is the idempotent in-place editor behind the script. It wraps the block in `# >>> frappe socket.io proxy (managed) >>>` / `# <<< ... <<<` markers, adopts an existing hand-written `location /socket.io`, and re-applies without duplicating.

The managed block:

- `proxy_set_header Host <backend>;`
- `proxy_set_header X-Frappe-Site-Name <backend>;`
- `proxy_set_header Origin https://<backend>;`
- `proxy_pass <socket-target>/socket.io;`
- Enables HTTP/1.1 with `Upgrade`/`Connection`, long read/send timeouts, and reflects `Access-Control-Allow-Origin`.

Authorization headers and polling GET/POST pass through; do not strip or override them.

Socket target:

- Backend Socket.IO server is local to the vhost host: `http://127.0.0.1:9000` (Frappe `socketio_port`). Verify with `ss -ltnp | grep 9000`.
- Backend is on a different host: point `--socket-target` at the backend's Socket.IO base.

New vhost provisioning scripts for such apps must emit the same managed markers so the helper stays idempotent. See `flutter-web-deployment.md`.

## App Configuration

- Keep `apiBaseUrl` and the site name on the backend (`backend(-dev).xealth.ca`).
- Point `socketBaseUrl` at the frontend host (`employee(-dev).xealth.ca`, `adminpanel(-dev).xealth.ca`).
- Build the socket URL as `{socketBaseUrl}/{siteName}` so the namespace stays the backend site; the proxy forwards `X-Frappe-Site-Name` as the backend host.
- Send the routing header `X-Frappe-Site-Name` from the client, and authenticate with the app's credential scheme (`token <key>:<secret>` or `FlutterDevice`). Header-authenticated browser sockets use polling.

## Local Development

- Run the frontend on the Frappe site hostname on a different port (Flutter `--web-hostname <site>`).
- Local socket base `<scheme>://<site>:9000`, namespace `/<site>`.
- `developer_mode: 1` must be in `sites/common_site_config.json` so the Node process rewrites the frontend origin port to the webserver port for its auth call; restart the Node process after changing it. Do not enable developer mode in production.

## Verification

- `.agents/scripts/add_socketio_proxy.sh --check` reports `present`.
- Same-origin handshake returns the frontend origin in the CORS header:

```bash
curl -i "https://<frontend>/socket.io/?EIO=4&transport=polling" -H "Origin: https://<frontend>"
```

Expect `200` and `Access-Control-Allow-Origin: https://<frontend>` (not the backend host).
- `nginx -t` passes and nginx reloads.
- In the browser, confirm no CORS errors and that live updates arrive; inspect Socket.IO packet bodies, not just HTTP 200/204.
