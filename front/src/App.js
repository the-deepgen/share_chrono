import "./App.css";
import Navbar from "./components/Navbar/Navbar";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Home from "./Pages/Home/Home";
import Chrono from "./Pages/Chrono/Chrono";
import { useState, useContext } from "react";
import userAPI from "./services/userAPI";

// Contexts
import userInfosContext from "./Contexts/userInfos";

function App() {
  const [userName, setUserName] = useState(userAPI.getUsername());

  // CONTEXT CREATION User Infos
  const contextUserInfos = {
    userName: userName,
    setUserName: setUserName,
  };

  return (
    <userInfosContext.Provider value={contextUserInfos}>
      <Router>
        <div className="App">
          <Navbar />
          {!userName && <p>lol</p>}
        </div>

        <Switch>
          <Route path="/" exact render={(props) => <Home />} />
          <Route path="/chrono/:id" render={(props) => <Chrono />} />
        </Switch>
      </Router>
    </userInfosContext.Provider>
  );
}

export default App;
