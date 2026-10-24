The canonical workspace rules and skill index live in `.agents/AGENTS.md`.
Before starting any task, identify which platform you are working on and read the relevant skill files from `.agents/skills/`.
Skills use the OpenCode package format at `.agents/skills/<name>/SKILL.md`. References in this file and skill documents use the shorthand `<name>.md`; for example, `frontend-forms.md` means `.agents/skills/frontend-forms/SKILL.md`.
For frontend/UI work, read the shared `frontend-*` product and interaction skills first, then the platform-specific implementation adapter.
For backend work, any external API call or long-running function must not block the request unless synchronous behavior is explicitly required. Persist local state first and run the external work in a background job.

## Platforms

| Platform | Location | Stack |
|----------|----------|-------|
| Mobile apps | `flutter_apps/*/`, `omor/omor_app/` | Flutter, Dio, BLoC |
| Web app | `next_apps/masarnext/` | Next.js, TypeScript, CSS Modules |
| React web apps | `react_apps/*/` | React, TypeScript, Vite; shared browser API client |
| Masar Admin | `flutter_apps/masar_admin/` | Flutter, BLoC, desktop-first, web/Chrome deployment |
| Backend | `apps/masar/` + other Frappe apps | Python, Frappe framework |

## COREAXIS LMS

COREAXIS LMS consists of a shared Frappe backend and Flutter administrator and student applications. This project mapping is tenant-neutral; production connections and deployment details belong in tenant-specific documentation.

### Components and Local Connections

| Component | Location | Required local URL |
|-----------|----------|--------------------|
| Backend / Frappe Desk | `apps/lms_custom/` | `http://lms.localhost:8000` |
| Admin frontend | `flutter_apps/frappe_lms_admin/` | `http://lmsadmin.localhost:8083` |
| Student frontend | `flutter_apps/frappe_lms_student/` | `http://lmsstudent.localhost:8084` |

These addresses define the required local setup; they do not imply that the site or services are already configured or running.

- The local Frappe site name is `lms.localhost`. Both frontends use `http://lms.localhost:8000` as their API base URL.
- Reserve port `8083` for the admin frontend and `8084` for the student frontend. Use the listed URLs for local runs, manual testing, and browser automation; do not silently fall back to another port.
- Run the admin Flutter web app with `--web-hostname lmsadmin.localhost --web-port 8083` and the student app with `--web-hostname lmsstudent.localhost --web-port 8084`.
- All three hostnames must resolve to the local development machine.
- Frappe CORS must allow `http://lmsadmin.localhost:8083` and `http://lmsstudent.localhost:8084`. If cookie authentication or realtime is used, configure those connections for the separate frontend origins as well.
- The separate frontend hostnames are an explicit COREAXIS LMS exception to the same-hostname convention in `project-connections.md`. This local connection table takes precedence for these two frontends.

### API Configuration References

| Component | Configuration file |
|-----------|--------------------|
| Admin frontend | `flutter_apps/frappe_lms_admin/lib/core/config/app_config.dart` |
| Student frontend | `flutter_apps/frappe_lms_student/lib/core/config/app_config.dart` |

Both Flutter applications support an `API_BASE_URL` override. Read backend URLs from application configuration and use the local backend URL above for this setup.

## Reading Order

### Scope And Precedence

- Route by the behavior being changed, not every surface present in the file. A copy-only correction does not activate form, layout, networking, or state-management skills unless those behaviors also change. Platform-wide requirements such as Flutter linting still apply.
- Required companions apply when their stated trigger is met. Optional companions are not a blanket reading list. Follow the sequences below for the relevant workflow, not for unrelated edits inside that workflow's files.
- Keep product rules in shared skills and implementation rules in platform adapters. This file owns routing, precedence, and workspace connections; avoid copying detailed skill rules here.
- Reading a deployment, release, or destructive-action skill does not authorize executing those actions. Explanation-only requests remain read-only.
- Treat recommendations as defaults with documented workflow exceptions. Security, permissions, data integrity, and explicit workspace constraints remain requirements; do not invent exceptions to them.

