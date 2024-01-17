// Header.jsx
import {Button,Menu, MenuItem, MenuButton, MenuList, Box, Flex, Text } from "@chakra-ui/react";
import {StarIcon} from "@chakra-ui/icons"
import { Link, useLocation } from "react-router-dom";


const Header = () => {
    const location = useLocation();
    const currentPath = location.pathname;

  // Проверьте, является ли текущий путь страницей авторизации
  const isAuthPage = ["/login", "/register", "/"].includes(currentPath);

  // Если это страница авторизации, не отображайте хедер
  if (isAuthPage) {
    return null;
  }

  return (
    <Flex p={4} bg="#B1B9FD" color="white" justify="space-between" align="center">
      <Text fontSize="xl">Логотип</Text>
      <Box borderRadius='lg'>
        

        <Menu>

            <Button variant='ghost' as={Link} to="/main" color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Главная</Button>


            <MenuButton variant='ghost' as={Button} color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Сравнение</MenuButton>
                <MenuList>
                    <MenuItem color="black" as={Link} to="/match2team" >Сравнение по группам</MenuItem>
                    <MenuItem color="black" as={Link} to="/match2team_vectorstudy" >Сравнение по направлениям</MenuItem>
                </MenuList>

            <Button variant='ghost' as={Link} to="/" color="white" _hover={{ color: "black" }} _active={{ bg: "transparent" }}>Выход</Button>

        </Menu>
      </Box>
    </Flex>
  );
};

export default Header;
