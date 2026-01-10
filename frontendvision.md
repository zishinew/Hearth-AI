# Project Vision: "ForeverHome" (Hackathon MVP)

## 1. Project Context
We are building a B2C search tool MVP in a 24-hour hackathon context.
**Goal:** Help elderly users visualize accessibility renovations in potential new homes to support "aging in place."
**Core Mechanism:** Users paste a Realtor.ca link -> System scrapes images (Apify) -> AI (Gemini Nano) analyzes/modifies images -> UI displays renovations + estimated costs.

## 2. Target Audience & UX Principles
* **Primary User:** Elderly individuals looking to downsize.
* **Design Philosophy:** "Accessibility First."
    * **Typography:** Large, readable sans-serif fonts (e.g., Inter or Plus Jakarta Sans). Minimum 16px body text.
    * **Contrast:** High contrast ratios (WCAG AAA preferred).
    * **Navigation:** Simple, clear labels. No hidden menus. Large clickable hit areas (buttons).
    * **Tone:** Trustworthy, calm, clear, and reassuring.

## 3. Tech Stack Requirements
* **Framework:** Next.js (App Router) + TypeScript.
* **Styling:** Tailwind CSS.
* **UI Library:** shadcn/ui (Buttons, Inputs, Cards, Skeleton loaders).
* **Icons:** Lucide React.
* **Specialized Libraries:**
    * `react-compare-slider` (CRITICAL: For the Before/After visualization).
    * `embla-carousel-react` (For the image carousels).

## 4. Page Architecture

### A. Landing Page (`/`)
* **Layout:** Centered, clean, welcoming.
* **Hero Section:**
    * **Headline:** Clear value prop (e.g., "Find a home that grows with you").
    * **Input:** A prominent, large Search Bar accepting a URL (placeholder: "Paste Realtor.ca link here...").
    * **Action:** Large "Analyze Home" button.
* **Trust Section:**
    * **Image Carousel:** An automated carousel showing "Success Stories" (examples of accessible renovations).
* **Footer:** Simple copyright/links.

### B. Analysis Results Page (`/report`)
* **State:** Needs a robust "Loading/Analyzing" skeleton state while AI processes the link.
* **Layout:** Two-Column Desktop Layout (Responsive stack on mobile).

#### Left Sidebar (30% width)
* **Property Details:**
    * Address/Location (Large text).
    * Listing Price.
* **Renovation Metrics:**
    * **Accessibility Score:** A visual gauge or score (0-100) indicating current safety.
    * **Estimated Renovation Cost:** Large, highlighted number (e.g., "+$15,000 to renovate").
    * **Total "Move-In" Cost:** Listing Price + Reno Cost.

#### Right Main Area (70% width)
* **Primary Feature:** The "Transformation" Viewer.
    * Use `react-compare-slider`.
    * **Left Image:** Original photo (e.g., steep stairs).
    * **Right Image:** AI-generated renovation (e.g., stairs with a lift or ramp).
    * **Caption:** Explanation of the change (e.g., "Added reinforced handrails and stair lift").
* **Gallery:**
    * Horizontal scroll/carousel below the main viewer containing other photos from the listing (both original and processed).

## 5. Hackathon Execution Rules
1.  **Mock Data First:** Hardcode a "Golden Path" demo first. Create a mock object with a sample Realtor.ca link, a sample "Before" image, and a sample "After" image so we can perfect the UI before hooking up the backend.
2.  **Speed over Perfection:** Use standard Tailwind spacing and shadcn components. Do not spend hours on custom CSS animations.
3.  **Error Handling:** If the URL is invalid, show a friendly, large error message.

## 6. Color Palette
* **Background:** Off-white / Cream (`#FAFAF9`) to reduce eye strain (pure white can be harsh).
* **Primary Action:** A safe, trusted Blue (`#2563EB`) or Warm Teal.
* **Text:** Dark Slate (`#1E293B`) for high contrast, never pure black.
* **Alerts:**
    * High Cost/Danger: Muted Red.
    * Safe/Accessible: Muted Green.