1. Identify the platform and product surface: admin, public, auth, listing, form, mobile, tablet, desktop, or backend.
2. For any frontend/UI work, read the matching platform-agnostic `frontend-*` skill first.
   For new screens/components or visual changes on any platform/framework, read `frontend-design-consistency.md` first: inspect the app's overall UI, shared components, and comparable screens, then follow the established design patterns. Copy-only and nonvisual logic changes do not require this visual audit.
3. Then read the platform adapter: Flutter, Next.js, Frappe Desk, or backend.
4. If a platform adapter and a `frontend-*` skill overlap, the `frontend-*` file owns product/UI behavior and the platform file owns implementation syntax, component paths, persistence, APIs, and tooling.

For browser-hosted mobile app concepts with a desktop client journey, realistic device frame, and mobile PWA fallback, read `frontend-device-layout.md` and then `frontend-mobile-app-prototyping.md` before the platform adapter.

For safe-area or PWA layout work in prototypes or production apps, read `frontend-device-layout.md` before the platform adapter. Next.js apps also read `nextjs-responsive-scaling.md` for browser inset implementation. Production PWA layout does not require the prototyping skill unless a desktop review/device-frame presentation is involved.

For admin detail pages, read `frontend-admin-panels.md`, `frontend-forms.md`, `frontend-ui-states.md`, and then `frontend-admin-detail-pages.md` before the platform adapter. If the detail form renders tabs or fields from metadata/schema, read `frontend-dynamic-tabs-fields.md` after `frontend-admin-detail-pages.md` and before the platform adapter.

For admin listing pages, read `frontend-admin-panels.md`, `frontend-listing-screens.md`, and `frontend-ui-states.md` before the platform adapter. If the listing renders columns, filters, search fields, or sort options from metadata/schema, read `frontend-dynamic-listing-fields.md` after `frontend-ui-states.md` and before the platform adapter.

For Frappe-backed listing pages that must update from server-side create, update, delete, workflow, or background-job changes, read `frappe-listing-realtime.md` after the listing platform adapter.

For connecting a frontend to Frappe Socket.IO realtime from its own domain (cross-origin CORS/origin errors, `/socket.io` nginx proxy, socket base host), read `setup-frappe-realtime.md` after the platform adapter and before the deployment adapter.

For any work that adds, changes, reviews, or optimizes multiple API calls or remote data loads, read `api-parallelization.md` alongside the platform adapter.

For any frontend API-client, authentication-header, credential-persistence, or networking change on any platform, read `frontend-api-client.md` before the platform adapter. It owns shared transport/auth behavior; platform adapters own implementation syntax and storage. For Frappe auth, also read `frappe-api-contracts.md`. React/Vite fetch guidance is in the shared skill's browser-client reference.

For any creation, update, review, API response, or frontend display of Frappe Notification Log records, read `frappe-notification-log.md` alongside the platform adapter.

For Pipecat self-hosting and production deployment, read `pipecat-self-hosting.md` and `github-actions-deployment.md`. The skill uses uv and systemd by default and includes Docker guidance for existing containerized bots.

For creating, configuring, or reviewing project-wide scheduled PR watchers, read `project-connections.md` first, then `project-pr-watcher.md`, followed by all applicable review and deployment skills. Discover connected repositories before defining the explicit authorized review/merge/deployment scope.

## Skills

### Platform-Agnostic Frontend UI

