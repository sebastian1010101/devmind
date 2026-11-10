import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
  {
    // react-three-fiber's idiomatic pattern is to mutate scene objects
    // (camera, meshes, materials) imperatively inside useFrame — the
    // React Compiler's immutability rule doesn't recognize this escape
    // hatch and flags it as if it mutated a value during render.
    files: ["components/three/**/*.{ts,tsx}"],
    rules: {
      "react-hooks/immutability": "off",
    },
  },
]);

export default eslintConfig;
