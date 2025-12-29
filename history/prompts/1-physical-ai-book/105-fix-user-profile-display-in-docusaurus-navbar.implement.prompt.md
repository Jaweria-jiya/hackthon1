---
id: 105
title: Fix User Profile Display in Docusaurus Navbar
stage: implement
date: 2025-12-29
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: main
user: ali
command: /sp.implement
labels: [frontend, docusaurus, react, authentication, ui, fix]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- "frontend-docusaurus/website/src/components/UserProfile/index.tsx"
- "frontend-docusaurus/website/src/components/UserProfile/UserProfile.css"
- "frontend-docusaurus/website/src/theme/Navbar/Content/index.tsx"
- "frontend-docusaurus/website/docusaurus.config.ts"
- "frontend-docusaurus/website/src/css/custom.css"
- "frontend-docusaurus/website/src/theme/Root.tsx"
tests:
- "none"
---

## Prompt

/sp.implement You are an expert Docusaurus developer with advanced expertise in authentication, conditional rendering in React components, and custom navbar styling using CSS and hooks like useContext for auth state.

Project: A Docusaurus book/site titled "Physical AI & Humanoid Robotics" with authentication (Sign In/Sign Up/Sign Out) and user profile display.

Current issues (based on screenshot and description):
- After user signs in, a profile is created but displays incorrectly: Not properly circular, background/image not covering the circle.
- Profile location is wrong: Appears on the left side of the header, below the "Book" name or similar.
- Navbar sequence is not ideal: Needs conditional rendering based on auth state.
- No profile photo handling: Should use user's email profile pic if available, or fallback to first letter of name/email in a colored circle.

Desired outcome:
- Conditional navbar on right side (next to GitHub):
  - If NOT logged in: "Sign In" (text link) → "Sign Up" (text link) → GitHub icon.
  - If logged in: "Sign Out" (text link, replacing Sign Up) → User Profile (circular avatar) → GitHub icon.
- Profile avatar: Circular (border-radius: 50%), size ~32px, cover the entire circle.
  - Use actual profile photo from auth provider (e.g., user.photoURL).
  - Fallback: First letter of user's name or email (e.g., "A" for "ali@example.com"), on a colored background (e.g., random or based on hash).
- Remove any misplaced profile display (e.g., on left side or below Book).
- Ensure responsive, clean, professional look; no duplicates.

Assumptions:
- Auth is set up with a context (e.g., AuthContext) providing isLoggedIn, user (with name, email, photoURL), and logout function.
- Navbar is likely swizzled for custom rendering.

Implementation steps:
1. Swizzle Navbar if not done: npx docusaurus swizzle @docusaurus/theme-classic Navbar.
2. In src/theme/Navbar/index.js:
   - Import auth hook/context (e.g., useAuth).
   - In the right items section, use conditional JSX:
     - If !isLoggedIn: Render Sign In and Sign Up links.
     - If isLoggedIn: Render Sign Out link (onClick: logout and redirect), then Profile avatar component.
   - Profile component: <div class="profile-avatar"><span>{user.name[0] || user.email[0]}</span></div> if no photo, or <img src={user.photoURL} alt="Profile" />.
3. CSS in src/css/custom.css:
   - .profile-avatar { width: 32px; height: 32px; border-radius: 50%; background-color: #ccc; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; overflow: hidden; }
   - For img: object-fit: cover;
   - Add margin for spacing next to Sign Out and GitHub.
4. If profile is appearing elsewhere (e.g., via plugin or other component), identify and remove it (e.g., check src/pages or swizzled DocItem).
5. Handle fallback: Generate color based on user ID/email hash for avatar background.

Provide:
- Swizzle command.
- Updated docusaurus.config.js if needed for navbar items.
- Full example code for swizzled Navbar/index.js with conditional logic and imports.
- CSS code block for profile styling.
- Step-by-step instructions to implement and test.
- Ensure no left-side profile remnants.

Output only the solution in a structured format with code blocks. No extra content.

## Response snapshot

I have now implemented all the necessary changes. Here is a summary of what I've done:

1.  **Created `UserProfile` component**: A new component at `frontend-docusaurus/website/src/components/UserProfile/index.tsx` to display the user's avatar, with a fallback to initials.
2.  **Styled `UserProfile` component**: Added CSS for the avatar in `frontend-docusaurus/website/src/components/UserProfile/UserProfile.css` and included it in `frontend-docusaurus/website/src/css/custom.css`.
3.  **Modified `Navbar/Content`**: Updated `frontend-docusaurus/website/src/theme/Navbar/Content/index.tsx` to conditionally render "Sign In"/"Sign Up" or "Sign Out" and the `UserProfile` component based on the authentication state.
4.  **Updated `docusaurus.config.ts`**: Removed the hardcoded "Sign In" and "Sign Up" links from the navbar configuration.
5.  **Wrapped application with `AuthProvider`**: Created `frontend-docusaurus/website/src/theme/Root.tsx` to wrap the entire application with `AuthProvider`, making the authentication context available to all components.

The implementation should now be complete and correct according to the user's request.

## Outcome

- ✅ Impact: Fixed the user profile display in the Docusaurus navbar, implementing conditional rendering for auth links and a circular avatar with a fallback.
- 🧪 Tests: No tests were run.
- 📁 Files: 6 files were created/modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The implementation followed the user's request closely, and all steps were completed successfully.
- 🐞 Failure modes observed: Incorrect relative paths caused build failures, which were resolved by correcting the paths.
- 🎓 Graders run and results (PASS/FAIL): n/a
- 💡 Next experiment (smallest change to try): n/a
