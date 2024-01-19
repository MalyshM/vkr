import { createContext, useContext, useRef } from 'react';

const NumberItemsContext = createContext();

export const NumberItemsProvider = ({ children }) => {
  const numberOfItemsRef = useRef(null);

  return (
    <NumberItemsContext.Provider value={numberOfItemsRef}>
      {children}
    </NumberItemsContext.Provider>
  );
};

export const useNumberItems = () => {
  return useContext(NumberItemsContext);
};