| Skill | When to apply |
|-------|---------------|
| `frontend-design-consistency.md` | New or visually changed screens/components on any platform: inspect the app's overall UI, theme, shared components, and comparable screens, and follow their established design patterns |
| `frontend-device-layout.md` | Any desktop, tablet, mobile, responsive behavior, safe areas, prototype or production PWA layout, proportional scaling, admin density, or mobile fallback decision |
| `frontend-mobile-app-prototyping.md` | Any browser-hosted clickable mobile app concept with production-oriented structure, a desktop client journey navigator, realistic device frame, or mobile PWA presentation |
| `frontend-listing-screens.md` | Any listing/table/index screen UX: pagination, search/filter/refresh/add header, row actions, table headers, loading/empty/error states, bulk selection, page-size options, and persistence |
| `frontend-dynamic-listing-fields.md` | Any admin listing where columns, standard filters, search fields, or sort options are generated from Frappe DocType metadata, Frappe listview settings, or another schema |
| `frontend-admin-detail-pages.md` | Any admin detail/profile/edit page UX: app bar identity, editable tabbed form sections, right overview rail, save/reset placement, loading/error/saving states |
| `frontend-dynamic-tabs-fields.md` | Any admin detail form where tabs, sections, or fields are generated from Frappe DocType metadata or another schema |
| `frontend-forms.md` | Any form UX: layout, validation, field behavior, selection components, save-state behavior, keyboard/input intent, and dummy-data linkage |
| `frontend-ui-states.md` | Shared loading, empty, error, retry, no-results, and no-data behavior across frontend surfaces |
| `frontend-auth-entry-ui.md` | Login, signup, OTP, authentication entry, and account access UI across desktop, tablet, and mobile |
| `frontend-admin-panels.md` | Any admin/back-office UI, operator workflow, density, task surface, confirmation, and recovery behavior |
| `frontend-interaction-patterns.md` | Cross-surface interaction rules: destructive actions, confirmations, modals, Escape key dialog closing, recovery after failures, action language, and refresh behavior |
| `frontend-video-player-controls.md` | Video playback controls, inactivity auto-hide timing, and player interaction behavior |
| `frontend-button-clicks.md` | Any button click, form submission, or generic action to ensure proper unfocus and haptic feedback |
| `frontend-country-code-picker.md` | Country code picker visual and interaction standard across platforms |
| `frontend-carousels.md` | Carousel/slider UX, behavior, responsiveness, accessibility, and content rules |
| `frontend-dummy-data.md` | Dev-only random data filling behavior for frontend forms |
| `frontend-strategy.md` | Legacy frontend guidance bridge to the current `frontend-*` skill set |

### Flutter Implementation

| Skill | When to apply |
|-------|---------------|
| `flutter-architecture.md` | Structuring Flutter projects, creating new features |
| `flutter-state-management.md` | Adding or modifying Flutter state logic |
| `flutter-networking.md` | API calls, Dio setup, repositories |
| `flutter-linting.md` | All Flutter code changes |
| `flutter-theming.md` | Flutter `ThemeData`, `Theme.of(context)`, notifications, local fonts, and animation implementation |
| `flutter-common-widgets.md` | Flutter shared widget placement, `lib/core/widgets/`, one-widget-per-file rules, and reusable component boundaries |
| `flutter-color-icon-picker.md` | Flutter color and icon pickers for Frappe-backed admin forms |
| `flutter-mobile-branding.md` | Flutter mobile app branding with app icons, native launch image/splash packages, display names, in-app splash, auth identity, and theme colors |
| `flutter-admin-branding.md` | Any Flutter admin app branding/rebranding, logo, splash, login identity, favicon/PWA metadata, or shell brand colors |
| `flutter-web-deployment.md` | Flutter web deploy scripts, nginx setup, certbot setup, static artifact sync, and GitHub Actions workflows |
| `flutter-utilities.md` | Auth flow plumbing, splash, webview, HTML, env |
| `flutter-app-release-gates.md` | Flutter Utils optional/forced updates, temporary-unavailable bottom sheets, startup/resume checks; also apply during new Flutter mobile GitHub/store deployment setup |
| `flutter-listing-screens.md` | Flutter implementation adapter for listing screens. Read `frontend-listing-screens.md` first |
| `flutter-forms.md` | Flutter implementation adapter for forms. Read `frontend-forms.md` first |
| `flutter-dialogs.md` | Flutter dialogs, modal route actions, focus behavior, and overlays above WebViews or platform views |
| `flutter-document-approval.md` | Flutter admin linked-document listing, preview, file actions, and approval/rejection workflows |
| `flutter-routing.md` | Navigation, route setup |
| `flutter-android-release.md` | Flutter Android appbundle, Play Store, and Fastlane release scripts |
| `flutter-ios-release.md` | Flutter iOS release, App Store, TestFlight, Xcode Organizer, Xcode Cloud ci_post_clone.sh, CocoaPods, and Swift Package Manager setup |
| `flutter-deploy.md` | Flutter development/production branch promotion, version incrementing, release scripts, and deployment-result confirmation |
| `flutter-phone-auth.md` | Use when implementing or fixing mobile phone authentication, OTP login, or registration flows powered by flutter_utils |

