# Alpha-Sam Frontend Design Prompt

**Objective**: Create a high-fidelity design for "Alpha-Sam", a Crypto Portfolio Management Application.
**Design System**: Modern, clean aesthetic similar to Flowbite-Svelte. Uses TailwindCSS utility classes.
**Theme**: Support for Light and Dark modes.
**Typography**: Inter or similar modern sans-serif.

---

## 1. Global Navigation (Navbar)
- **Position**: Fixed at the top.
- **Left**: Brand Name "Alpha-Sam" (Bold).
- **Center/Right (Authenticated)**:
  - Links: "Dashboard", "Assets", "Positions".
  - Icons/Menu: Settings Icon, User Profile/Logout.
- **Center/Right (Guest)**:
  - Buttons: "Log in" (Ghost/Text), "Sign up" (Primary Color).

## 2. Dashboard Page (`/`)
**Layout**: Grid-based dashboard.
1.  **Header**: Title "Portfolio Dashboard".
2.  **Key Metrics (Top Row)**: 4 Card Layout.
    - **Total Assets**: Number (e.g., 5).
    - **Active Positions**: Number (e.g., 3).
    - **Total Valuation**: Currency (e.g., $12,345.00).
    - **Portfolio Return**: Percentage with trend color (Green for +, Red for -).
3.  **Visualization (Middle Row)**: 2 Large Cards.
    - **Allocation**: Pie/Donut chart showing asset distribution.
    - **Performance**: Line chart showing portfolio value over time (History).
4.  **Details & Actions (Bottom Row)**: 2 Cards.
    - **Quick Actions**: Vertical stack of buttons ("Manage Assets", "Manage Positions").
    - **Summary Text**: Text-based breakdown of Total Invested vs Total Profit/Loss.

## 3. Assets Management Page (`/assets`)
**Layout**: Data-heavy view.
1.  **Header Area**:
    - Title: "Assets".
    - Action Buttons: "Refresh Prices" (Secondary/Outline), "Add Asset" (Primary/Solid).
2.  **Portfolio Summary Strip**:
    - Same 4 generic metrics (Valuation, Invested, PnL, Return) displayed in a 4-column grid.
3.  **Asset Table**:
    - **Style**: Striped or clean rows with hover effects.
    - **Columns**:
        - **Symbol**: Bold text (e.g., BTC).
        - **Name**: Asset name (e.g., Bitcoin).
        - **Category**: Tag or text (e.g., Crypto).
        - **Current Price**: Currency. Include small tooltip/icon for "Last Updated".
        - **Quantity**: Decimals supported (up to 8 places).
        - **Buy Price**: Currency (Avg. cost).
        - **Valuation**: Current Value (Price * Qty).
        - **Profit/Loss**: Currency value. Colored Green (+) or Red (-).
        - **Return Rate**: Percentage. Colored Green (+) or Red (-).
        - **Actions**: "Edit" (or "Add Position") button, "Delete" button.

## 4. Modals (Dialogs)
- **Add/Edit Asset**: Simple form with fields for Symbol, Name, Category.
- **Add/Edit Position**: Form linked to an Asset. Fields for Quantity, Buy Price per unit.

## 5. Authentication Pages
- **Login / Signup**:
    - Centered Card on screen.
    - Title: "Log in to Alpha-Sam".
    - Fields: Email, Password.
    - Primary Button: Full width.
    - Footer link: "Don't have an account? Sign up".
