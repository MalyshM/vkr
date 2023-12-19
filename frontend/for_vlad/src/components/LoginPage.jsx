import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './useAuth';
import { Box, Heading, FormControl, FormLabel, Input, Button,} from '@chakra-ui/react';
import { useToast } from '@chakra-ui/react';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [FIO, setFIO] = useState('');
  const [email, setEmail] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const navigate = useNavigate();
  const { setUserToken } = useAuth();

  const toast = useToast();


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
      const response = await fetch('http://localhost:8090/api/login_standard', {
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
  <Box
    maxW="md"
    borderWidth="2px"
    borderRadius="lg"
    p={6}
    m="auto"
    mt={10}
    boxShadow="base"
    borderColor='#00aeef'
  >
    <Heading as="h2" size="lg" mb={6}>
      Вход
      
    </Heading>
    
    <FormControl isRequired id="FIO" mb={4}>
      <FormLabel>ФИО:</FormLabel>
      <Input
        type="text"
        value={FIO}
        onChange={(e) => setFIO(e.target.value)}
        required
      />
    </FormControl>
    <FormControl isRequired id="username" mb={4}>
      <FormLabel>Логин:</FormLabel>
      <Input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
    </FormControl>
    <FormControl isRequired id="email" mb={4}>
      <FormLabel>Адрес электронной почты:</FormLabel>
      <Input
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
    </FormControl>
    <FormControl isRequired id="password" mb={4}>
      <FormLabel>Пароль:</FormLabel>
      <Input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
    </FormControl>
    <Button colorScheme="twitter" onClick={login}>
      Войти
    </Button>
    <Button ml={5} colorScheme="gray" as={Link} to="/">
      Вернуться назад
    </Button>
    
  </Box>
);
};
export default LoginPage;
