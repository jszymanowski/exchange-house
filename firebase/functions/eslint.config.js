// eslint.config.js
import eslintPluginImport from "eslint-plugin-import";
import eslintPluginTs from "@typescript-eslint/eslint-plugin";
import parserTs from "@typescript-eslint/parser";

export default [
  {
    ignores: ["/lib/**/*", "/generated/**/*"],
  },
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      ecmaVersion: 2015,
      sourceType: "module",
      parser: parserTs,
      parserOptions: {
        project: ["tsconfig.json", "tsconfig.dev.json"],
      },
    },
    plugins: {
      "@typescript-eslint": eslintPluginTs,
      import: eslintPluginImport,
    },
    rules: {
      quotes: ["error", "double"],
      "import/no-unresolved": "off",
      indent: ["error", 2],
      "max-len": ["error", { code: 120 }],
      ...eslintPluginTs.configs.recommended.rules,
      ...eslintPluginImport.configs.errors.rules,
      ...eslintPluginImport.configs.warnings.rules,
      ...(eslintPluginImport.configs.typescript?.rules || {}),
    },
    settings: {
      "import/resolver": {
        typescript: {
          alwaysTryTypes: true,
          project: "./tsconfig.json",
        },
      },
    },
  },
];
