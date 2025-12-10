// eslint.config.js
export default [
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: {
          jsx: true, // habilita JSX
        },
      },
      globals: {
        React: "readonly", // evita erro de React não definido
      },
    },
    plugins: {
      react: await import("eslint-plugin-react"),
      "react-hooks": await import("eslint-plugin-react-hooks"),
    },
    rules: {
      "react/react-in-jsx-scope": "off",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
    settings: {
      react: { version: "detect" },
    },
  },
];
