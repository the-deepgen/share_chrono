function getUsername() {
  const dataLocalStorage = localStorage.getItem("username");
  return dataLocalStorage || null;
}

function setUsername(userName) {
  const dataLocalStorage = localStorage.setItem("username", userName);
  return dataLocalStorage || null;
}

export default { getUsername, setUsername };
