import { ChakraProvider, ColorModeScript } from '@chakra-ui/react'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
<<<<<<< HEAD
import theme from './components/theme'


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <ColorModeScript  initialColorMode={theme.config.initialColorMode}/>
=======
import './index.css'
import { BrowserRouter } from 'react-router-dom'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <BrowserRouter>
  
    <ChakraProvider>
>>>>>>> 6acb0b2e2e708f4dee60172bf28ed2224f88798d
    <App />
    </ChakraProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
