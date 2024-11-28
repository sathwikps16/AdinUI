//Header.js

import React from 'react';
import profile from '../img/profile.png'
import search from '../img/search.png'
import notification from '../img/notification.png'
const Header = () => {
    return (
        <header>
            <div class="logosec">
                <div class="logo">NETBOT</div>
            </div>

            <div class="searchbar">
                <input type="text"
                    placeholder="Search" />
                <div class="searchbtn">
                    <img src={search}
                        class="icn srchicn"
                        alt="search-icon" />
                </div>
            </div>

            <div class="message">
                <div class="circle"></div>
                <img src={notification}
                    class="icn"
                    alt="" />
                <div class="dp">
                    <img src={profile}                        
                        class="dpicn"
                        alt="dp" />
                </div>
            </div>

        </header>
    );
};

export default Header;