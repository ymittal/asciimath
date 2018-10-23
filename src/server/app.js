const express = require('express');
const bodyParser = require('body-parser');

const ASCIIMathTeXImg = require('./ASCIIMathTeXImg');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/api/translate', (req, res) => {
	asciiMarkups = req.body.markups;
	if (asciiMarkups === undefined) {
		asciiMarkups = Array();
	} else if (asciiMarkups.constructor !== Array) {
		asciiMarkups = [asciiMarkups];
	}

	latexMarkups = asciiMarkups.map((asciiMarkup) => {
		return ASCIIMathTeXImg.AMTparseAMtoTeX(asciiMarkup);
	});
	res.send(latexMarkups);
});

const port = 8080;
app.listen(port, () => {
	console.log('App listening on port', port);
});
