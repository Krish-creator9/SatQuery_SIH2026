---
name: Orbital Precision
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#849495'
  outline-variant: '#3a494b'
  surface-tint: '#00dbe7'
  primary: '#e1fdff'
  on-primary: '#00363a'
  primary-container: '#00f2ff'
  on-primary-container: '#006a71'
  inverse-primary: '#00696f'
  secondary: '#adc6ff'
  on-secondary: '#002e6a'
  secondary-container: '#0566d9'
  on-secondary-container: '#e6ecff'
  tertiary: '#f7f6ff'
  on-tertiary: '#2b303e'
  tertiary-container: '#d6daec'
  on-tertiary-container: '#5a5f6f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#74f5ff'
  primary-fixed-dim: '#00dbe7'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#dee2f4'
  tertiary-fixed-dim: '#c2c6d8'
  on-tertiary-fixed: '#161b28'
  on-tertiary-fixed-variant: '#424655'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
typography:
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Geist
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.05em
  data-mono-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 26px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
---

## Brand & Style

The design system is engineered for a high-performance geospatial intelligence environment. It prioritizes a **Modern/Glassmorphic** aesthetic that balances scientific rigor with cutting-edge technology. The interface aims to evoke a sense of "mission control"—sophisticated, authoritative, and deeply technical, yet accessible through a refined information hierarchy.

The visual narrative centers on clarity amidst complexity. By utilizing deep space tones and vibrant, light-emitting accents, the system differentiates between the vast "unknown" (data pools) and the "insight" (AI-driven findings). The emotional response should be one of absolute trust in the data and a feeling of being at the forefront of satellite reconnaissance.

## Colors

This design system utilizes a high-contrast dark theme to reduce eye strain during prolonged analysis and to make geospatial data visualization pop.

- **Primary (Electric Cyan):** Reserved for critical action states, focus indicators, and active data points. It represents the "pulse" of the AI.
- **Secondary (Tech Blue):** Used for primary navigation, secondary actions, and progress indicators. It provides a professional, stable counterweight to the vibrant cyan.
- **Surface Tiers:** 
  - **Base (#0B0F19):** The foundational canvas.
  - **Container (#161B28):** Used for panels, sidebars, and card backgrounds to create subtle structural separation.
- **Functional Colors:** 
  - Success: Emerald Green for positive query results.
  - Alert: Vivid Orange for anomalies or high-priority intelligence updates.

## Typography

The typography system employs a dual-font strategy to separate UI narrative from raw data.

- **UI & Body (Geist/Inter):** Geist is used for headings to provide a sharp, technical edge. Inter is used for body copy to ensure maximum legibility across dense reports.
- **Metadata & Logs (JetBrains Mono):** All coordinates, timestamps, JSON snippets, and system logs must use the monospace face. This creates a clear visual "bracket" for technical output, distinguishing it from human-readable interface text.
- **Scaling:** Headings should reduce by approximately 20% on mobile devices to maintain vertical space for map views.

## Layout & Spacing

The layout is a **Fluid Grid** system optimized for multi-pane dashboard configurations. It follows a 4px baseline rhythm.

- **Grid Model:** 12-column system for desktop. Sidebars for filters and metadata should be fixed (approx 320px) while the primary map/data visualization remains fluid.
- **Density:** High information density is expected. Use "MD" (16px) spacing for primary structural gaps and "SM" (8px) for internal component padding.
- **Mobile Adaptation:** On mobile, sidebars collapse into bottom sheets or slide-over overlays to keep the map view unobstructed.

## Elevation & Depth

Depth is established through **Glassmorphism and Tonal Layering** rather than traditional heavy shadows.

- **Surfaces:** Use semi-transparent backgrounds (e.g., `rgba(22, 27, 40, 0.7)`) with a `backdrop-filter: blur(12px)`.
- **Borders:** Every container must have a subtle 1px border (`#ffffff15`) to define its edges against the map or dark background.
- **Active Glow:** Interactive elements in an active or hovered state should emit a soft, localized glow using the primary cyan (`box-shadow: 0 0 15px rgba(0, 242, 255, 0.3)`).
- **Stacking:** Use three primary Z-index tiers:
    1. Base Map (0)
    2. Persistent UI Panels (10)
    3. Overlays/Modals/Tooltips (100)

## Shapes

The design system utilizes **Rounded (2)** geometry to soften the technical nature of the data and make the interface feel modern and approachable.

- **Containers/Cards:** Use `rounded-lg` (16px) for main dashboard panels.
- **Interactive Elements:** Use `rounded-md` (8px) for buttons and input fields.
- **Visual Markers:** Map markers and status pips should be fully circular to distinguish them from structural UI elements.

## Components

- **Buttons:** Primary buttons use a solid Tech Blue background with white text. Ghost buttons use a Cyan border and text. On hover, a subtle inner glow should activate.
- **Glass Cards:** All containers should utilize the 1px border and backdrop blur. Title areas within cards should have a subtle bottom border to separate headers from content.
- **Input Fields:** Darker than the container background, with a 1px border that turns Electric Cyan on focus. Use JetBrains Mono for text entry in coordinate or query fields.
- **Data Chips:** Small, rounded-full elements with low-opacity Tech Blue backgrounds and high-contrast text for tagging satellite IDs or sensor types.
- **Execution Logs:** A dedicated component with a terminal-like appearance, using a black background, JetBrains Mono font, and color-coded status prefixes ([INFO], [WARN], [SUCCESS]).
- **Status Indicators:** Use pulsing animations for "Live" data streams to indicate active satellite connectivity.