function loadCentersFromCSV(map) {
    var csvFilePath = 'out.csv';
    fetch(csvFilePath)
        .then(response => response.text())
        .then(csvData => Papa.parse(csvData, { header: true }))
        .then(data => {
            var filteredData = filterMostRecentEntries(data.data);
            placeMarkersFromCSVData(map, filteredData);
        })
        .catch(error => console.error('Erreur lors de la récupération des données CSV:', error));
}

function filterMostRecentEntries(data) {
    var latestEntries = {};
    data.forEach(entry => {
        if (entry.N_SERVICE !== undefined) {
            var nService = entry.N_SERVICE.toUpperCase();
            if (!latestEntries[nService] || entry.ANNEE > latestEntries[nService].ANNEE) {
                latestEntries[nService] = entry;
            }
        }
    });
    var filteredData = Object.values(latestEntries);
    return filteredData;
}

function placeMarkersFromCSVData(map, csvData) {
    var markers = L.markerClusterGroup();
    csvData.forEach(center => {
        var x = parseFloat(center.LATITUDE);
        var y = parseFloat(center.LONGITUDE);
        if (!isNaN(x) && !isNaN(y)) {
            var marker = L.marker([x,y]).bindPopup('Centre de tri : ' + center.N_SERVICE);
            markers.addLayer(marker);
        } 
    });
    map.addLayer(markers);
}

function initMap() {
    var map = L.map('map');
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    if (navigator.permissions && navigator.geolocation) {
        navigator.permissions.query({ name: 'geolocation'}).then(permissionStatus => {
            if (permissionStatus.state === 'granted') {
                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        var userCoordinates = [position.coords.latitude, position.coords.longitude];
                        map.setView(userCoordinates,13);
                        loadCentersFromCSV(map);
                    },
                    function (error) {
                        console.error('Erreur lors de la récupération de la position de l\'utilisateur :', error.message);
                        loadCentersFromCSV(map);
                    }
                );
            } else if (permissionStatus.state === 'prompt') {
                var isUserAgreed = confirm('Veuillez autoriser l\'accès à votre position pour une meilleure expérience.');
                if (isUserAgreed) {
                    navigator.geolocation.getCurrentPosition(
                        function (position) {
                            var userCoordinates = [position.coords.latitude, position.coords.longitude];
                            map.setView(userCoordinates,13);
                            loadCentersFromCSV(map);
                        },
                        function (error) {
                            console.error('Erreur lors de la récupération de la position de l\'utilisateur :', error.message);
                        }
                    );
                } else {
                    console.error('La géolocalisation n\'est pas autorisée par l\'utilisateur.');
                    loadCentersFromCSV(map);
                }
            } else {
                console.error('La géolocalisation n\'est pas autorisée par l\'utilisateur.');
                loadCentersFromCSV(map);
            }
        });
    } else {
        console.error('La géolocalisation n\'est pas prise en charge par votre navigateur.');
        loadCentersFromCSV(map);
    }
}

window.onload = function () {
    initMap();
};