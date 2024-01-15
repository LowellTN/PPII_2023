var commentsList = [
    ["User1", "2022-01-14", "110", "This is a comment about the waste sorting center."],
    ["User2", "2022-01-15", "010", "Another user's comment about the waste sorting center."],
    // Add more comments as needed
];

function displayComments() {
    var commentsContainer = document.getElementById("commentsContainer");

    commentsList.forEach(function(comment) {
        var author = comment[0];
        var date = comment[1];
        var wasteTypes = comment[2];
        var commentText = comment[3];

        var commentHTML = `
            <div class="comment">
                <div class="comment-banner">
                    <strong>${author}</strong> - ${date}
                </div>
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

