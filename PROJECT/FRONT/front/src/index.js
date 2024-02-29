import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import {RouterProvider, createBrowserRouter} from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Libros from './pages/Libros';

const router = createBrowserRouter([
  {path: '/', element: <App/>},
  {path: '/login', element: <Login/>},
  {path: '/register', element: <Register/>},
  {path: '/libros', element: <Libros/>}])

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router}/>
  </React.StrictMode>
);


