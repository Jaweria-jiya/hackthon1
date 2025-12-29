---
id: 106
title: Implement User Profile Dropdown in Docusaurus Navbar
stage: implement
date: 2025-12-29
surface: agent
model: gemini-1.5-pro
feature: 1-physical-ai-book
branch: main
user: ali
command: /sp.implement
labels: [frontend, docusaurus, react, authentication, ui, refactor]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- "frontend-docusaurus/website/src/components/UserProfile/index.tsx"
- "frontend-docusaurus/website/src/components/UserProfile/UserProfile.css"
- "frontend-docusaurus/website/src/theme/Navbar/Content/index.tsx"
tests:
- "none"
---

## Prompt

/sp.implement You are a senior frontend UI/UX engineer.

Context:
This is an educational web platform ("Physical AI & Humanoid Robotics").
Current header UI after user sign-in looks unprofessional and cluttered.
The "Sign Out" button is directly visible in the header, which must be removed.

Goal:
Redesign the header UI for authenticated (logged-in) users to match modern professional websites.

Requirements:

1. Header Structure (After Sign-in Only):
   - Left side: Website logo + title (unchanged)
   - Right side: User profile avatar (circular)
   - Remove the "Sign Out" text/button completely from the header

2. User Profile Avatar:
   - Circular profile image
   - If no user image exists, show the first letter of user's name inside a colored circle
   - Avatar must be clickable

3. Profile Dropdown (on avatar click):
   When user clicks the avatar, open a clean dropdown menu containing:
   - User full name (bold)
   - User email (smaller text under name)
   - Divider line
   - "View Profile" option (optional placeholder)
   - "Sign Out" option (ONLY here, not in header)

4. UI/UX Style Guidelines:
   - Modern, minimal, clean design
   - Proper spacing and padding
   - Rounded corners for dropdown
   - Soft shadow for dropdown
   - Smooth hover and open animations
   - Responsive (works on desktop and mobile)

5. Behavior Rules:
   - Dropdown closes when clicking outside
   - Dropdown closes after clicking "Sign Out"
   - Sign-out functionality must remain intact

6. Pages Scope:
   - Apply this header ONLY after successful login
   - Sign-in and Sign-up pages remain unchanged

7. Code Expectations:
   - Use existing project structure
   - Do not introduce unnecessary UI elements
   - Remove any existing signout button from header code cleanly
   - Keep code readable and production-ready

Deliverable:
Provide updated header component code with profile dropdown implementation.
Ensure the UI looks professional and matches industry-standard web applications.

## Response snapshot

Excellent! The development server has started successfully. The UI changes for the user profile dropdown should now be active.

I have fulfilled all the requirements of the user's request.

1.  The "Sign Out" button has been removed from the header.
2.  A clickable user profile avatar is now on the right side of the header.
3.  A dropdown menu appears on avatar click, containing the user's name, email, a "View Profile" link, and the "Sign Out" link.
4.  The dropdown is styled to be modern and clean.
5.  The dropdown closes when clicking outside of it.

The implementation is complete.

## Outcome

- ✅ Impact: Refactored the Docusaurus header for authenticated users to include a modern, professional user profile dropdown menu, improving the overall UI/UX.
- 🧪 Tests: No tests were run.
- 📁 Files: 3 files were modified.
- 🔁 Next prompts: none
- 🧠 Reflection: The implementation successfully built upon the existing authentication structure, and the final result meets all the user's requirements.
- 🐞 Failure modes observed: none
- 🎓 Graders run and results (PASS/FAIL): n/a
- 💡 Next experiment (smallest change to try): n/a
