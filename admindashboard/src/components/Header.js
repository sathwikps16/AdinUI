import React, { useState } from 'react';
import profile from '../img/profile.png';
import search from '../img/search.png';
import notification from '../img/notification.png';
import settingsIcon from '../img/settings.png';
import logoutIcon from '../img/logout.png';
import "./Styles/Header.css"
const Header = () => {
    const [dropdownOpen, setDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setDropdownOpen((prevState) => !prevState);
    };

    return (
        <header className="header">
            {/* Logo Section */}
            <div className="logosec">
                <div className="logo">NETBOT</div>
            </div>

            {/* Search Bar Section */}
            <div className="searchbar">
                <input type="text" placeholder="Search" />
                <div className="searchbtn">
                    <img src={search} className="icn srchicn" alt="search-icon" />
                </div>
            </div>

            {/* Message and Profile Section */}
            <div className="message">
                {/* Notifications */}
                <div className="circle"></div>
                <img src={notification} className="icn" alt="notification-icon" />

                {/* Profile Section */}
                <div className="profile-section">
                    <img
                        src={profile}
                        className="dpicn"
                        alt="profile"
                        onClick={toggleDropdown}
                    />
                    {dropdownOpen && (
                        <div className="dropdown-menu">
                            <div className="dropdown-item">
                                <img src={settingsIcon} alt="Settings" />
                                <span>Settings</span>
                            </div>
                            <div className="dropdown-item">
                                <img src={logoutIcon} alt="Logout" />
                                <span>Logout</span>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;
