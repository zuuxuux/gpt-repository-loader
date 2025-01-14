# Noovox Frontend
Uses vanilla javascript and html at the moment

## created using:
1. npm create vite@latest . -- --template react-ts
2. npm install
3. npm install -D tailwindcss postcss autoprefixer
4. npx tailwindcss init -p
5. npm install @radix-ui/react-icons
6. npm install -g shadcn-ui
7. npx shadcn@latest init


## Dev requirements
1. Install npm:
    - `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash`
    - `nvm install stable`
    - `nvm use stable`
2. Install dependencies:
    - navigate to this directory
    - `npm install`
3. Create .env file:
    - copy `.env.local.example` -> `.env.local`
3. Run a dev version of the app:
    - `npm run dev`
  
## Setup for testing:
Run `npx playwright install` to install browser binaries, and `sudo apt-get install libevent-2.1-7t64 libavif16` for dependencies

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```
