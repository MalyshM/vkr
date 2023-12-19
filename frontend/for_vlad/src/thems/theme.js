// Ваш файл с настройками темы (например, theme.js)
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  styles: {
    global: {
      body: {
        // bg: ' linear-gradient(to right, #00d2ff, #3a7bd5) ',
        bg: "#c2cbd6",
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
