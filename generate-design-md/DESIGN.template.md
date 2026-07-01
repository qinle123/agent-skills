---
version: alpha
name: <Design System Name>
description: <Short description of the visual system>
colors:
  primary: "#000000"
  secondary: "#666666"
  accent: "#0055ff"
  surface: "#ffffff"
  surface-muted: "#f5f5f5"
  text: "#111111"
  text-muted: "#6b7280"
  border: "#e5e7eb"
typography:
  h1:
    fontFamily: <Heading Font>
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.1
  h2:
    fontFamily: <Heading Font>
    fontSize: 2rem
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: <Body Font>
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  label-sm:
    fontFamily: <Body Font>
    fontSize: 0.875rem
    fontWeight: 500
    lineHeight: 1.4
rounded:
  sm: 6px
  md: 10px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 12px
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: 12px
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: 16px
---

## Overview

<Describe the dominant product feeling in one short paragraph. Focus on the existing system rather than an aspirational redesign.>

## Colors

- **Primary:** <What this color is used for in the current system>
- **Secondary:** <Where supporting tones appear>
- **Accent:** <How sparingly or prominently the accent is used>
- **Surface:** <Background and panel usage>
- **Border:** <Divider, input, and card edge usage>

## Typography

- **Headings:** <How display text behaves in the current product>
- **Body:** <Default reading tone and density>
- **Labels and UI text:** <How compact labels, buttons, and metadata should feel>

## Layout

- <Describe spacing rhythm, density, and page composition>
- <Note whether the system feels compact, roomy, editorial, dashboard-like, etc.>
- <Mention any stable grid, container width, or section spacing patterns if known>

## Elevation & Depth

- <Describe shadows, borders, layering, and whether depth is subtle or prominent>
- <If the system mainly uses borders instead of shadows, say so explicitly>

## Shapes

- <Describe the role of rounded corners, sharp edges, pills, or geometric motifs>
- <Call out where stronger radius is acceptable and where it should stay restrained>

## Components

- **Buttons:** <Default visual weight, primary vs secondary hierarchy, and interaction tone>
- **Inputs:** <How fields, selects, and textareas should read>
- **Cards:** <How grouped information is separated>
- **Navigation:** <If applicable, describe tabs, sidebars, top nav, or breadcrumb style>

## Do's and Don'ts

### Do

- <Repeat stable visual patterns already present in the system>
- <Preserve the current density and hierarchy>
- <Use the accent color with the same restraint or emphasis as existing pages>

### Don't

- <Do not introduce a second visual language that conflicts with existing screens>
- <Do not add one-off colors, oversized radius, or flashy effects unless already part of the system>
- <Do not turn a restrained product UI into a generic marketing-style interface>
