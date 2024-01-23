import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './useAuth';
import { Box, Heading, FormControl, FormLabel, Input, Button,Center} from '@chakra-ui/react';
import { useToast } from '@chakra-ui/react';
import { Flex, Spacer } from '@chakra-ui/react'
import { CloseIcon } from '@chakra-ui/icons'


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
  <Center bg="#72b5bb" h="100vh">
    <Box
      // maxW="md"
      // height='500px'
      width='500px'
      borderWidth="2px"
      borderRadius="lg"
      p={6}
      // m="auto"
      // mt={40}
      boxShadow="base"
      borderColor='#1A1A1A'
      bg='white'
    >
      <Flex justify="space-between" >
        <Center>
          <Heading as="h2" size="lg" mb={6}>Вход</Heading>
        </Center>
        <Spacer/>
        <Button ml={5} colorScheme="gray" as={Link} to="/"> <CloseIcon/> </Button>
      </Flex>
      

      
      
      
    <FormControl  id="FIO" mb={4}>
      <FormLabel>ФИО:</FormLabel>
      <Input
        type="text"
        value={FIO}
        onChange={handleInputChangeFIO}
        onBlur={handleBlurFIO}
        required
        borderColor={isFIOEmpty ? "red.500" : (isFIOPopulated ? "green.500" : "gray.200")}
        placeholder='Введите ваше ФИО'
        autoComplete="off"
      />
      {isFIOEmpty && (
        <Box color="red.500" fontSize="sm" mt={1}>
          Поле не может быть пустым.
        </Box>
      )}
      
    </FormControl>

      <form autoComplete="off">
      <FormControl  id="username" mb={4}>
        <FormLabel>Логин:</FormLabel>
        <Input
          type="text"
          value={username}
          onChange={handleInputChangeUsername}
          onBlur={handleBlurUsername}
          required
          autoComplete="off"
          placeholder='Введите ваш логин'
          borderColor={isUsernameEmpty ? "red.500" : (isUsernamePopulated ? "green.500" : "gray.200")}
        />
        {isUsernameEmpty && (
        <Box color="red.500" fontSize="sm" mt={1}>
          Поле не может быть пустым.
        </Box>
      )}
      </FormControl>
      </form>

      <form autoComplete="off">
      <FormControl  id="email" mb={4}>
        <FormLabel>Адрес электронной почты:</FormLabel>
        <Input
          type="text"
          value={email}
          onChange={handleInputChangeEmail}
          onBlur={handleBlurEmail}
          required
          autoComplete="off"
          placeholder='Введите вашу электронную почту '
          borderColor={isEmailEmpty ? "red.500" : (isEmailPopulated ? "green.500" : "gray.200")}
        />
        {isEmailEmpty && (
        <Box color="red.500" fontSize="sm" mt={1}>
          Поле не может быть пустым.
        </Box>
      )}
      </FormControl>
      </form>

      <form autoComplete="off">
      <FormControl  id="password" mb={4}>
        <FormLabel>Пароль:</FormLabel>
        <Input
          type="password"
          value={password}
          onChange={handleInputChangePas}
          onBlur={handleBlurPas}
          required
          autoComplete="off"
          placeholder='Введите пароль'
          borderColor={isPasswordEmpty ? "red.500" : (isPasswordPopulated ? "green.500" : "gray.200")}

        />
        {isPasswordEmpty && (
        <Box color="red.500" fontSize="sm" mt={1}>
          Поле не может быть пустым.
        </Box>
      )}
      </FormControl>
      </form>

      <Button mt='30px' w='450px' colorScheme="teal" onClick={login}>
        Войти
      </Button>
      
      
    </Box>
    </Center>
);
};
export default LoginPage;
