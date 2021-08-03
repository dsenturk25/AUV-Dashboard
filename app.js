
const express = require('express');
const path = require('path')
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000

const indexRouter = require('./Routers/indexRoute');

app.use(express.static(path.join(__dirname, "public")));

app.use('/', indexRouter)

app.listen(port, () => {
  console.log('Listening to server on port ' + port)
})