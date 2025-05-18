import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})

// import { defineConfig } from 'vite'
// import react from '@vitejs/plugin-react-swc'
// // // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
//   base: '/assets/',
//   build: {
//     assetsDir: '',
//   },
//   define: {
//     // This ensures process.env.NODE_ENV is available in the browser
//     'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
//   }
// })
