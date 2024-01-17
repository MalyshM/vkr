// Ваш файл с настройками темы (например, theme.js)
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colorScheme: {
    customPurple: "#B1B9FD", // Замените "B1B9FD" на ваш цвет
  },
  styles: {
    global: {
      body: {
        bg: "#FFFFFF",
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
