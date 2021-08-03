
const express = require('express')
const Router = express.Router()
const fs = require('fs');

Router.get('/', (req, res) => {
  res.sendFile("./public/index.html");
})


Router.get('/video', (req, res) => {
  const range = req.headers.range;
  if (!range) {
    res.status(400).send("Requires Range header");
  }

  const videoPath = "./public/GraphQL.mp4";
  const videoSize = fs.statSync("./public/GraphQL.mp4").size;

  const CHUNK_SIZE = 10 ** 7; // 1MB
  const start = Number(range.replace(/\D/g, ""));
  const end = Math.min(start + CHUNK_SIZE, videoSize - 1);

  // Create headers
  const contentLength = end - start + 1;
  const headers = {
    "Content-Range": `bytes ${start}-${end}/${videoSize}`,
    "Accept-Ranges": "bytes",
    "Content-Length": contentLength,
    "Content-Type": "video/mp4",
  };

  res.writeHead(206, headers);

  const videoStream = fs.createReadStream(videoPath, { start, end });

  videoStream.pipe(res);
})

module.exports = Router
