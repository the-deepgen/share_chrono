import "./App.css";
import Navbar from "./components/Navbar";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
      </div>

      <Switch>
        <Route path="/a" exact render={(props) => <p>Test</p>} />
      </Switch>
    </Router>
  );
}

export default App;
