import userInfosContext from "../../Contexts/userInfos";
import { useContext } from "react";
import userAPI from "../../services/userAPI";
import TextField from "@material-ui/core/TextField";

const User = () => {
  const { userName, setUserName } = useContext(userInfosContext);

  const handleChange = (e) => {
    userAPI.setUsername(e.target.value);
    setUserName(e.target.value);
  };

  return (
    <div className="container marginTop20px">
      Modifier mon nom d'utilisateur
      <p>
        <TextField
          id="outlined-basic"
          label="Votre nom"
          variant="outlined"
          onChange={(e) => handleChange(e)}
          value={userName}
        />
      </p>
    </div>
  );
};

export default User;
