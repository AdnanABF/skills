---
name: frontend-design-consistency
description: Use when implementing or visually changing frontend screens or components on any platform or framework to match the existing app's UI and component design patterns.
---

# Frontend Design Consistency

## When To Use

Apply before implementing a new frontend screen/component or changing an existing one's visual presentation, regardless of platform or framework.

Pure backend work, transport-only changes, and copy-only corrections that do not change presentation do not require a visual audit. For a new app with no established UI, follow its approved design direction and establish reusable patterns rather than inventing a different style for each screen.

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

- Compare the changed UI with the identified reference screens: header, type hierarchy, surfaces, spacing, icons, actions, and applicable data states should belong to the same app.
- Check touched code for unnecessary one-off styles and duplicated shared components.
- Exercise affected actions and keyboard operation at relevant mobile, tablet, and desktop sizes, including long content where applicable.
- Run the platform's analysis/tests. Report which visual and runtime checks actually ran and which remain unverified.
