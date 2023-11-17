/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./website/templates/**/*.html", "./website/static/js/**/*.js"],
  theme: {
    extend: {
      colors: {
        secondary: "#your-color",
      },
    },
  },
  variants: {},
  plugins: [],
  mode: "jit",
};
