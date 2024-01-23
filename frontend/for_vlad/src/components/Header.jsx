// Header.jsx
import {Button,Menu, MenuItem, MenuButton, MenuList, Box, Flex, Text } from "@chakra-ui/react";
import {StarIcon} from "@chakra-ui/icons"
import { Link, useLocation } from "react-router-dom";
import React, { useEffect, useState } from 'react';


const Header = () => {
    const location = useLocation();
    const currentPath = location.pathname;
    const [currentDate, setCurrentDate] = useState(new Date());

    useEffect(() => {
      // Обновляем текущую дату каждый час
      const intervalId = setInterval(() => {
        setCurrentDate(new Date());
      }, 3600000); // 1 час в миллисекундах
  
      // Очищаем интервал при размонтировании компонента
      return () => clearInterval(intervalId);
    }, []);

    const formatDate = (date) => {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return date.toLocaleDateString('ru-RU', options);
    };


  // Проверьте, является ли текущий путь страницей авторизации
  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  // Если это страница авторизации, не отображайте хедер
  if (isAuthPage) {
    return null;
  }

  return (
    <Flex h={90} p={4}
    // backgroundImage="linear-gradient(to right, #6260DB, #4CAF50)" 
    bg="#56adc0" color="white" justify="space-between" align="center">
      <Text fontSize='sm' as='b' ml={5} mr={'auto'} >Данные актуальны на {formatDate(currentDate)} </Text>
      <Box borderRadius='lg'>
        <Menu>
            <Button variant='ghost' as={Link} to="/main" color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Главная</Button>
            <Button variant='ghost' as={Link} to="/analys_kr" color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Анализ КР</Button>
            <MenuButton variant='ghost' as={Button} color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Группы/Направления</MenuButton>
                <MenuList>
                    <MenuItem color="black" as={Link} to="/your_group" >Ваши группы</MenuItem>
                    <MenuItem color="black" as={Link} to="/match2team" >Сравнение по группам</MenuItem>
                    <MenuItem color="black" as={Link} to="/your_vectorstudy" >Ваши направления</MenuItem>
                    <MenuItem color="black" as={Link} to="/match2team_vectorstudy" >Сравнение по направлениям</MenuItem>
                </MenuList>

            <Button variant='ghost' as={Link} to="/" color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Выход</Button>

        </Menu>
      </Box>
    </Flex>
  );
};

export default Header;
