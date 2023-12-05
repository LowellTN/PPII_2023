function initMap() {
    var map = L.map('map').setView([0,0],2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    var defaultMarker = L.marker([0,0]).addTo(map)
        .bindPopup('Marqueur par défaut');
    loadNearbyCenters(map);
}

function loadNearbyCenters(map) {
    var centerMarker = L.marker([12.9714, 77.5946]).addTo(map)
        .bindPopup('Centre de tri factice')
}

window.onload = function () {
    initMap();
};