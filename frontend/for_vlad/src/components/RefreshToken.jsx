 // функция для обновление токена
 export const refreshToken = async (token) => {
  try {
    const response = await fetch(`http://moais-dashboard.ru:8082/api/refresh_token?token=${token}`, {
      method: 'POST',
    });
    const data = await response.json();
    return data.newToken;
  } catch (error) {
    throw new Error('Failed to refresh token');
  }
};

// функция - чек запрос с авто обработкой 401 ерор
export const fetchWithTokenRefresh = async (url, options) => {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      if (response.status === 401) {
        const newToken = await refreshToken(localStorage.getItem('token'));
        localStorage.setItem('token', newToken);
        const updatedOptions = {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${newToken}`,
          },
        };
        return await fetch(url, updatedOptions);
      }
      throw new Error('Request failed');
    }
    return response;
  } catch (error) {
    throw new Error('Request failed');
  }
};
  