import "./style.css";
import ContainedButtons from "../../components/Button/Button";

const Home = () => {
  return (
    <div className="container marginTop20px">
      <main className="main">
        <div className="imageContainer">
          <img src="chrono.svg" />
        </div>
        <div className="buttonContainer">
          <ContainedButtons
            text="Créer un chrono"
            onClick={(e) => console.log(e)}
            size="large"
          />
        </div>
      </main>
    </div>
  );
};

export default Home;