### Next.js Implementation

| Skill | When to apply |
|-------|---------------|
| `nextjs-architecture.md` | Project structure, features, API routes, shared utilities |
| `nextjs-page-performance.md` | Any new/edited `page.tsx`, or any route slow to open from nav. Never block SSR on data not needed for first paint; fetch on the client |
| `nextjs-responsive-scaling.md` | Next.js responsive CSS, viewport sizing, scroll ownership, safe areas, and prototype/production PWA shells; Masar conventions are in its reference. Read `frontend-device-layout.md` first |
| `nextjs-listing-screens.md` | Next.js implementation adapter for listing/index pages. Read `frontend-listing-screens.md` first |
| `nextjs-carousels.md` | Swiper-specific carousel implementation. Read `frontend-carousels.md` first |
| `nextjs-empty-states.md` | Next.js empty-state component adapter. Read `frontend-ui-states.md` first |
| `nextjs-forms.md` | Next.js implementation adapter for forms. Read `frontend-forms.md` first |
| `nextjs-deployment.md` | Next.js deploy scripts, nginx setup, PM2, and production web deploy flow |

### Backend And Frappe

| Skill | When to apply |
|-------|---------------|
| `frappe-python.md` | Any Python / Frappe backend code |
| `frappe-api-contracts.md` | Any Frappe API used by Flutter, Next.js, or other external clients |
| `frappe-async-external-apis.md` | Any backend flow that calls external APIs, webhooks, storage providers, or other long-running functions |
| `frappe-file-images.md` | Any backend API that uploads, stores, or returns files or image fields |
| `frappe-customizations.md` | Frappe doctype customizations, patches |
| `frappe-app-branding.md` | CoreAxis Frappe application branding |
| `frappe-document-approval-flow.md` | Generic Frappe document upload, verification, approval, and rejection flows |
| `frappe-app-navigation.md` | Any create/edit under `apps/*/desktop_icon/` or `apps/*/workspace_sidebar/`. Read `frontend-admin-panels.md` first for admin navigation intent. **Mandatory:** always run `bench --site <site> migrate` in the same turn |
| `frappe-list-filters.md` | Frappe Desk list filter customization. Read `frontend-admin-panels.md` first; keep filters in the native list filter row in strict order |
| `frappe-listing-realtime.md` | Frappe-backed listing/index realtime refresh using standard `list_update` events. Read after `frontend-listing-screens.md` and the platform adapter; use with `frappe-realtime-updates.md` when backend code changes |
| `frappe-notification-log.md` | Any creation, update, review, API response, or frontend display of Frappe Notification Log records |
| `frappe-realtime-updates.md` | Any backend Frappe change or frontend listing/detail page that must refresh from server-pushed create, update, delete, workflow, or background-job events |
| `setup-frappe-server.md` | Setting up or configuring a Frappe server, bench, sites, apps, services, or production prerequisites |
| `setup-frappe-realtime.md` | Setting up or connecting Frappe Socket.IO realtime for a frontend served from a different domain, including the nginx `/socket.io` reverse proxy and socket base host configuration |

### Cross-Platform Technical

| Skill | When to apply |
|-------|---------------|
| `visual-explainer.md` | Visual explanations of plans, implementations, architectures, workflows, and tradeoffs using diagram-first, self-contained HTML |
| `penpot-solution-design.md` | Software architecture diagrams, user journeys, wireframes, UI systems, and clickable prototypes in Penpot through MCP; use shared frontend companions when designing their behaviors |
| `api-parallelization.md` | Any work that adds, changes, reviews, or optimizes multiple API calls or remote data loads; run independent calls in parallel wherever possible |
| `frontend-api-client.md` | Shared HTTP client ownership, auth injection, credential safety, and session expiration for any frontend platform |
| `project-connections.md` | Project app mappings, site URLs, app paths, environment config |
| `pipecat-self-hosting.md` | Pipecat self-hosting with default uv and systemd production deployment plus Docker Compose guidance for existing containerized bots |
| `github-actions-deployment.md` | Any GitHub Actions workflow that builds, releases, or deploys code, including development and production branch promotion helpers |
| `frappe-deployment.md` | Frappe app development and production deployment through GitHub Actions, `deploy`, and the remote Bench lifecycle |
| `frappe-backup.md` | Frappe site backup/download/restore sync scripts and explaining or changing backup sync flow |
| `event-based-refresh.md` | Cross-component refresh/invalidation after shared frontend context changes, such as default role/sport or active profile |
| `project-scaffolding.md` | Creating or bootstrapping applications; creating/updating local run scripts and safe restart launchers |

