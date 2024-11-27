// Nav.js
import React from 'react';
import { Link } from 'react-router-dom';

const Nav = () => {
    return (
        <div className="navcontainer">
            <nav className="nav">
                <div className="nav-upper-options">
                    <div className="nav-option option1">
                        <img
                            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210182148/Untitled-design-(29).png"
                            className="nav-img"
                            alt="dashboard"
                        />
                        <Link to="/" style={{ textDecoration: 'none', color: 'black' }}>
                            <h3>Dashboard</h3>
                        </Link>
                    </div>

                    <div className="nav-option option2" >
                        <img
                            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210183320/5.png"
                            className="nav-img"
                            alt="Knowledge Base"
                        />
                        <Link to="/knowledge-base" style={{ textDecoration: 'none', color: 'black'}}>
                            <h3>Knowledge Base</h3>
                        </Link>
                    </div>

                    <div className="nav-option option3">
                        <img
                            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210183323/10.png"
                            className="nav-img"
                            alt="All integrations"
                        />
                        <h3>Integrations</h3>
                    </div>

                    <div className="nav-option option4">
                        <img
                            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210183320/4.png"
                            className="nav-img"
                            alt="settings"
                        />
                        <h3>Settings</h3>
                    </div>

                    <div className="nav-option logout">
                        <img
                            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210183321/7.png"
                            className="nav-img"
                            alt="logout button"
                        />
                        <h3>Logout</h3>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Nav;
