---
name: frontend-design-consistency
description: Use when implementing or visually changing frontend screens or components, or connecting a working prototype UI to real backend data, while preserving the existing app's UI and component design patterns.
---

# Frontend Design Consistency

## When To Use

Apply before implementing a new frontend screen/component, changing an existing one's visual presentation, or integrating a working prototype with real backend data, regardless of platform or framework. Prototype integration activates this skill even when no visual change is intended: preserving the existing UI is part of the task.

Pure backend work, transport-only changes, and copy-only corrections that do not change presentation do not require a visual audit. For a new app with no established UI, follow its approved design direction and establish reusable patterns rather than inventing a different style for each screen.

## Working Prototype + Real Backend: Integrate, Do Not Redesign

- When the user asks to connect an existing working prototype to a real backend, treat that prototype as the approved UI baseline. Backend integration is **not** permission to redesign or replace it. This applies to every frontend platform, not only browser apps.
- Preserve the screen composition and user journey: shell/navigation, headers, cards, table columns, form sections, wizard step count and order, side rails, action placement, dialogs, uploads, typography, spacing, density, colors, icons, and responsive behavior. Do not replace them with generic API-backed forms, tables, framework-default controls, or a newly invented layout merely because the data becomes asynchronous.
- Inspect the actual prototype and its shared components first. Capture representative before screenshots when browser/runtime access permits; otherwise inspect the source and existing screenshots and state the verification limit. For an integration-only request, the working target screen is the primary reference—not an unrelated screen used to justify a redesign.
- Adapt the data layer to the existing presentation. Prefer repositories/services, response-to-view-model mappings, canonical-ID/readable-label adapters, and feature-local state or hooks over rewriting the screen's markup and styles. Internal refactoring is allowed when it preserves the rendered design and intended interactions.
- Small, targeted improvements are allowed when they support integration or fix a usability defect: inline validation, loading/error/retry feedback, pending/disabled states, accessible focus handling, real uploads, searchable live selectors, or a compact workflow action using the existing component style. Keep them local; an improvement must not become a wholesale UI rewrite.
- Material changes require explicit UI approval first: replacing the page layout/component system, restructuring navigation, adding/removing/reordering wizard steps, changing table/form presentation, or removing established task surfaces. A backend implementation plan, new required fields, or a preference for standardization does not by itself authorize these changes. Explain the smallest necessary adjustment and obtain approval before proceeding.
- Preserve existing capabilities and recognizable information areas. Replace mock values with real records without silently removing cards, controls, or entire sections. When the backend cannot yet support an area, retain its established presentation with an honest empty/unavailable state or clearly disabled action; explain significant gaps. Never preserve fake metrics, source links, uploads, approvals, or success claims merely to make the screen look populated.
- Wire new approval/review behavior into the existing task surface and shared dialogs/buttons where practical. Do not turn backend workflow integration into an unrelated new frontend design.

## Inspect Before Implementing

- Review the app's overall visual language, not only the file being edited. Inspect the theme/design tokens, shared component library, app shell/navigation, and comparable screens in the same product.
- Inspect at least one comparable screen and representative components from elsewhere in the app when available. Prefer maintained, repeated patterns over an isolated legacy screen.
- Identify the established patterns for colors, typography, spacing, content widths, density, surfaces, borders, radii, shadows, icons, headers, buttons, and loading/empty/error states.
- Check how those patterns adapt across the app's supported device classes and themes. Use existing screenshots or a running app when available; distinguish source inspection from runtime verification.
- State the reference screens/components used when reporting the work. If existing patterns conflict materially and there is no clear maintained standard, clarify the intended direction rather than guessing a redesign.

## Implement Within The Existing Design Language

- Reuse existing shared components and theme tokens before creating alternatives. Extend a shared component when appropriate without changing unrelated consumers.
- Match composition and component behavior as well as colors. Inheriting a theme alone is not sufficient if header structure, card treatment, action placement, spacing, or states look unrelated to the rest of the app.
- Do not introduce framework-default controls, new palettes, fonts, icon families, decorative treatments, or one-off component variants that conflict with established patterns.
- Keep feature-specific presentation local; promote genuinely cross-feature patterns into the app's shared component layer. Do not force feature-specific models or data loading into shared visual components.
- Preserve accessibility, readable contrast, keyboard focus, and responsive behavior. Do not copy an existing usability defect merely for visual consistency.
- A consistency fix is not authorization for an app-wide redesign. Broader visual changes require explicit scope; keep intentional redesigns distinct from routine feature implementation.

## Companions

- Read the matching behavioral `frontend-*` skills, then the platform implementation adapter. This skill supplements rather than replaces their requirements.
- Read `frontend-device-layout.md` when layout or responsive behavior changes, and `frontend-ui-states.md` when data-state presentation changes.
- Flutter theme/token implementation belongs in `flutter-theming.md`; shared widget boundaries belong in `flutter-common-widgets.md`.

## Verification

- For prototype-to-backend integration, compare before and after at equivalent data states and viewport sizes. Check the actual original layout, wizard steps, side panels, controls, styling, and navigation—not just whether API requests succeed. Distinguish real-data differences from layout changes, and label mocked browser checks as such.
- Review the diff for replaced working screens, large CSS/markup rewrites, added wizard steps, removed capabilities, or unnecessary new presentation components. Every material visual departure needs explicit approval; report any small intentional improvements and any unavailable backend areas.
- Compare the changed UI with the identified reference screens: header, type hierarchy, surfaces, spacing, icons, actions, and applicable data states should belong to the same app.
- Check touched code for unnecessary one-off styles and duplicated shared components.
- Exercise affected actions and keyboard operation at relevant mobile, tablet, and desktop sizes, including long content where applicable.
- Run the platform's analysis/tests. Report which visual and runtime checks actually ran and which remain unverified.
