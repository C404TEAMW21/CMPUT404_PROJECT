import React, { useContext } from "react";
import { useHistory } from "react-router-dom";
import { Menu, Dropdown, Icon } from "semantic-ui-react";
import { Context } from "../../Context";
import { ReactComponent as AppLogo } from "../../assets/AppLogo.svg";
import {
  PAGE_MY_FEED,
  PAGE_PROFILE,
  PAGE_PUBLIC_FEED,
  ROUTE_LOGIN,
  PAGE_CREATE_POST,
} from "../../Constants";
import "./NavBar.scss";

const NavBar = (props) => {
  const context = useContext(Context);
  let history = useHistory();

  const handleClick = (e, { name }) => {
    props.renderPage(name);
  };

  const handleLogout = () => {
    context.updateUser(null);
    context.deleteCookie();
    history.push(ROUTE_LOGIN);
  };

  return (
    <div className="nav-bar">
      <Menu className="nav-bar-content" size="large" icon="labeled">
        <Menu.Item className="app-logo">
          <AppLogo />
        </Menu.Item>
        <Menu.Item
          className="menu-item"
          name={PAGE_MY_FEED}
          active={props.activeMenuItem === PAGE_MY_FEED}
          onClick={handleClick}
        >
          <Icon inverted name="newspaper outline" />
          My Feed
        </Menu.Item>
        <Menu.Item
          className="menu-item"
          name={PAGE_PUBLIC_FEED}
          active={props.activeMenuItem === PAGE_PUBLIC_FEED}
          onClick={handleClick}
        >
          <Icon inverted name="bullhorn" />
          Public Feed
        </Menu.Item>
        <Menu.Menu position="right">
          <Menu.Item
            className="menu-item"
            name={PAGE_CREATE_POST}
            active={props.activeMenuItem === PAGE_CREATE_POST}
            onClick={handleClick}
          >
            <Icon inverted name="edit outline" />
            Create Post
          </Menu.Item>
          <Dropdown
            className="menu-item"
            as="a"
            item
            icon={null}
            trigger={
              <>
                <Icon inverted name="user" />
                {context.user ? context.user.username : "loading..."}
              </>
            }
          >
            <Dropdown.Menu>
              <Dropdown.Item
                text="Profile"
                name={PAGE_PROFILE}
                onClick={handleClick}
              />
              <Dropdown.Item
                icon="sign-out"
                text="Logout"
                onClick={handleLogout}
              />
            </Dropdown.Menu>
          </Dropdown>
        </Menu.Menu>
      </Menu>
    </div>
  );
};

export default NavBar;