### Workspace Workflow

| Skill | When to apply |
|-------|---------------|
| `skill-updates.md` | Task not covered by any existing skill, or creating/updating skills in the `.agents/skills` catalog |
| `project-local-feature-branches.md` | Local-only feature branches, preserving working changes, and isolating feature commits from open PRs in one working folder |
| `erp-assistant.md` | Read-only live CoreAxis ERP record inspection, search, analysis, reporting, and proposed change plans through MCP; not application implementation or ERP mutation execution |
| `project-manager.md` | Read-only live CoreAxis ERP project health, tasks, deadlines, milestones, dependencies, risks, and status briefs; read `erp-assistant.md` first |
| `project-pr-watcher.md` | Project-wide scheduled PR watcher discovery, review, blocker comments, protected merges, dependency-aware deployment, and durable recovery |

### Compatibility Adapters

| Skill | When to apply |
|-------|---------------|
| `admin-panels.md` | Legacy references that should route to `frontend-admin-panels.md` |
| `country-code-picker.md` | Legacy references that should route to `frontend-country-code-picker.md` |
| `login-screen-ui.md` | Legacy references that should route to `frontend-auth-entry-ui.md` |

## Visual Planning Agent

- Select `visual-planner` for collaborative feature planning with diagram-first HTML documentation, not application implementation. The complete canonical definition, including its permissions, is `.agents/agents/visual-planner.md`.
- OpenCode discovers it through the project-local symlink `.opencode/agents/visual-planner.md`. No global configuration or duplicate definition is required; `opencode.json` continues to register workspace instructions and skills.
- The agent uses `visual-explainer.md` for visual artifacts and reads other skills only when their behavior is being designed. Discuss first; write documentation when requested. Built-in Plan mode remains read-only outside its permitted plan directory.
- Choose the target project's own `docs/` and existing conventions; default to `docs/features/<feature-name>.html`. Multiple projects may each have a `docs/` directory. Ask when ownership is unclear; use root documentation only for workspace-wide topics.
- The agent may edit documentation only beneath exact `docs` directory segments inside `/home/lubshad/frappe-bench`. Its permissions deny shell execution, delegation, and external tools. The workspace boundary is installation-specific and must be reviewed if this catalog moves.
- Plan approval is not implementation authorization. Switch to an implementation agent for application changes, deployments, migrations, agent/skill maintenance, or validation requiring tools unavailable to the planner.

## Completion Evidence

- Report checks actually run, their results, and relevant checks left unverified. Do not describe a planned check as passed.
- UI changes: check affected interactions, keyboard operation, and relevant viewport sizes; copy-only changes need not trigger unrelated interaction testing.
- API changes: check permissions, invalid inputs, and the response contract. Background-job changes also check enqueue/commit ordering, observable failure state, and retry safety where applicable.
- Deployment work: distinguish workflow started, build passed, deployment completed, and live behavior verified. Report only the stages supported by evidence.

## Catalog Quality

Validate the skill catalog after changing skills or `.agents/AGENTS.md`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 .agents/scripts/validate_skills.py
PYTHONDONTWRITEBYTECODE=1 python3 .agents/scripts/validate_skill_scenarios.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s .agents/scripts -p 'test_*.py'
```

The catalog validator fails structural problems and reports content-quality warnings. Scenario checks validate active references and explicit required/forbidden skill and action expectations. See `.agents/skills/routing-scenarios.md` for the schema and limitations; these checks do not evaluate model prompt understanding.
