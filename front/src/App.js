import "./App.css";
import Navbar from "./components/Navbar/Navbar";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./Pages/Home/Home";
import Chrono from "./Pages/Chrono/Chrono";
import User from "./Pages/User/User";
import { useState, useContext } from "react";
import userAPI from "./services/userAPI";

// Contexts
import userInfosContext from "./Contexts/userInfos";
import modalContext from "./Contexts/modal";
import SimpleModal from "./components/Modal/Modal";

function App() {
  const [userName, setUserName] = useState(userAPI.getUsername());
  const [isDisplayed, setIsDisplayed] = useState(!!!userName);

  // CONTEXT CREATION User Infos
  const contextUserInfos = {
    userName: userName,
    setUserName: setUserName,
  };

  // CONTEXT CREATION Modal
  const contextModal = {
    isDisplayed: isDisplayed,
    setIsDisplayed: setIsDisplayed,
  };

  return (
    <userInfosContext.Provider value={contextUserInfos}>
      <modalContext.Provider value={contextModal}>
        <Router>
          <div className="App">
            <Navbar />
            {isDisplayed && <SimpleModal />}
          </div>

          <Switch>
            <Route
              path="/"
              exact
              render={({ match, history }) => (
                <Home match={match} history={history} />
              )}
            />
            <Route
              path="/chrono/:id"
              render={({ match, history }) => (
                <Chrono match={match} history={history} />
              )}
            />
            <Route path="/user" render={() => <User />} />
          </Switch>
        </Router>
      </modalContext.Provider>
    </userInfosContext.Provider>
  );
}

export default App;
