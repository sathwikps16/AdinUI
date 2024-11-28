//main.js

import React from 'react';

const Main = () => {
    return (
        <div className="main">
            {/* Welcome message */}
            <h1 className="welcome-message">Welcome to admin dashboard</h1>
            <p className="dashboard-description">
                Manage your data efficiently and explore all features available to administrators.
            </p>

            {/* Search bar */}
            <div className="searchbar2">
                <input type="text" name="search" id="search" placeholder="Search" />
                <div className="searchbtn">
                    <img
                        src="../img/search.png"
                        className="icn srchicn"
                        alt="search-button"
                    />
                </div>
            </div>
        </div>
    );
};

export default Main;
