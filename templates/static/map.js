function loadCentersFromCSV(map) {
    var csvFilePath = 'static/out.csv';
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

//Attention pour compter le nombre de clics, il faudra stocker les résultats dans la base de données

var clickCounters = {};

function incrementClickCounter(popupId) {
    if (!clickCounters[popupId]) {
        clickCounters[popupId] = 1;
    } else {
        clickCounters[popupId]++;
    }
    console.log(`Nombre de clics pour la popup ${popupId} : ${clickCounters[popupId]}`);
}

function placeMarkersFromCSVData(map, csvData) {
    var markers = L.markerClusterGroup();
    var visibleCentersList = document.getElementById('visible-centers-list');
    var currentBounds = map.getBounds();
    csvData.forEach(center => {
        var x = parseFloat(center.LATITUDE);
        var y = parseFloat(center.LONGITUDE);
        if (!isNaN(x) && !isNaN(y)) {
            var popupContent = `
                <div class="custom-popup">
                <strong>Centre de tri :</strong> ${center.N_SERVICE}<br>
                <strong>Téléphone :</strong> ${center.TEL_SERVICE || 'non renseigné'}<br>
                <strong>Adresse :</strong> ${center.AD1_SITE || 'non renseigné'}<br>
                <strong>Code Postal :</strong> ${center.CP_SITE || 'non renseigné'}<br>
                <strong>Ville :</strong> ${center.L_VILLE_SITE || 'non renseigné'}<br>
                <div class="star" onmouseover="showTooltip(this)" onmouseout="hideTooltip(this)" onclick="toggleFavorite(this)"></div>
                <div class="tooltip">Ajouter aux favoris</div>
                <button onclick="openGoogleMaps(${x}, ${y})">Itinéraire</button><br>
                <button onclick="leaveComment('${center.N_SERVICE}')">Laisser un commentaire sur ce centre</button></div>
            `; // Fonction leaveComment à définir (relier à l'espace de commentaires)
            var marker = L.marker([x,y]).bindPopup(popupContent);
            marker.on('click', function () {
                incrementClickCounter(center.N_SERVICE);
            });
            markers.addLayer(marker);
            if (currentBounds.contains([x,y])) {
                var centerName = center.N_SERVICE || 'Non renseigné';
                var listItem = document.createElement('div');
                listItem.textContent = centerName;
                listItem.addEventListener('click', function () {
                map.setView([x, y], 15);
                });
                visibleCentersList.appendChild(listItem);
            }
        } 
    });
    map.addLayer(markers);
}

function openGoogleMaps(latitude, longitude) {
    window.open(`https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`);
}

function toggleFavorite(starElement) {
    starElement.classList.toggle('filled');
}

function showTooltip(starElement) {
    var tooltip = starElement.nextElementSibling;
    tooltip.style.display = 'block';
}

function hideTooltip(starElement) {
    var tooltip = starElement.nextElementSibling;
    tooltip.style.display = 'none';
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