import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './UserProfile.css';

const UserProfile = () => {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setDropdownOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!user) {
    return null;
  }

  const getInitials = (name: string, email: string) => {
    if (name) {
      return name[0].toUpperCase();
    }
    if (email) {
      return email[0].toUpperCase();
    }
    return '';
  };

  const hashCode = (str: string) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
  };

  const intToRGB = (i: number) => {
    const c = (i & 0x00FFFFFF)
      .toString(16)
      .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
  };

  const handleSignOut = () => {
    setDropdownOpen(false);
    logout();
  };

  return (
    <div className="profile-container" ref={dropdownRef}>
      <div className="profile-avatar-container" onClick={() => setDropdownOpen(!dropdownOpen)}>
        {user.photoUrl ? (
          <img src={user.photoUrl} alt={user.name || user.email} className="profile-avatar-image" />
        ) : (
          <div className="profile-avatar-initials" style={{ backgroundColor: `#${intToRGB(hashCode(user.email))}` }}>
            {getInitials(user.name, user.email)}
          </div>
        )}
      </div>
      {dropdownOpen && (
        <div className="profile-dropdown">
          <div className="user-info">
            <strong>{user.name || 'User'}</strong>
            <small>{user.email}</small>
          </div>
          <hr />
          <a href="#" className="dropdown-item">View Profile</a>
          <a href="#" onClick={handleSignOut} className="dropdown-item">Sign Out</a>
        </div>
      )}
    </div>
  );
};

export default UserProfile;

