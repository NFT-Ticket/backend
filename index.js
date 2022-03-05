// Use environment variables from .env file for Development (NOT used for Production)
if (process.env.NODE_ENV !== "production") {
	require("dotenv").config();
}
const express = require("express"),
	app = express(),
	mongoose = require("mongoose"),
	uri =
		"mongodb+srv://" +
		process.env.dbUser +
		":" +
		process.env.dbPass +
		"@" +
		process.env.dbHost +
		"/" +
		process.env.db +
		"?retryWrites=true&w=majority";

// Connecting to the database
mongoose
	.connect(uri, {
		useNewUrlParser: true,
		useUnifiedTopology: true,
	})
	.then(() => console.log("Connected to MongoDB Atlas!"))
	.catch((error) => console.error(error.message));

app.get("/", (req, res) => {
	res.send("<center><h1>The backend server is up and running!<h1><center>");
});

app.listen(process.env.PORT, () =>
	console.log(`Server listening at port ${process.env.PORT}!`)
);
