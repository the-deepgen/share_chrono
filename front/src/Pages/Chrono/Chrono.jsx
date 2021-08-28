import "./style.css";
import { io } from "socket.io-client";

const Chrono = () => {
  const socket = io("/test_connect");

  return <div className="container marginTop20px">Chrono</div>;
};

export default Chrono;
