import React, { useEffect, useContext, useState } from "react";
import { Route, withRouter, Switch, Redirect } from "react-router-dom";
import LoginPage from "./components/SignupLogin/LoginPage";
import SignupPage from "./components/SignupLogin/SignupPage";
import LandingPage from "./components/Landing/LandingPage";
import ProfilePage from "./components/Profile/ProfilePage";
import MyFeedPage from "./components/Feeds/MyFeedPage";
import PublicFeedPage from "./components/Feeds/PublicFeedPage";
import CreatePostPage from "./components/Post/CreatePostPage";
import { Context } from "./Context";
import { getCurrentUserObject } from "./ApiUtils";
import {
  ROUTE_MY_FEED,
  ROUTE_PUBLIC_FEED,
  ROUTE_LOGIN,
  PAGE_MY_FEED,
  PAGE_PUBLIC_FEED,
  ROUTE_SIGNUP,
  PAGE_CREATE_POST,
} from "./Constants";
import "./App.scss";

const App = (props) => {
  const context = useContext(Context);

  const [shouldRedirect, updateShouldRedirect] = useState(false);

  // Protected React Routes
  // From StackOverflow https://stackoverflow.com/a/43171515
  // From Tyler McGinnis https://stackoverflow.com/users/1867084/tyler-mcginnis
  const PrivateRoute = ({
    component: Component,
    isAuthorized,
    subComponent: SubComponent,
    activeMenuItem,
    ...rest
  }) => {
    return (
      <Route
        {...rest}
        render={(props) =>
          isAuthorized ? (
            <Component
              {...props}
              subComponent={<SubComponent />}
              activeMenuItem={activeMenuItem}
            />
          ) : (
            <Redirect
              to={{
                pathname: { ROUTE_LOGIN },
                state: { from: props.location },
              }}
            />
          )
        }
      />
    );
  };

  const updateUserObject = async () => {
    const response = await getCurrentUserObject(context.cookie);

    if (response.status === 401) {
      context.deleteCookie();
      updateShouldRedirect(true);
      return;
    }

    if (response.data && response.data.username) {
      context.updateUser(response.data);
    }
  };

  useEffect(() => {
    updateUserObject();
  }, []);

  return (
    <div className="app">
      {shouldRedirect && <Redirect to={ROUTE_LOGIN} />}
      <Route exact path="/">
        {context.cookie ? (
          <Redirect to={ROUTE_MY_FEED} />
        ) : (
          <Redirect to={ROUTE_LOGIN} />
        )}
      </Route>

      <Switch key={props.location.key}>
        <Route path={ROUTE_LOGIN} component={LoginPage} />
        <Route path={ROUTE_SIGNUP} component={SignupPage} />
        <PrivateRoute
          isAuthorized={context.cookie}
          path={ROUTE_MY_FEED}
          component={LandingPage}
          subComponent={MyFeedPage}
          activeMenuItem={PAGE_MY_FEED}
        />
        <PrivateRoute
          isAuthorized={context.cookie}
          path={ROUTE_PUBLIC_FEED}
          component={LandingPage}
          subComponent={PublicFeedPage}
          activeMenuItem={PAGE_PUBLIC_FEED}
        />
        <PrivateRoute
          isAuthorized={context.cookie}
          path="/author/createpost"
          component={LandingPage}
          subComponent={CreatePostPage}
          activeMenuItem={PAGE_CREATE_POST}
        />
        <PrivateRoute
          isAuthorized={context.cookie}
          path="/author/:id"
          component={LandingPage}
          subComponent={ProfilePage}
        />
      </Switch>
    </div>
  );
};

export default withRouter(App);
