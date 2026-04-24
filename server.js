const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 5173;
const ROOT = __dirname;
const ALLOWED_FILES = new Set(["index.html", "app.js", "style.css"]);

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
};

const server = http.createServer((req, res) => {
  const requestPath = req.url === "/" ? "index.html" : req.url.split("?")[0].replace(/^\/+/, "");
  const safePath = decodeURIComponent(requestPath);

  if (!ALLOWED_FILES.has(safePath)) {
    res.writeHead(404);
    res.end("Not found");
    return;
  }

  const filePath = path.resolve(ROOT, safePath);
  const rootPrefix = `${ROOT}${path.sep}`;

  if (filePath !== ROOT && !filePath.startsWith(rootPrefix)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": contentType });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
