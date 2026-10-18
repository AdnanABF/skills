# Sync Release-Gate Reference

The reference client is `flutter_apps/syncapp/`. Backend policy is owned by
`apps/flutter_utils/`; no app-specific backend endpoint was needed.

## Source Map

Paths below are relative to the Sync client directory:

| File | Responsibility |
|---|---|
| `lib/app.dart` | Bounded startup lookup, root BLoC ownership, navigator observer, lifecycle and sheet hosts |
| `lib/features/sync/data/app_settings_repository.dart` | Public release request, installed version/platform lookup, typed release state |
| `lib/features/sync/bloc/app_release_bloc.dart` | Checks, timeout/failure handling, session dismissal, queued foreground refresh |
| `lib/features/sync/bloc/app_release_event.dart` | Manual check, resume, optional dismissal inputs |
| `lib/features/sync/bloc/app_release_state.dart` | Confirmed release, checking/error/dismissed state, blocking/sheet decisions |
| `lib/features/sync/widgets/app_release_lifecycle.dart` | Root `AppLifecycleListener.onResume` dispatch, disposal |
| `lib/features/sync/widgets/app_release_navigation_guard.dart` | Root route pop entries and Android Back policy |
| `lib/features/sync/widgets/sync_release_gate.dart` | App-wide sheet placement, branded blocking backdrop, focus/semantics/barrier |
| `lib/features/sync/widgets/sync_release_sheet.dart` | Shared sheet presentation, optional drag controller, store/support launches |
| `lib/core/platform/push_registrar.dart` | Existing push identifier to align with release requests |
| `docs/app_release_controls.md` | Operator configuration and expected behavior |

The logical identifier used by this reference is `sync_dating`; it is not a
universal Flutter Utils identifier. Inspect the target app's existing push
registration and config when selecting one for a new app.

## Important Integration Details

- Sync's shared client uses `Options(extra: {'public': true})` for this request.
  Other apps may use a different explicit auth-mode API; follow their client.
- The host is in `MaterialApp.builder`, outside the root navigator. This avoids
  another route/dialog covering a blocking release sheet. A root navigator
  observer registers `PopEntry` on routes; changing policy updates its
  `canPopNotifier`. Unregister and dispose these entries/subscriptions correctly.
  A `PopScope` above the navigator alone does not register against its routes.
- The underlying route tree stays mounted. Blocking policy hides its visuals,
  focus, and semantics behind branding; it does not reset login or forms.
- Startup checks are bounded and run alongside independent product config.
  Resume/manual checks have a bounded timeout and retain confirmed gates on
  failure. Resume arriving mid-check queues one fresh request and ignores the
  older result for policy changes.
- Optional dismissal lasts for the process session; forced/maintenance results
  override it. No recurring timer or realtime backend change was added.
- Earlier full-screen update/maintenance view files may remain in the client.
  The current integration uses `SyncReleaseSheet`; do not select obsolete views
  merely because they exist.

## Tests to Read

- `test/app_release_state_test.dart`: public request, installed platform/version,
  safe parsing, force-update conditions.
- `test/app_release_bloc_test.dart`: failure preservation, concurrency, queued
  resume, timeout, optional-dismissal persistence.
- `test/app_release_gate_test.dart`: bottom-sheet behavior, swipe dismissal,
  precedence, link validation, route coverage and Back handling.
- `test/app_release_lifecycle_test.dart`: background/foreground checks and sheet
  recovery without restarting; lifecycle callback disposal.

These tests establish mocked behavior, not that the deployed site has matching
settings, users have the latest client build, or an actual store URL is correct.

## Backend Sources

- `apps/flutter_utils/docs/app-settings.md`: endpoint, operator controls,
  version comparison, and response contract.
- `apps/flutter_utils/flutter_utils/api/app_settings.py`: public endpoint.
- `apps/flutter_utils/flutter_utils/app_settings.py`: release-state decisions.
- `apps/flutter_utils/flutter_utils/flutter_utils/doctype/flutter_utils_settings/`:
  settings schema and validation.
- `apps/flutter_utils/flutter_utils/tests/test_app_settings.py`: backend contract
  tests; use the backend's own comparison rather than duplicating it in Dart.
