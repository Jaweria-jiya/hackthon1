import React, {type ComponentProps, type ReactNode, useState} from 'react';
import clsx from 'clsx';
import {ThemeClassNames, useThemeConfig} from '@docusaurus/theme-common';
import {
  useHideableNavbar,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import {translate} from '@docusaurus/Translate';
import NavbarMobileSidebar from '@theme/Navbar/MobileSidebar';
import type {Props} from '@theme/Navbar/Layout';

import styles from './styles.module.css';
import authStyles from './auth.module.css'; // Import new auth-specific styles

import Link from '@docusaurus/Link'; // Import Link
import { useAuth } from '@site/src/contexts/AuthContext'; // Import useAuth


function NavbarBackdrop(props: ComponentProps<'div'>) {
  return (
    <div
      role="presentation"
      {...props}
      className={clsx('navbar-sidebar__backdrop', props.className)}
    />
  );
}

export default function NavbarLayout({children}: Props): ReactNode {
  const {
    navbar: {hideOnScroll, style},
  } = useThemeConfig();
  const mobileSidebar = useNavbarMobileSidebar();
  const {navbarRef, isNavbarVisible} = useHideableNavbar(hideOnScroll);
  const { user, logout, loading } = useAuth(); // Use the auth hook
  const [isDropdownOpen, setIsDropdownOpen] = useState(false); // State for dropdown

  // Helper function to get avatar text
  const getAvatarText = (email: string, name?: string) => {
    if (name && name.length > 0) return name[0].toUpperCase();
    return email[0].toUpperCase();
  };


  return (
    <nav
      ref={navbarRef}
      aria-label={translate({
        id: 'theme.NavBar.navAriaLabel',
        message: 'Main',
        description: 'The ARIA label for the main navigation',
      })}
      className={clsx(
        ThemeClassNames.layout.navbar.container,
        'navbar',
        'navbar--fixed-top',
        hideOnScroll && [
          styles.navbarHideable,
          !isNavbarVisible && styles.navbarHidden,
        ],
        {
          'navbar--dark': style === 'dark',
          'navbar--primary': style === 'primary',
          'navbar-sidebar--show': mobileSidebar.shown,
        },
      )}>
      <div className="navbar__inner">
        {children}
      </div>
      <NavbarBackdrop onClick={mobileSidebar.toggle} />
      <NavbarMobileSidebar />
    </nav>
  );
}
