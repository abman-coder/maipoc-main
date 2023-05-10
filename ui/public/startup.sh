export NODE_PATH=/usr/local/lib/node_modules:$NODE_PATH
if [ -z "$PORT" ]; then
export PORT=8080
fi

npm i
npm run build
node /home/site/wwwroot/start.js