// Ваш файл с настройками темы (например, theme.js)
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colorScheme: {
    customPurple: "#98d4e1", // Замените "B1B9FD" на ваш цвет
  },
  styles: {
    global: {
      body: {
        bg: "#F6F6F6",
        color: 'black',
      },
    },
  },

  components: {
    // Стили компонентов здесь
    Button: {
      baseStyle: {
        fontWeight: 'bold',
      },
    },
  },

  
  
});


export default theme;
