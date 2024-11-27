import React, { createContext, useState } from 'react';

// Create the context
const MyContext = createContext();

// This is the context provider component
export const MyContextProvider = ({ children }) => {
  const [contextValue, setContextValue] = useState("Hello, world!"); // You can set this value to anything you want

  return (
    <MyContext.Provider value={contextValue}>
      {children} {/* All children of this provider will have access to the context */}
    </MyContext.Provider>
  );
};

export default MyContext;
