module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"], // Purge unused styles in production
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {}, // Custom styles can be added here
  },
  variants: {
    extend: {},
  },
  plugins: [], // Tailwind plugins (if any)
};
