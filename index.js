const express = require("express");
const app = express();
const PORT = 8080; //TODO: Define using environment variables

app.get("/", (req, res) => {
	res.send("<center><h1>The backend server is up and running!<h1><center>");
});

app.listen(PORT, () => console.log(`Server listening at port ${PORT}`));
