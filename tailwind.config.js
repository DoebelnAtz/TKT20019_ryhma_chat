const plugin = require("tailwindcss/plugin");
/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
        "./app/templates/**/*.html",
        "./app/static/**/*.{js,css}"
        ],  
        darkMode: "selector",
  plugins: [
    plugin(function ({ addBase, theme }) {
      addBase({
        ".text-head-0": {
          fontWeight: theme("fontWeight.medium"),
          fontSize: theme("fontSize.2xl"),
          lineHeight: theme("lineHeight.7"),
        },
        ".text-head-1": {
          fontWeight: theme("fontWeight.semibold"),
          fontSize: theme("fontSize.xl"),
          lineHeight: theme("lineHeight.6"),
          letterSpacing: theme("letterSpacing.tight"),
        },
        ".text-head-2": {
          fontWeight: theme("fontWeight.medium"),
          fontSize: theme("fontSize.base"),
          lineHeight: theme("lineHeight.5"),
          letterSpacing: theme("letterSpacing.tight"),
        },
        ".text-head-3": {
          fontWeight: theme("fontWeight.semibold"),
          fontSize: theme("fontSize.base"),
          lineHeight: theme("lineHeight.4"),
        },
        ".text-elem-1": {
          fontWeight: theme("fontWeight.light"),
          fontSize: theme("fontSize.16px"),
          lineHeight: theme("lineHeight.5_5"),
        },
        ".text-elem-2": {
          fontWeight: theme("fontWeight.medium"),
          fontSize: theme("fontSize.sm"),
          lineHeight: theme("lineHeight.4"),
        },
        ".text-elem-3": {
          fontWeight: theme("fontWeight.normal"),
          fontSize: theme("fontSize.sm"),
          lineHeight: theme("lineHeight.4"),
        },

        ".text-body": {
          fontWeight: theme("fontWeight.medium"),
          fontSize: theme("fontSize.sm"),
          lineHeight: theme("lineHeight.4_5"),
          letterSpacing: theme("letterSpacing.tight-sm"),
        },
        ".text-body-bold": {
          fontWeight: theme("fontWeight.bold"),
          fontSize: theme("fontSize.sm"),
          lineHeight: theme("lineHeight.4_5"),
          letterSpacing: theme("letterSpacing.tight-sm"),
        },
      });
    }),
  ],
  theme: {
    fontFamily: {
      sans: ["Inter", "Outfit", "sans-serif"],
      system: [
        "ui-sans-serif",
        "-apple-system",
        "BlinkMacSystemFont",
        '"Segoe UI"',
        "Helvetica",
        '"Apple Color Emoji"',
        "Arial",
        "sans-serif",
        '"Segoe UI Emoji"',
        '"Segoe UI Symbol"',
      ],
    },
    container: {
      center: true,
    },
    colors: {
      white: "var(--white)",
      fg1: "var(--fg1)",
      fg2: "var(--fg2)",
      fg3: "var(--fg3)",
      fg4: "var(--fg4)",
      fg5: "var(--fg5)",
      fg6: "var(--fg6)",
      fg7: "var(--fg7)",
      fg8: "var(--fg8)",
      fg9: "var(--fg9)",
      
      bg1: "var(--bg1)",
      bg2: "var(--bg2)",
      bg3: "var(--bg3)",
      bg4: "var(--bg4)",
      bg5: "var(--bg5)",
      bg6: "var(--bg6)",
      bg7: "var(--bg7)",
      bg8: "var(--bg8)",
      bg9: "var(--bg9)",

      primary1: "var(--primary1)",
      primary2: "var(--primary2)",
      primary3: "var(--primary3)",
      primary4: "var(--primary4)",
      primary5: "var(--primary5)",
      primary6: "var(--primary6)",
      primary7: "var(--primary7)",
      primary8: "var(--primary8)",
      primary9: "var(--primary9)",

      secondary1: "var(--secondary1)",
      secondary2: "var(--secondary2)",
      secondary3: "var(--secondary3)",
      secondary4: "var(--secondary4)",
      secondary5: "var(--secondary5)",
      secondary6: "var(--secondary6)",
      secondary7: "var(--secondary7)",
      secondary8: "var(--secondary8)",
      secondary9: "var(--secondary9)",
      transparent: "transparent",
    },
    letterSpacing: {
      wide: "0.0125rem",
      "tight-2xs": "-0.00625rem",
      "tight-xs": "-0.0075rem",
      "tight-sm": "-0.00875rem",
      tight: "-0.0125rem",
      tighter: "-0.03rem",
      tightest: "-0.03375rem",
    },
    extend: {
      borderWidth: {
        0.25: "0.25px",
        0.5: "0.5px",
        0.75: "0.75px",
      },
      animation: {
        "spin-slow": "spin 3s linear infinite",
      },
      borderRadius: {
        "4xl": "2rem",
      },
      maxWidth: {
        "2xs": "10rem",
      },
      fontSize: {
        "base-lg": "1.0625rem",
        "13px": "0.8125rem",
        "2xs": "0.625rem",
      },
      lineHeight: {
        "4_75": "1.1875rem",
        "4_5": "1.125rem",
        "3_75": "0.9375rem",
        "3_5": "0.875rem",
        "2_5": "0.625rem",
      },
      width: {
        "3/2": "150%",
        "2/1": "200%",
      },
      height: {
        "3/2": "150%",
        "2/1": "200%",
      },
    },
  },
  }