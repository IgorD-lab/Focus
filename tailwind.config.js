/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./website/templates/**/*.html", "./website/static/js/**/*.js"],
  theme: {
    extend: {
      backgroundColor: {
        "red-800": "#b91c1c",
      },
      colors: {
        secondary: "#your-color",
      },
    },
  },
  variants: {},
  plugins: [],
  mode: "jit",
};
