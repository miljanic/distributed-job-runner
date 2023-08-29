import React from 'react';
import { Navigate } from 'react-router-dom';
import PropTypes from 'prop-types';

import { isAuthenticated } from './utils/AuthUtils';
import Header from "./components/Header";

// eslint-disable-next-line

export function PublicOnlyRoute({ component: Component, ...rest }) {
  const authenticated = isAuthenticated();

  return (
    !authenticated ? <Component {...rest} /> : <Navigate to={{pathname: "/jobs"}} />
  );
}

PublicOnlyRoute.propTypes = {
    component: PropTypes.func
};


export function PrivateRoute({ component: Component, ...rest }) {
  const authenticated = isAuthenticated();

  return (
    authenticated ? <Header><Component {...rest} /></Header> : <Navigate
      to={{
        pathname: '/login',
      }}
    />
  );
}

PrivateRoute.propTypes = {
    component: PropTypes.func
};
