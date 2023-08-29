import { useNavigate, NavLink } from 'react-router-dom';
import { storeAccessToken } from '../utils/AuthUtils';
import {baseUrl} from "../utils/ApiUtils";
import axios from 'axios';
import { useForm } from 'react-hook-form';

function Login() {
  const navigate = useNavigate();
  const {
    register,
    formState: { errors },
    handleSubmit,
    setError,
  } = useForm();

  function onSubmit(data) {
    axios
      .post(`${baseUrl}/auth/login`, data)
      .then(({ data: response }) => {
        storeAccessToken(response);
        navigate('/jobs');
      })
      .catch(() => {
        setError('password', {type: 'incorrect'});
      });
  }


  return (
    <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          <img
            className="mx-auto h-26 w-auto"
            src="/logo.svg"
            alt="Your Company"
          />
          <h2 className="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            <div>
              <label className="block text-sm font-medium leading-6 text-gray-900">
                Username
              </label>
              <div className="mt-2">
                <input
                  name="username"
                  placeholder="Enter your username"
                  {...register("username")}
                  required
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
                {errors.username && errors.username.type === 'required' &&
                  (<p>
                    Please enter your username
                  </p>)
                }
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="block text-sm font-medium leading-6 text-gray-900">
                  Password
                </label>
              </div>
              <div className="mt-2">
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  placeholder="Enter your password"
                  {...register("password")}
                  className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                />
                {errors.password && errors.password.type === 'required' && (
                  <p>
                    Please enter your password
                  </p>
                )}
                {errors.password && errors.password.type === 'minLength' && (
                  <p>
                    Please use at least 8 characters for your password
                  </p>
                )}
                {errors.password && errors.password.type === 'incorrect' && (
                  <p>
                    The username and password combination is incorrect
                  </p>
                )}
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Sign in
              </button>
            </div>
            <div className="text-center text-sm pt-2">
              <NavLink
                to="/register"
                className="text-sky-400 hover:text-sky-700"
              >Register</NavLink>
            </div>
          </form>
        </div>
      </div>
  );
}

export default Login;
