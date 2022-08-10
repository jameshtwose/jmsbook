// api url
// const api_url = "https://2q6e55.deta.dev/all";
const api_url = "http://127.0.0.1:8000/";
const options = {
  method: 'GET',
  mode: "cors",
  // credentials: 'omit',
	headers: {
    "content-type": "application/json",
    "Access-Control-Allow-Origin": "*",
	}
};

fetch(api_url, options)
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("NETWORK RESPONSE ERROR");
    }
  })
  .then(data => {
    console.log(data);
    displayHome(data)
  })
  .catch((error) => console.error("FETCH ERROR:", error));

  function displayHome(data) {
    const home = data.message;
    const homeDiv = document.getElementById("home");    
    const heading = document.createElement("h2");
    heading.innerHTML = "Home message: " + home;
    homeDiv.appendChild(heading);
  }

const login_api_url = "http://127.0.0.1:8000/users";
const login_options = {
  method: 'POST',
  mode: "cors",
  // credentials: 'omit',
	headers: {
    "content-type": "application/json",
    "Access-Control-Allow-Origin": "*",
	},
    body: JSON.stringify({username: "jms3@gmail.com", password: "pass12345"})
};


fetch(login_api_url, login_options)
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("NETWORK RESPONSE ERROR");
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch((error) => console.error("FETCH ERROR:", error));

  function displayUsername(data) {
    const user = data.username;
    const userDiv = document.getElementById("user");    
    const heading = document.createElement("h4");
    heading.innerHTML = "Username: " + user;
    homeDiv.appendChild(heading);
  }

get_user_id_url = "http://127.0.0.1:8000/users/10"
const get_user_options = {
    method: 'GET',
    mode: "cors",
    // credentials: 'omit',
      headers: {
      "content-type": "application/json",
      "Access-Control-Allow-Origin": "*",
      }
  };
fetch(get_user_id_url, get_user_options)
  .then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("NETWORK RESPONSE ERROR");
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch((error) => console.error("FETCH ERROR:", error));