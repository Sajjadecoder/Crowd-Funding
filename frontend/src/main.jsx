import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import { createBrowserRouter, Router, RouterProvider } from 'react-router-dom'
import Login from './pages/Login.jsx'
import Home from './pages/Home.jsx'
import Register from './pages/Register'
import CampaignCard from './components/CampaignCard'
import AllCampaigns from './pages/AllCampaigns'
import CampaignDetails from './pages/CampaignDetails'
const route  = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    path: '/register',
    element: <Register />
  },
  {
    path: '/all-campaigns',
    element: <AllCampaigns />
  },
  {
    path: '/all-campaigns/:id',
    element: <CampaignDetails />
  },
  {
    path: '/all-campaigns',
    element: <AllCampaigns />
  }
])
createRoot(document.getElementById('root')).render(
  <RouterProvider router={route} />
)
