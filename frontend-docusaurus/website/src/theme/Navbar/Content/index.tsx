import React from 'react';
import {useThemeConfig} from '@docusaurus/theme-common';
import {
  splitNavbarItems,
  useNavbarMobileSidebar,
} from '@docusaurus/theme-common/internal';
import NavbarItem from '@theme/NavbarItem';
import NavbarColorModeToggle from '@theme/Navbar/ColorModeToggle';
import SearchBar from '@theme/SearchBar';
import NavbarMobileSidebarToggle from '@theme/Navbar/MobileSidebar/Toggle';
import NavbarLogo from '@theme/Navbar/Logo';
import NavbarSearch from '@theme/Navbar/Search';
import {useAuth} from '../../../contexts/AuthContext.tsx';
import UserProfile from '../../../components/UserProfile/index.tsx';
import type {Props} from '@theme/Navbar/Content';

import styles from './styles.module.css';

function NavbarItems({items}) {
  return (
    <>
      {items.map((item, i) => (
        <NavbarItem {...item} key={i} />
      ))}
    </>
  );
}
function NavbarContentLayout({left, right}) {
  return (
    <div className="navbar__inner">
      <div className="navbar__items">{left}</div>
      <div className="navbar__items navbar__items--right">{right}</div>
    </div>
  );
}
export default function NavbarContent({className}: Props): JSX.Element {
  const mobileSidebar = useNavbarMobileSidebar();
  const items = useThemeConfig().navbar.items;
  const [leftItems, rightItems] = splitNavbarItems(items);
  const searchBarItem = items.find((item) => item.type === 'search');

  const {user, logout} = useAuth();

  return (
    <NavbarContentLayout
      left={
        // TODO stop hardcoding items?
        <>
          {!mobileSidebar.disabled && <NavbarMobileSidebarToggle />}
          <NavbarLogo />
          <NavbarItems items={leftItems} />
        </>
      }
      right={
        // TODO stop hardcoding items?
        // Use A provided an item with type "search" - this might be a mistake
        <>
          <NavbarItems items={rightItems.filter(item => item.label !== 'Sign In' && item.label !== 'Sign Up')} />
          <NavbarColorModeToggle className={styles.colorModeToggle} />
          {!searchBarItem && (
            <NavbarSearch>
              <SearchBar />
            </NavbarSearch>
          )}
          {!user ? (
            <>
              <NavbarItem to="/signin" label="Sign In" />
              <NavbarItem to="/signup" label="Sign Up" />
            </>
          ) : (
            <>
              <UserProfile />
            </>
          )}
        </>
      }
    />
  );
}