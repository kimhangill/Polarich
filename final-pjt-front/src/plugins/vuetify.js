import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";
import { createVuetify } from "vuetify";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { ko } from 'vuetify/locale';
import { ko as dateKo } from 'date-fns/locale';

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: {
      mdi,
    },
  },
    
  locale: {
    locale: 'ko',
    messages: { ko },
  },
  date: {
    locale: dateKo,
  },
  
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#1976D2",
          secondary: "#424242",
          accent: "#82B1FF",
          error: "#FF5252",
          info: "#2196F3",
          success: "#4CAF50",
          warning: "#FFC107",
        },
      },
    },
    typography: {
      fontFamily: "Roboto, sans-serif",
    },
  },
});
