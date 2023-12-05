/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./website/templates/**/*.html", "./website/static/js/**/*.js"],
  theme: {
    extend: {
      backgroundColor: {
        "red-800": "#b91c1c",
      },
      colors: {
        // DARK blue
        backgroundD: "#222831",
        secondaryD: "#222831",
        accentD: "#393E46",
        primaryD: "#00ADB5",
        textD: "#EEEEEE",
        hoverButtonD: "#45b4c8",
        // backgroundD: "#04181b",
        // textD: "#dbf7fa",
        // primaryD: "#64dbe8",
        // secondaryD: "#04181b",
        // accentD: "#1ebbcc",
        // hoverButtonD: "#45b4c8",
        // LIGHT blue
        backgroundL: "#e4f8fb",
        textL: "#052124",
        primaryL: "#178e9b",
        secondaryL: "#e4f8fb",
        accentL: "#33cfe1",
        hoverButtonL: "#17c6c6",
      },
    },
  },
  variants: {},
  plugins: [
    function ({ addUtilities }) {
      const newUtilities = {
        ".custom-blur": {
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.25)",
          filter: "blur(8px)",
          backgroundColor: "rgba(255, 255, 255, 0.5)",
        },
      };
      addUtilities(newUtilities);
    },
  ],
  mode: "jit",
};
