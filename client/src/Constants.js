// export const SERVER_HOST = "http://127.0.0.1:8000";
export const SERVER_HOST =
  process.env.NODE_ENV === "production"
    ? "https://konnection-server.herokuapp.com"
    : "http://127.0.0.1:8000";

export const ROUTE_LOGIN = "/login";
export const ROUTE_SIGNUP = "/signup";
export const ROUTE_MY_FEED = "/myfeed";
export const ROUTE_PUBLIC_FEED = "/publicfeed";

export const PAGE_MY_FEED = "MyFeed";
export const PAGE_PUBLIC_FEED = "PublicFeed";
export const PAGE_CREATE_POST = "CreatePost";
export const PAGE_PROFILE = "Profile";

export const FOLLOWER_LIST = "FollowerList";
export const FRIEND_LIST = "FriendList";
export const FRIEND_REQUEST_LIST = "FriendRequestList";

export const MARKDOWN_TYPE = "text/markdown";
export const PLAINTEXT_TYPE = "text/plain";
