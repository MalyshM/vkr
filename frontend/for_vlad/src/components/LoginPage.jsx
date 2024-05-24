import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './useAuth';
// import { Box, Heading, FormControl, FormLabel, Input, Button,Center} from '@chakra-ui/react';
import { useToast } from '@chakra-ui/react';
import { Flex, Spacer } from '@chakra-ui/react'
import { CloseIcon } from '@chakra-ui/icons'
import { fetchWithTokenRefresh } from './RefreshToken';

import { Button, Layout, Typography, Card, Form, Input, Space } from 'antd';
import { CloseOutlined } from '@ant-design/icons';

const LoginPage = () => {

  const [username, setUsername] = useState('');
  const [isUsernameEmpty, setIsUsernameEmpty] = useState(false);
  const [isUsernamePopulated, setIsUsernamePopulated] = useState(false);

  const [password, setPassword] = useState('');
  const [isPasswordEmpty, setIsPasswordEmpty] = useState(false);
  const [isPasswordPopulated, setIsPasswordPopulated] = useState(false);

  const [FIO, setFIO] = useState('');
  const [isFIOEmpty, setIsFIOEmpty] = useState(false);
  const [isFIOPopulated, setIsFIOPopulated] = useState(false);


  const [email, setEmail] = useState('');
  const [isEmailEmpty, setIsEmailEmpty] = useState(false);
  const [isEmailPopulated, setIsEmailPopulated] = useState(false);

  const [responseMessage, setResponseMessage] = useState('');

  const navigate = useNavigate();
  const { setUserToken } = useAuth();

  const toast = useToast();

  
  const handleInputChangeFIO = (e) => { // Обработчик изменения значения в поле ФИО  
    setFIO(e.target.value); // Установка нового значения ФИО
    setIsFIOEmpty(false); // Сброс состояния ошибки при изменении значения
    setIsFIOPopulated(e.target.value.trim() !== ""); //отслеживания заполненности поля
  };

  const handleInputChangeEmail = (e) => { 
    setEmail(e.target.value); 
    setIsEmailEmpty(false); 
    setIsEmailPopulated(e.target.value.trim() !== ""); 
  };

  const handleInputChangeUsername = (e) => {  
    setUsername(e.target.value);
    setIsUsernameEmpty(false); 
    setIsUsernamePopulated(e.target.value.trim() !== ""); 
  };
  const handleInputChangePas = (e) => { 
    setPassword(e.target.value); 
    setIsPasswordEmpty(false); 
    setIsPasswordPopulated(e.target.value.trim() !== ""); 
    };
  

  const handleBlurFIO = () => { // Обработчик потери фокуса с поля ФИО
    
    if (FIO.trim() === "") { // Проверка, пусто ли поле ФИО
      setIsFIOEmpty(true);
    }
  };

  const handleBlurUsername = () => { // Обработчик потери фокуса с поля ФИО
    
    if (username.trim() === "") { // Проверка, пусто ли поле ФИО
      setIsUsernameEmpty(true);
    }
  };

  const handleBlurEmail = () => { // Обработчик потери фокуса с поля ФИО
    
    if (email.trim() === "") { // Проверка, пусто ли поле ФИО
      setIsEmailEmpty(true);
    }
  };

  const handleBlurPas = () => { // Обработчик потери фокуса с поля ФИО
    
    if (password.trim() === "") { // Проверка, пусто ли поле ФИО
      setIsPasswordEmpty(true);
    }
  };



  const login = async () => {
    // Проверка на пустые поля
    if (!username || !password || !FIO || !email) {
      toast({
        title: 'Ошибка',
        description: 'Пожалуйста, заполните все поля!',
        status: 'error',
        duration: 3000, // Продолжительность отображения в миллисекундах
        isClosable: true,
      });
      return;
    }

    try {
      const response = await fetchWithTokenRefresh('http://moais-dashboard.ru:8082/api/login_standard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          FIO,
          email,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        setUserToken(result.access_token);
        setResponseMessage(`Welcome, ${username}! Access Token: ${result.access_token}`);
        navigate('/main');
      } else {
        const errorMessages = Array.isArray(result.detail) ? result.detail.map(detail => detail.msg).join(', ') : 'Unknown error';
        setResponseMessage(`Authentication failed: ${errorMessages}`);
      }
    } catch (error) {
      console.error('Error during login:', error);
      setResponseMessage('An error occurred during login.');
    }
  };


return (
  <Layout style={{ minHeight: '100vh', backgroundColor: '#00aeef', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Card
        style={{
          width: '500px',
          borderWidth: '2px',
          borderRadius: '8px',
          padding: '24px',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
          borderColor: '#1A1A1A',
          backgroundColor: 'white',
        }}
      >
        <Space style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
          <Typography.Title level={2}>Вход</Typography.Title>
          <Link to='/'>
          <Button type="text" icon={<CloseOutlined />}/>
          </Link>
        </Space>
        
        <Form layout="vertical">
          <Form.Item
            label="ФИО:"
            validateStatus={isFIOEmpty ? "error" : (isFIOPopulated ? "success" : "")}
            help={isFIOEmpty ? "Поле не может быть пустым." : ""}
          >
            <Input
              type="text"
              value={FIO}
              onChange={handleInputChangeFIO}
              onBlur={handleBlurFIO}
              placeholder="Введите ваше ФИО"
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item
            label="Логин:"
            validateStatus={isUsernameEmpty ? "error" : (isUsernamePopulated ? "success" : "")}
            help={isUsernameEmpty ? "Поле не может быть пустым." : ""}
          >
            <Input
              type="text"
              value={username}
              onChange={handleInputChangeUsername}
              onBlur={handleBlurUsername}
              placeholder="Введите ваш логин"
              autoComplete="off"
            />
          </Form.Item>

          <Form.Item
            label="Адрес электронной почты:"
            validateStatus={isEmailEmpty ? "error" : (isEmailPopulated ? "success" : "")}
            help={isEmailEmpty ? "Поле не может быть пустым." : ""}
            
          >
            <Input
              type="text"
              value={email}
              onChange={handleInputChangeEmail}
              onBlur={handleBlurEmail}
              placeholder="Введите вашу электронную почту"
              autoComplete="off"
              
            />
          </Form.Item>

          <Form.Item
            label="Пароль:"
            validateStatus={isPasswordEmpty ? "error" : (isPasswordPopulated ? "success" : "")}
            help={isPasswordEmpty ? "Поле не может быть пустым." : ""}
          >
            <Input
              type="password"
              value={password}
              onChange={handleInputChangePas}
              onBlur={handleBlurPas}
              placeholder="Введите пароль"
              autoComplete="off"
            />
          </Form.Item>

          <Button
            type="primary"
            style={{ width: '100%', marginTop: '30px' }}
            onClick={login}
          >
            Войти
          </Button>
          
        </Form>
      </Card>
    </Layout>
);
};
export default LoginPage;
