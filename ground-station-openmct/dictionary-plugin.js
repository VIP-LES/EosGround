function getDictionary() {
    return http.get('/dictionary.json')
        .then(function (result) {
            return result.data;
        });
}

let objectProvider = {
    get: function (identifier) {
        return getDictionary().then(function (dictionary) {
            if (identifier.key === 'balloon') {
                return {
                    identifier: identifier,
                    name: dictionary.name,
                    type: 'folder',
                    location: 'ROOT'
                };
            } else {
                let measurement = dictionary.measurements.filter(function (m) {
                    return m.key === identifier.key;
                })[0];
                return {
                    identifier: identifier,
                    name: measurement.name,
                    type: 'EOS',
                    telemetry: {
                        values: measurement.values
                    },
                    location: 'EOS:balloon'
                };
            }
        });
    }
};

let compositionProvider = {
    appliesTo: function (domainObject) {
        return domainObject.identifier.namespace === 'EOS' &&
               domainObject.type === 'folder';
    },
    load: function (domainObject) {
        return getDictionary()
            .then(function (dictionary) {
                return dictionary.measurements.map(function (m) {
                    return {
                        namespace: 'EOS',
                        key: m.key
                    };
                });
            });
    }
};

let DictionaryPlugin = function (openmct) {
    return function install(openmct) {
        openmct.objects.addRoot({
            namespace: 'EOS',
            key: 'balloon'
        });

        openmct.objects.addProvider('EOS', objectProvider);

        openmct.composition.addProvider(compositionProvider);

        openmct.types.addType('EOS', {
            name: 'Telemetry Endpoints',
            description: 'Data from sensors aboard the EOS Weather Balloon.',
            cssClass: 'icon-telemetry'
        });
    };
};