import React from "react";

export default React.createContext({
  userInfos: {
    userName: "",
  },
  setUserInfos: (value) => {},
});
