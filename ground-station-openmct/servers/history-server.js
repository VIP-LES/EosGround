let express = require('express');

function HistoryServer(spacecraft) {
    let router = express.Router();

    router.get('/:pointId', function (req, res) {
        let start = +req.query.start;
        let end = +req.query.end;
        let ids = req.params.pointId.split(',');

        let response = ids.reduce(function (resp, id) {
            return resp.concat(spacecraft.history[id].filter(function (p) {
                return p.timestamp > start && p.timestamp < end;
            }));
        }, []);
        res.status(200).json(response).end();
    });

    return router;
}

module.exports = HistoryServer;

