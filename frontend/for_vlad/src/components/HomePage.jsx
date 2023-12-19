// src/components/MainPage.jsx
import React from 'react';
import {  Link } from 'react-router-dom';
import { Box, Button, Heading ,Center } from '@chakra-ui/react';


const HomePage = () => {

    return (
    <Center h="100vh"position="relative" >
      {/* <Image
        maxW="100%" // Ширина изображения, можете настроить по вашему усмотрению
        position="absolute"
        top="20%"
        left="50%"
        transform="translate(-50%, -50%)"
        zIndex="-1"

      /> */}

        <Box
          p={8}
          borderWidth="2px"
          borderRadius="md"
          boxShadow="lg"
          textAlign="center"
          borderColor='#00aeef'
        >
          <Heading as="h1" size="xl" mb={6}  fontFamily="Trebuchet MS">
            Добро пожаловать!
          </Heading>
          <Button colorScheme="twitter" variant="solid" size="lg" m="2" as={Link} to="/login">
            Вход
          </Button>
          <Button colorScheme="gray" variant="solid" size="lg" m="2" as={Link} to="/register">
          Регистрация
          </Button>
        </Box>
    </Center>
      );
    };
    
export default HomePage;
