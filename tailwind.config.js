/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  mode: "jit",
  content: ["./web/templates/**/*.{html,js}", "./web/static/js/*.js"],
  theme: {
    extend: {
      colors: {
        primary: {
          100: "#EA6106",
          200: "#D05605",
          300: "#B64C05",
          400: "#9C4104",
          500: "#823603",
          600: "#783203",
          700: "#6F2E03",
          800: "#662A03",
          900: "#5C2602",
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
          primary: "#b45309",
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
