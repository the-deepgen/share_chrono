import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import "./style.css";
import { Link } from "react-router-dom";
import userInfosContext from "../../Contexts/userInfos";
import { useContext } from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {},
}));

export default function Navbar() {
  const classes = useStyles();

  const { userName } = useContext(userInfosContext);

  return (
    <div className={classes.root}>
      <AppBar position="static" color="transparent">
        <Toolbar className="toolbarContainer">
          <Link to="/">
            <img src="2.png" className="logo_team_swan" />
          </Link>
          {/* <IconButton
            edge="start"
            className={classes.menuButton}
            color="inherit"
            aria-label="menu"
          >
            <MenuIcon />
          </IconButton> */}
          <Link to="/">
            <Typography variant="h5" className={classes.title}>
              Share Chrono
            </Typography>
          </Link>
          <Typography variant="h6" className={classes.title}>
            <Link to="/user">{userName}</Link>
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
  );
}
