import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';

import {
  createBrowserRouter, Navigate,
  RouterProvider,
} from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Jobs from "./pages/Jobs";
import Job from "./pages/Job";
import {PrivateRoute, PublicOnlyRoute} from "./routes";
import {getAccessToken} from "./utils/AuthUtils";
import axios from "axios";
import {baseUrl} from "./utils/ApiUtils";
import JobCreate from "./pages/JobCreate";



const accessToken = getAccessToken();

window.axios = axios;

axios.defaults.baseURL = baseUrl;
axios.defaults.headers.common['Content-Type'] = 'application/json';
axios.defaults.headers.common['Accept'] = 'application/json';

if (accessToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <Navigate to={{pathname: "/jobs"}}/>
  },
  {
    path: "/login",
    element: <PublicOnlyRoute component={Login} />
  },
  {
    path: "/register",
    element: <PublicOnlyRoute component={Register} />
  },
  {
    path: "/jobs",
    element: <PrivateRoute component={Jobs} />
  },
  {
    path: "/jobs/create",
    element: <PrivateRoute component={JobCreate} />
  },
  {
    path: "/jobs/:id",
    element: <PrivateRoute component={Job} />
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <RouterProvider router={router} />
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
