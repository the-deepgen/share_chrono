import React, { useContext } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Modal from "@material-ui/core/Modal";
import "./style.css";
import userInfosContext from "../../Contexts/userInfos";
import userAPI from "../../services/userAPI";
import ContainedButtons from "../Button/Button";
import TextField from "@material-ui/core/TextField";

function getModalStyle() {
  const top = 50;
  const left = 50;

  return {
    top: `${top}%`,
    left: `${left}%`,
    transform: `translate(-${top}%, -${left}%)`,
  };
}

const useStyles = makeStyles((theme) => ({
  paper: {
    position: "absolute",
    width: 400,
    backgroundColor: theme.palette.background.paper,
    border: "2px solid #000",
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3),
    borderRadius: "6px",
  },
}));

export default function SimpleModal() {
  const { userName, setUserName } = useContext(userInfosContext);

  const classes = useStyles();
  // getModalStyle is not a pure function, we roll the style only on the first render
  const [modalStyle] = React.useState(getModalStyle);
  const [open, setOpen] = React.useState(true);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    if (userName) {
      setOpen(false);
    } else {
      return;
    }
  };

  const saveUserName = (userName) => {
    userAPI.setUsername(userName);
    setUserName(userName);
  };

  return (
    <div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="simple-modal-title"
        aria-describedby="simple-modal-description"
      >
        <div style={modalStyle} className={classes.paper}>
          <h2 id="simple-modal-title">Merci d'indiquer votre nom</h2>
          <p id="simple-modal-description">
            <TextField
              id="outlined-basic"
              label="Votre nom"
              variant="outlined"
              onChange={(e) => saveUserName(e.target.value)}
              value={userName}
              fullWidth
            />
          </p>
          <div className="buttonContainer">
            <ContainedButtons
              text="OK"
              disabled={!userName}
              onClick={handleClose}
            />
          </div>
        </div>
      </Modal>
    </div>
  );
}
