function displayComments() {
    var commentsContainer = document.getElementById("commentsContainer");

    commentsList.forEach(function(comment) {
        var author = comment[0];
        var date = comment[1];
        var wasteTypes = comment[2];
        var commentText = comment[3];

        var commentHTML = `
            <div class="comment">
                <strong>Author:</strong> ${author}<br>
                <strong>Date:</strong> ${date}<br>
                <strong>Waste Types:</strong> ${getSelectedWasteTypes(wasteTypes)}<br>
                <strong>Comment:</strong> ${commentText}
            </div>
        `;

        commentsContainer.innerHTML += commentHTML;
    });
}

function getSelectedWasteTypes(wasteTypes) {
    var selectedTypes = [];
    for (var i = 0; i < wasteTypes.length; i++) {
        if (wasteTypes.charAt(i) === '1') {
            selectedTypes.push("WasteType" + (i + 1));
        }
    }
    return selectedTypes.join(', ');
}

window.onload = displayComments;

