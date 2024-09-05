const darkButton = document.getElementById("dark_mode-button");
const whiteButton = document.getElementById("white_mode-button");
const root = document.documentElement;
const messagesContainer = document.getElementById("messages-container");

change_var = false;


const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};




darkButton.addEventListener('click', () => {

  root.style.setProperty('--body-background-color', '#bbc8dc');
  root.style.setProperty('--main-background-color', '#376b6c');
  root.style.setProperty('--main-color', '#bbc8dc');
  root.style.setProperty('--border-color', 'white');
});

whiteButton.addEventListener('click', () => {

  root.style.setProperty('--body-background-color', '#f5f6f8');
  root.style.setProperty('--main-background-color', '#ffffff');
  root.style.setProperty('--main-color', '#2a303b');
  root.style.setProperty('--border-color', 'black');
});

