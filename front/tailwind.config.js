module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#8F8F8F',
          hover: '#717171', // Adjusted to a valid hex color
          dark: '#707070',
        },
        secondary: {
          DEFAULT: '#FFFFFF',
          hover: '#FFFFFFC2', // Adjusted to a valid hex color with opacity
          dark: '#000000',
        },
        accent: {
          DEFAULT: '#D33131',
          hover: '#D33131A3', // Adjusted to a valid hex color with opacity
          dark: '#D33131',
        },
        text: {
          DEFAULT: '#000000',
          dark: '#ECF3ED',
        },
        bgCustom: {
          DEFAULT: '#FFFFFF',
          dark: '#000000',
        },
      },
    },
  },
  plugins: [],
}
