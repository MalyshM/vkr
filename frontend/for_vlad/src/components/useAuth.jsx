// СТАРАЯ РЕАЛИЗАЦИЯ
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



// import React, { createContext, useContext, useState, useEffect } from 'react';

// const AuthContext = createContext();

// const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }

//   const { userToken: initialToken, setUserToken: setContextUserToken } = context;
//   const [userToken, setUserToken] = useState(initialToken);

//   useEffect(() => {
//     const token = localStorage.getItem('token');
//     const tokenExpiration = localStorage.getItem('tokenExpiration');
//     const currentTime = new Date().getTime();

//     if (token && tokenExpiration) {
//       if (currentTime < parseInt(tokenExpiration)) {
//         setUserToken(token);
//       } else {
//         refreshToken();
//       }
//     }
//   }, []);

//   const setTokenWithExpiry = (token, expiration) => {
//     localStorage.setItem('token', token);
//     localStorage.setItem('tokenExpiration', expiration);
//     setUserToken(token);
//   };

//   const refreshToken = () => {
//     // Логика обновления токена
//     const newToken = 'новый_токен'; // Замените это на вашу логику обновления токена
//     const newExpiration = new Date().getTime() + (30 * 60 * 1000); 
//     setTokenWithExpiry(newToken, newExpiration);
//   };

//   const clearUserToken = () => {
//     localStorage.removeItem('token');
//     localStorage.removeItem('tokenExpiration');
//     setUserToken('');
//   };

//   return { userToken, refreshToken, clearUserToken };
// };

// const AuthProvider = ({ children }) => {
//   const [userToken, setUserToken] = useState(localStorage.getItem('token') || '');

//   return (
//     <AuthContext.Provider value={{ userToken, setUserToken }}>
//       {children}
//     </AuthContext.Provider>
//   );
// };
// export { AuthProvider, useAuth };