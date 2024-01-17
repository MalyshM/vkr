// src/components/MainPage.jsx
import React from 'react';
import {  Link } from 'react-router-dom';
import { Box, Button, Heading ,Center,} from '@chakra-ui/react';

const HomePage = () => {

    return (
    <Center bg='#B1B9FD' h="100vh"position="relative" >
      

        <Box
          p={8}
          borderWidth="2px"
          borderRadius="2xl"
          boxShadow="lg"
          textAlign="center"
          borderColor='#1A1A1A'
          height="300px"
          width="500px"
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          bg='white'

        >

          <Heading as="h1" size="xl" mb={6}  fontFamily="Trebuchet MS">
            Добро пожаловать!
          </Heading>
          <Button w='200px' colorScheme="yellow" variant="solid" size="lg" m="2" as={Link} to="/login">
            Войти
          </Button>
          <Button  colorScheme="purple" variant='solid' size="lg" m="2" as={Link} to="/register">
          Создать аккаунт
          </Button>
        </Box>
        
    </Center>
      );
    };
    
export default HomePage;
