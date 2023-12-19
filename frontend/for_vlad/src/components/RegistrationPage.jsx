 // useEffect(() => {
  //   // Проверяем, есть ли токен при загрузке компонента
  //   const storedToken = localStorage.getItem('token');
  //   if (storedToken) {
  //     setToken(storedToken);
  //   }
  //   }, [] );

    // if (!username || !password || !confirmPassword) {
    //   setError('All fields are required');
    //   return;
    // }

    // if (password !== confirmPassword) { //на потом
    //   setError('Passwords do not match');
    //   return;
    // }

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';
import { useAuth } from './useAuth';
import { Box, Heading, FormControl, FormLabel, Input, Button, Radio, RadioGroup } from '@chakra-ui/react';
import { useToast } from '@chakra-ui/react';


const RegistrationPage = () => {
  // Состояния для отслеживания значений полей ввода и сообщений об ответе
  const [FIO, setFIO] = useState('');
  const [role, setRole] = useState(''); // Состояние для хранения выбранной роли

  const [isAdmin, setIsAdmin] = useState(false);
  const [isCurator, setIsCurator] = useState(false);
  const [isTeacher, setIsTeacher] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const navigate = useNavigate();
  const { setUserToken } = useAuth(); 
  const toast = useToast();

  const handleRoleChange = (selectedRole) => {
    setRole(selectedRole);

    // Сбросить все состояния ролей
    setIsAdmin(false);
    setIsCurator(false);
    setIsTeacher(false);

    // Установить состояние для выбранной роли
    if (selectedRole === 'admin') {
      setIsAdmin(true);
    } else if (selectedRole === 'curator') {
      setIsCurator(true);
    } else if (selectedRole === 'teacher') {
      setIsTeacher(true);
    }
  };



const register = async () => {

  if (!username || !password || !FIO || !email || !role) {
    toast({
      title: 'Ошибка',
      description: 'Пожалуйста, заполните все поля!',
      status: 'error',
      duration: 3000, // Продолжительность отображения в миллисекундах
      isClosable: true,
    });
    return;
  }
    // Функция для выполнения регистрации по отправке запроса к API
    try {
      // Отправка POST-запроса к API для регистрации
      const response = await fetch('http://localhost:8090/api/registration_standard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({

          FIO,
          isAdmin,
          isCurator,
          isTeacher,
          username,
          password,
          email,
        }),
      });

      // Обработка ответа от сервера
      const result = await response.json();

      // Если ответ от сервера успешный, обновление сообщения об ответе
      if (response.ok) {
        setUserToken(result.access_token); // Обновляем токен в AuthContext
        setResponseMessage(`Registration successful! Welcome, ${username}!, Access Token: ${result.access_token}`);
        navigate('/main');
      } else {
        // Если регистрация не удалась, обновление сообщения об ответе
        setResponseMessage(`Registration failed: ${result.detail}`);
      }
    } catch (error) {
      // Обработка ошибок в случае неудачной отправки запроса
      console.error('Error during registration:', error);
      setResponseMessage('An error occurred during registration.');
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
      Регистрация
    </Heading>
    
    <FormControl isRequired id="role" mb={4}>

        <FormLabel>Роль:</FormLabel>

        <RadioGroup onChange={(value) => handleRoleChange(value)} value={role} checked={'red'} >

          <Radio colorScheme='red'  mr={5} value="admin">Админ</Radio>
          <Radio colorScheme='red'  mr={5} value="teacher">Преподаватель</Radio>
          <Radio colorScheme='red' value="curator">Куратор</Radio>

        </RadioGroup>

    </FormControl>

    <FormControl isRequired id="FIO" mb={4}>
      <FormLabel >ФИО:</FormLabel>
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
    </FormControl >
    <FormControl isRequired id="password" mb={4}>
      <FormLabel>Пароль:</FormLabel>
      <Input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
    </FormControl>
    <FormControl isRequired id="email" mb={4}>
      <FormLabel>Адрес электронной почты:</FormLabel>
      <Input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
    </FormControl>
    <Button  colorScheme="twitter" onClick={register}>
      Подтвердить
    </Button>
    <Button ml={5} colorScheme="gray" as={Link} to="/">
      Вернуться назад
    </Button>
    <p id="responseMessage">{responseMessage}</p>
  </Box>
);
};

export default RegistrationPage;
