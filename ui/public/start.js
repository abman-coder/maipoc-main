var express = require('express');
var server = express();
var options = {
    index: ['index.html']
};
const swaggerUi = require('swagger-ui-express');
const openApiDocumentation = require('./openapi.json');
server.use('/api-docs', swaggerUi.serve, swaggerUi.setup(openApiDocumentation));
server.use('/', express.static('/home/site/wwwroot', options));
server.use('/*', express.static('/home/site/wwwroot', options));
server.listen(process.env.PORT);