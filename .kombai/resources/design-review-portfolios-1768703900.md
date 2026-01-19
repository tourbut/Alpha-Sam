# Design Review Results: Portfolios Page

**Review Date**: January 18, 2026
**Route**: `/portfolios`
**Focus Areas**: Performance (bundle size, render performance, optimization)

## Summary

The portfolios page suffers from severe performance issues primarily due to massive bundle sizes. The page loads 7MB of JavaScript, with the Flowbite Icons library alone accounting for 3.26MB (46% of total). Chart.js is loaded even in the empty state, and the INP (Interaction to Next Paint) metric of 944ms indicates sluggish interactivity.

## Issues

| # | Issue | Criticality | Location |
|---|-------|-------------|----------|
| 1 | Entire Flowbite Icons library loaded (3.26MB) instead of selective imports | 🔴 Critical | `frontend/src/routes/portfolios/+page.svelte:6` |
| 2 | Chart.js loaded eagerly even when no portfolios exist (empty state) | 🔴 Critical | `frontend/src/routes/portfolios/+page.svelte:9`<br>`frontend/src/lib/components/portfolio/PortfolioPieChart.svelte:2` |
| 3 | Total bundle size of 7MB is excessive for a simple portfolios listing page | 🔴 Critical | Overall architecture |
| 4 | INP (Interaction to Next Paint) of 944ms far exceeds recommended 200ms threshold | 🟠 High | Overall performance |
| 5 | Flowbite Svelte component library bundle is 1.4MB | 🟠 High | Throughout codebase |
| 6 | No lazy loading of PortfolioPieChart component when portfolios exist | 🟠 High | `frontend/src/routes/portfolios/+page.svelte:147` |
| 7 | Chart.js registering all components instead of only required ones | 🟡 Medium | `frontend/src/lib/components/portfolio/PortfolioPieChart.svelte:26` |
| 8 | Mock data hardcoded in component instead of loaded from API | 🟡 Medium | `frontend/src/routes/portfolios/+page.svelte:36-61` |
| 9 | Multiple icon imports from flowbite-svelte-icons without tree shaking | 🟡 Medium | `frontend/src/routes/portfolios/+page.svelte:6` |
| 10 | No route-level code splitting for portfolios feature | 🟡 Medium | `frontend/src/routes/portfolios/+page.svelte` |
| 11 | Entire Chart library loaded but only doughnut chart type is used | 🟡 Medium | `frontend/src/lib/components/portfolio/PortfolioPieChart.svelte:26` |
| 12 | Hover scale animation (scale-[1.02]) triggers layout reflow | ⚪ Low | `frontend/src/routes/portfolios/+page.svelte:107` |

## Criticality Legend
- 🔴 **Critical**: Breaks functionality or violates accessibility standards  
- 🟠 **High**: Significantly impacts user experience or design quality
- 🟡 **Medium**: Noticeable issue that should be addressed
- ⚪ **Low**: Nice-to-have improvement

## Detailed Recommendations

### 1. Icon Library Optimization (Critical - 3.26MB savings)

**Current**: Importing entire `flowbite-svelte-icons` library
```svelte
import { PlusOutline, WalletSolid, ArrowRightOutline } from "flowbite-svelte-icons";
```

**Recommended**: Use individual icon imports or switch to a lighter icon library
```svelte
// Option A: Individual imports (if package supports it)
import PlusOutline from "flowbite-svelte-icons/PlusOutline";
import WalletSolid from "flowbite-svelte-icons/WalletSolid";
import ArrowRightOutline from "flowbite-svelte-icons/ArrowRightOutline";

// Option B: Switch to lucide-svelte (much smaller)
import { Plus, Wallet, ArrowRight } from "lucide-svelte";
```

### 2. Lazy Load Chart.js (Critical - ~500KB savings on empty state)

**Current**: Chart.js and PortfolioPieChart always imported
```svelte
import PortfolioPieChart from "$lib/components/portfolio/PortfolioPieChart.svelte";
```

**Recommended**: Dynamic import only when portfolios exist
```svelte
let PortfolioPieChart;
onMount(async () => {
  if (portfoliosWithAssets.length > 0) {
    const module = await import("$lib/components/portfolio/PortfolioPieChart.svelte");
    PortfolioPieChart = module.default;
  }
});
```

### 3. Optimize Chart.js Registration (Medium - ~200KB savings)

**Current**: Registering all Chart.js components
```javascript
Chart.register(...registerables);
```

**Recommended**: Register only required components
```javascript
import { Chart, DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js';
Chart.register(DoughnutController, ArcElement, Tooltip, Legend);
```

### 4. Implement Code Splitting (Medium)

**Recommended**: Split portfolios feature into separate chunks
```javascript
// In svelte.config.js or vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'flowbite': ['flowbite-svelte'],
          'charts': ['chart.js']
        }
      }
    }
  }
}
```

### 5. Replace Heavy Component Library (High - Architectural)

Consider replacing Flowbite Svelte with lighter alternatives:
- **shadcn-svelte**: Smaller, tree-shakeable components
- **Skeleton UI**: Lightweight Svelte component library
- **Custom components**: Build only what you need

### 6. Optimize Animations (Low)

**Current**: Using transform scale which can trigger reflow
```svelte
class="hover:scale-[1.02]"
```

**Recommended**: Use CSS transforms with will-change hint
```css
.portfolio-card {
  transition: transform 0.3s ease;
  will-change: transform;
}
.portfolio-card:hover {
  transform: scale(1.02);
}
```

## Performance Metrics Analysis

**Current Metrics**:
- **FCP**: 1280ms (Acceptable - target: <1800ms)
- **LCP**: 1280ms (Acceptable - target: <2500ms) 
- **CLS**: 0.001 (Excellent - target: <0.1)
- **INP**: 944ms (❌ Poor - target: <200ms)
- **Page Size**: 7MB (❌ Extremely Large - target: <1MB)
- **Time to Interactive**: 1280ms (Acceptable - target: <3800ms)

**Expected Metrics After Optimization**:
- **Page Size**: ~1.5MB (78% reduction)
- **INP**: ~200ms (79% improvement)
- **Time to Interactive**: ~600ms (53% improvement)

## Next Steps

**Priority 1 (Critical - Immediate Action)**:
1. Implement selective icon imports or switch to lucide-svelte
2. Add lazy loading for Chart.js component
3. Measure bundle size improvements with `vite-bundle-visualizer`

**Priority 2 (High - This Week)**:
4. Optimize Chart.js registration to include only doughnut components
5. Evaluate and plan migration from Flowbite Svelte to lighter alternative

**Priority 3 (Medium - This Sprint)**:
6. Implement route-level code splitting
7. Move mock data to API calls
8. Add bundle size budgets in CI/CD

**Priority 4 (Low - Future Enhancement)**:
9. Optimize animations with CSS transforms and will-change
10. Add performance monitoring with web-vitals library

## Bundle Analysis Summary

**Top 5 Largest Resources**:
1. flowbite-svelte-icons.js: 3.26MB (46%)
2. flowbite-svelte.js: 1.4MB (20%)
3. @sveltejs/kit/client.js: 496KB (7%)
4. chunk-PAJUT44J.js: 441KB (6%)
5. @vite/client: 179KB (3%)

**Total**: 7.0MB across 54 resources
