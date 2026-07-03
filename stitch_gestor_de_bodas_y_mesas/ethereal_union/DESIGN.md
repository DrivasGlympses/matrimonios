---
name: Ethereal Union
colors:
  surface: '#f7f9ff'
  surface-dim: '#d5dae2'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4fc'
  surface-container: '#e9eef6'
  surface-container-high: '#e3e9f0'
  surface-container-highest: '#dde3eb'
  on-surface: '#161c22'
  on-surface-variant: '#4d4447'
  inverse-surface: '#2b3137'
  inverse-on-surface: '#ecf1f9'
  outline: '#7f7477'
  outline-variant: '#d0c3c6'
  surface-tint: '#6b5a5f'
  primary: '#6b5a5f'
  on-primary: '#ffffff'
  primary-container: '#f8e1e7'
  on-primary-container: '#746368'
  inverse-primary: '#d7c1c7'
  secondary: '#735c00'
  on-secondary: '#ffffff'
  secondary-container: '#fed65b'
  on-secondary-container: '#745c00'
  tertiary: '#5d5f5f'
  on-tertiary: '#ffffff'
  tertiary-container: '#e7e7e7'
  on-tertiary-container: '#666768'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#f4dde3'
  primary-fixed-dim: '#d7c1c7'
  on-primary-fixed: '#24181c'
  on-primary-fixed-variant: '#524348'
  secondary-fixed: '#ffe088'
  secondary-fixed-dim: '#e9c349'
  on-secondary-fixed: '#241a00'
  on-secondary-fixed-variant: '#574500'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#f7f9ff'
  on-background: '#161c22'
  surface-variant: '#dde3eb'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-md-mobile:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  title-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '500'
    lineHeight: '1.5'
    letterSpacing: 0.01em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: 0.1em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
---

## Brand & Style

The design system is anchored in a philosophy of "Refined Celebration." It targets a premium market of couples and wedding planners who value meticulous organization as much as romantic aesthetics. The emotional response should be one of calm confidence—reducing the stress of planning through structured elegance.

The design style is **Modern Editorial**. It blends the high-contrast sophistication of fashion magazines with the functional clarity of a professional SaaS platform. We utilize generous white space (luxury's greatest marker) and a focus on "Soft Layering" to create depth without visual noise. The interface avoids heavy borders, favoring subtle tonal shifts and delicate champagne accents to guide the user’s eye.

## Colors

The palette is designed to evoke a sense of warmth and timelessness. 

- **Primary (Blush):** Used primarily for soft backgrounds, highlight areas, and subtle callouts. It provides the "romantic" foundation without being overwhelming.
- **Secondary (Champagne Gold):** Reserved for interactive elements, primary CTAs, and decorative accents (like icons or thin separators). It signifies luxury and premium status.
- **Surface (White):** The dominant canvas color. All cards and main content areas sit on a pure white field to maintain a clean, organized feel.
- **Text (Deep Slate):** A high-contrast grey (#2F353B) is used instead of pure black to keep the interface feeling "soft" while ensuring maximum legibility for dense planning data.

## Typography

This design system uses a traditional "Serif-Display, Sans-UI" pairing. 

- **Playfair Display** handles all major headings. Its high-contrast strokes and elegant serifs provide the romantic, editorial feel. 
- **Inter** is utilized for all functional UI elements, body copy, and data inputs. It was chosen for its exceptional legibility at small sizes and comprehensive character support, ensuring that guest lists and budget sheets remain easy to scan.
- **Letter Spacing:** Headlines use slight negative tracking for a tighter, premium look. Labels and small navigational items use increased tracking (10%) in all-caps to denote authority and hierarchy.

## Layout & Spacing

The layout philosophy follows a **Fixed Centered Grid** on desktop and a **Fluid Single Column** on mobile. 

- **The 8px Rhythm:** All spacing between elements must be a multiple of 8. This ensures a consistent vertical cadence across complex dashboards.
- **Margins:** Large outer margins (64px+) on desktop create a "letterhead" feel, framing the content as if it were on high-end stationery.
- **Grid:** A 12-column grid is used for desktop layouts. For planning tools (dashboards), elements typically span 4 or 6 columns to prevent data from feeling cramped.

## Elevation & Depth

To maintain an elegant and light atmosphere, the design system avoids heavy shadows and dark overlays.

- **Ambient Shadows:** We use a "Whisper Shadow" for cards—a very wide, ultra-low opacity (4-6%) shadow tinted with the secondary Champagne color. This makes elements feel as though they are floating slightly above a soft surface.
- **Tonal Layering:** Depth is primarily communicated through color shifts. A background might be Blush (#F8E1E7), while the active card surface is Pure White (#FFFFFF).
- **Glassmorphism:** Use a subtle backdrop blur (12px) with a semi-transparent white fill (80% opacity) for sticky navigation bars to maintain context while scrolling through long guest lists or itineraries.

## Shapes

The shape language is **Soft and Structural**. 

While the brand is romantic, it is also professional. We use a base corner radius of `4px` (Soft) for most UI components like input fields and small buttons. This provides a hint of approachability without losing the precision and "sharpness" associated with high-end luxury brands. 

Larger containers, such as modal windows or primary content cards, may use a larger radius (`8px`) to feel more welcoming. Circular shapes are reserved strictly for user avatars or specific decorative icon backgrounds.

## Components

- **Buttons:** 
  - *Primary:* Solid Champagne Gold (#D4AF37) with white text. No border.
  - *Secondary:* White background with a thin (1px) Champagne Gold border.
  - *Shape:* All buttons have a 4px corner radius and generous horizontal padding.
- **Input Fields:** 
  - Use a minimal "Floating Label" style. The bottom border is a subtle grey, which turns Champagne Gold on focus. Avoid heavy box-style inputs to keep the forms feeling light.
- **Cards:** 
  - White background, 4px radius, and a "Whisper Shadow." Content inside cards should have at least 32px of internal padding to maintain the editorial look.
- **Chips & Tags:** 
  - Used for RSVP status or budget categories. Use the Blush color (#F8E1E7) for the background with a darkened version of the same hue for the text.
- **Specialty Components:** 
  - *Timeline Tracker:* A vertical line in Champagne Gold with small pearl-like nodes to track wedding countdown milestones.
  - *Image Gallery:* Images should use "Soft" corner radii and be arranged in an asymmetrical masonry grid to evoke a scrapbook or mood-board aesthetic.