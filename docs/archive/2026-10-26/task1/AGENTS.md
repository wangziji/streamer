# Repository Guidelines

## Architecture & Scope

Build a home streaming music player: an Android Raspberry Pi handles sources, playback protocols, software, GUI, and controls. Custom electronics provide power, clock processing, DAC conversion, filtering, and analog output to an external amplifier. Use KiCad for electronics and Blender for 3D-printed enclosures and mechanical parts. Document the selected Pi, Android image, audio interface, and clock ownership before circuit implementation.

## Project Structure & Module Organization

- `AK4499.kicad_pro`, `AK4499.kicad_sch`, and `AK4499.kicad_pcb`: local project, schematic, and board.
- Root-level `.lib`, `.dcm`, `.kicad_sym`, and `.kicad_mod` files: custom component libraries and footprints; preserve references when moving them.
- `AK4499-backups/`: existing recovery snapshots, not production releases.
- Upstream [wangziji/streamer](https://github.com/wangziji/streamer) contains `system/aosp/` and Chinese requirements/feasibility documents named `.mk`; these documents are Markdown, not build scripts.

This directory has no Git metadata or Android sources. Confirm the checkout before committing. Blender assets and automated tests are absent; document locations when introduced. Older platform/material proposals are historical where they conflict with the scope above.

## Build, Test, and Development Commands

- `open AK4499.kicad_pro`: open the project on macOS with KiCad associated.
- In KiCad, run **Inspect → Electrical Rules Checker** for schematics and **Inspect → Design Rules Checker** for boards.
- `git diff --check`: check whitespace after working in a Git checkout.

There is no local build runner or test framework. KiCad CLI is installed at `kicad-cli`, outside PATH. Use the selected Android checkout's documented build instructions rather than assuming a generic AOSP target.

## Style & Naming Conventions

Preserve existing component references and library identifiers. Use descriptive net names such as `DAC_RESET_N` and `AVDD_5V`. Write Markdown with short sections and fenced commands. Let KiCad serialize CAD files; agents must use Konnect for CAD mutations rather than text edits. If unavailable, report the blocker. Use project-relative library paths.

## Validation Guidelines

Record ERC/DRC results and justify exclusions. Verify footprints against datasheets, power sequencing, clock compatibility, analog return paths, and connector pinouts. Bench-test supply rails, playback, sample-rate switching, mute behavior, noise, and distortion. Check enclosure clearances and print fit. Distinguish planned checks from measured results; no coverage threshold exists.

## Authoritative Circuit References

Use locally archived manufacturer specifications under `docs/specs/` as the sole authority for circuit design. Download the exact part's official datasheet before selection or design; record source URL, revision and SHA-256 in its manifest. Cite local file and page/section for design decisions. Forums, third-party articles, distributor mirrors and search snippets are not circuit evidence. Product briefs do not replace complete datasheets. Missing or restricted documents block the affected design; report gaps without substituting unofficial material.

## Commit & Pull Request Guidelines

Upstream history uses short Chinese/English summaries without a consistent prefix. Use focused, descriptive subjects. PRs should link requirements/issues, explain electrical or mechanical effects, and include schematic/layout renders, validation evidence, and unresolved risks. Keep generated fabrication files tied to a reviewed revision; exclude credentials and machine-specific caches.
