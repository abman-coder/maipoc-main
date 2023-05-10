let pathU = process.env.REACT_APP_API_PATH;
if (pathU) pathU = (pathU + "").trim()

const availablePaths = {
  "dev": "https://maipocaa.azurewebsites.net/api/",
  "local": "http://localhost:7071/api/",
}

export default {
  apiUrl: pathU || availablePaths["dev"],
  // apiUrl: "http://localhost:8000/",
  // apiUrl: "https://maipoctest.azurewebsites.net/",
};