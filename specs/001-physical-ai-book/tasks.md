# 001-physical-ai-book - Fix Auth Flow Refactor

## Feature Name: Fix Auth Flow Refactor

This document outlines the tasks required to refactor the authentication flow, specifically addressing critical issues identified in protected routes and navbar rendering, adhering to Docusaurus best practices.

## Dependencies:
- Foundational tasks must be completed before User Story tasks.
- User Story tasks can generally be parallelized as indicated.

## Implementation Strategy:
The implementation will focus on correcting the authentication source of truth, stabilizing auth state, and implementing route protection at a Docusaurus layout/router level. The previous MDX-level protection will be removed.

---

### Phase 1: Setup

- [X] T001 Run `npm install` in `frontend-docusaurus/website` to ensure all dependencies are up to date.

---

### Phase 2: Foundational - Authentication Core Refinement

**Goal**: Ensure `access_token` is the authoritative source for authentication state and provide a loading state for stable redirects.

- [X] T002 Modify `frontend-docusaurus/website/src/contexts/AuthContext.tsx` to include a `loading` state during the initial authentication check from `localStorage`.
- [X] T003 Update `frontend-docusaurus/website/src/contexts/AuthContext.tsx`'s `useAuth` return type to expose the `loading` state.

---

### Phase 3: User Story: Refactor Doc Route Protection [US1]

**Goal**: Remove MDX-level authentication guards and implement route protection for `/docs/*` at the Docusaurus layout or router level using best practices.

**Independent Test Criteria**:
- Accessing any `/docs/*` route as an unauthenticated user redirects to `/login`.
- Accessing any `/docs/*` route as an authenticated user shows the content.
- Page refresh on a `/docs/*` page as an authenticated user does not redirect to `/login`.

- [X] T004 Remove `frontend-docusaurus/website/src/components/ProtectedRoute.tsx` as it represents an anti-pattern for Docusaurus route protection.
- [X] T005 Restore `frontend-docusaurus/website/docs/intro.mdx` to its original `.md` format and remove the `<ProtectedRoute>` wrapper.
- [X] T006 Swizzle Docusaurus `DocRoot` component to `frontend-docusaurus/website/src/theme/DocRoot/index.tsx` to allow custom route protection.
- [X] T007 Modify `frontend-docusaurus/website/src/theme/DocRoot/Layout/index.tsx` to check `useAuth().user` and `useAuth().loading` states, redirecting to `/login` if no user is found and not in loading state.
- [X] T008 Update `frontend-docusaurus/website/src/theme/Navbar/Layout/index.tsx` to handle the `loading` state before rendering user information or login/signup links.

---

### Phase 4: Polish & Cross-Cutting Concerns

**Goal**: Ensure a smooth user experience and confirm all previous fixes.

- [X] T009 Verify that login redirects exactly once to `/docs/intro`.
- [X] T010 Verify that page refresh does not redirect logged-in users to `/login`.
- [X] T011 Conduct end-to-end testing of the authentication flow to ensure no redirect loops or unexpected behavior.