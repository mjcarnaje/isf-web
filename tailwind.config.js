/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  mode: "jit",
  content: ["./web/templates/**/*.{html,js}", "./web/static/js/*.js"],
  theme: {
    extend: {
      colors: {
        primary: "#642902",
      },
      fontFamily: {
        sans: ["'Libre Franklin'", ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
