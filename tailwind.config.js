/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  mode: "jit",
  content: ["./web/templates/**/*.{html,js}", "./web/static/js/*.js"],
  theme: {
    extend: {
      colors: {
        primary: {
          100: "#F7B472",
          200: "#F6AD64",
          300: "#F5A556",
          400: "#F49E48",
          500: "#F3953A",
          600: "#F28C25",
          700: "#F18111",
          800: "#DF760D",
          900: "#CB6B0C",
        },
        primary_light: "#FCECDD",
        secondary: "#FFF2CC",
      },
      fontFamily: {
        sans: ["'Libre Franklin'", ...defaultTheme.fontFamily.sans],
      },
      backgroundImage: {
        "hero-image": "url('/static/images/landing.jpg')",
        "our-rescue-1": "url('/static/images/our_rescue_1.png')",
        "our-rescue-2": "url('/static/images/our_rescue_2.png')",
        "our-rescue-3": "url('/static/images/our_rescue_3.png')",
        "ways-to-make-better": "url('/static/images/ways_to_make_better.png')",
      },
    },
  },
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["light"],
          primary: "#F3953A",
          secondary: "#FCEBDD",
        },
      },
    ],
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("daisyui"),
  ],
};
