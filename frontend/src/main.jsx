import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { createBrowserRouter, Router, RouterProvider } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Home from './pages/Home.jsx'
import Register from './pages/Register'
const route  = createBrowserRouter([
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/register',
    element: <Register />
  }
])
createRoot(document.getElementById('root')).render(
  <RouterProvider router={route} />
)
