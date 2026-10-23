# Penpot MCP Execution Reference

## Discover and Inspect

1. Discover the Penpot tools exposed by the current environment. In Code Mode, use the tool catalog and call the exact returned paths through `execute`; do not infer additional tools.
2. Read `high_level_overview` once per conversation before other Penpot tools. If already read, use that context rather than calling it again.
3. Look up the required types/members through `penpot_api_info` before relying on unfamiliar API methods.
4. Inspect the connected file identity using documented APIs. List pages with `penpotUtils.getPages()`, resolve the intended page, and inspect a bounded structure with `penpotUtils.shapeStructure(page.root, 3)`.
5. Inspect target assets and layout before mutation. If using the selection as a target, copy it into `storage` immediately: selection can change between calls. Keep scope explicit across calls and pages.

Available server tools can differ from those mentioned by the overview. For example, discover whether an export/preview tool is actually exposed. If not, consult documented API export capabilities; report the limitation if no usable visual inspection route exists.

## Safe Mutation

- Use the server's `execute_code` only for scoped Penpot API operations. For a review-only task, run only inspection code.
- Use `storage` for target IDs, intermediate results, and useful helpers. Revalidate stored targets before subsequent changes; do not assume old selection or active-page state remains current.
- Use native editable elements. Use documented APIs for paths, text, interactions, components, variants, and tokens; do not assume Penpot has a dedicated automatic architecture connector/router.
- Name pages, boards, and meaningful elements semantically. Architecture connector paths should remain editable and be checked again after node movement.
- Reuse assets before creating new ones. Avoid duplicate components or token sets during retries. Inspect the result of a failed batch before retrying: mutations may have partially completed.
- Work in small batches that can be inspected. Keep a record of newly created IDs and changed targets for the session. Do not delete user elements for cleanup.
- Do not treat `remove()` as reparenting. Use documented append/insert operations, preserving intended coordinates and containment.
- For flex/grid boards, change layout properties instead of fighting auto-layout with manual child coordinates. Use `penpotUtils` helpers rather than reimplementing search and layout utilities.
- Shape width/height and bounds are read-only; use `resize()`. Replace full fills/strokes arrays rather than mutating their entries. Use uppercase hex colors.
- Text resizing does not resize font glyphs. Check text bounds and restore intended growth mode after resizing; allow asynchronous layout to settle before measuring.
- Avoid returning complete file trees or logging the same data you return. Return concise IDs, summaries, and verification results.

## Inspect and Report

After each meaningful batch:

1. Re-read the affected structure, relevant geometry, text, and layout.
2. Use containment helpers such as `penpotUtils.isContainedIn` and `analyzeDescendants` where appropriate; distinguish intended overlays from accidental overflow.
3. Export/preview relevant boards using tools or documented API capabilities actually available. Inspect the image for clipping, overlap, alignment, contrast, and diagram legibility; structural checks alone do not establish visual quality.
4. Check configured prototype triggers and destinations. Test in the prototype viewer when accessible; otherwise report “configured, not viewer-tested.”
5. Report completed changes, remaining issues, and unverified checks. Do not claim merely obtaining the overview proves a live file connection, or that a successful API mutation proves the finished design looks correct.
