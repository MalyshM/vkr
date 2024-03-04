

// const AuthContext = createContext();

// const updateUserToken = (newToken) => {
//   setUserToken(newToken);
// };


// const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };

// const AuthProvider = ({ children }) => {
//   const [userToken, setUserToken] = useState(localStorage.getItem('token') || '');

//   return (
//     <AuthContext.Provider value={{ userToken, updateUserToken  }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export { AuthProvider, useAuth };
// 1
// 2
// import { createContext, useContext, useState } from 'react';
// const AuthContext = createContext();

// const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };

// const { setUserToken } = context;


// const updateUserToken = (token) => {
//   // Обновите логику обновления токена, например, обновление состояния пользователя или сохранение в localStorage
//   console.log('Updating user token:', token);
//   // Вместо console.log() вы можете выполнить другие действия, в зависимости от вашей логики
// };

// const AuthProvider = ({ children }) => {
//   const [userToken, setUserToken] = useState(localStorage.getItem('token') || '');



//   return (
//     <AuthContext.Provider value={{ userToken, updateUserToken }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export { AuthProvider, useAuth, updateUserToken };

import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  const { userToken, setUserToken: setContextUserToken } = context;

  const setUserToken = (token) => {
    // Обновите логику обновления токена, например, обновление состояния пользователя или сохранение в localStorage
    setContextUserToken(token);
    localStorage.setItem('token', token);
    console.log('Setting user token:', token);
  };

  const updateUserToken = (token) => {
    setContextUserToken(token);
    localStorage.setItem('token', token);

  };

  const clearUserToken = () => {
    // Очищаем состояние и удаляем значение из localStorage
    setContextUserToken('');
    localStorage.removeItem('token');
  };


  return { userToken, setUserToken, updateUserToken,clearUserToken  };
};

const AuthProvider = ({ children }) => {
  const [userToken, setUserToken] = useState(localStorage.getItem('token') || '');

  return (
    <AuthContext.Provider value={{ userToken, setUserToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthProvider, useAuth };
