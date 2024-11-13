// Function to load HTML content into the tab
function loadTabContent(tabId, fileName) {
    console.log(`Loading content for ${fileName} into ${tabId}`); // Debugging log

    // Fetch the HTML content from the server
    fetch(`/html_files/${fileName}.html`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            console.log(`Successfully loaded content for ${fileName}`);
            const contentDiv = document.getElementById(tabId);
            contentDiv.innerHTML = html;

            // Initialize map if a map container exists in the loaded content
            const mapElement = contentDiv.querySelector('.map');
            if (mapElement) {
                console.log('Map container found. Initializing map...');
                initializeMap(mapElement.id); // Pass the map container ID
            }
        })
        .catch(error => {
            console.error('Error loading content:', error);
        });
}

// Function to handle tab switching
function openTab(evt, tabId) {
    console.log(`Switching to ${tabId}`); // Debugging log

    // Hide all tab content
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show the clicked tab content
    const contentDiv = document.getElementById(tabId);
    contentDiv.classList.add('active');

    // Add active class to the clicked tab button
    evt.currentTarget.classList.add('active');

    // Load content for the selected tab if not already loaded
    if (!contentDiv.innerHTML.trim()) {
        const fileName = tabId.replace('tab', 'file');  // Change tab name to file name (e.g., 'tab1' -> 'file1')
        loadTabContent(tabId, fileName);
    }
}

// Function to initialize the map (assuming you are using Leaflet)
function initializeMap(mapId) {
    console.log(`Initializing map in container: ${mapId}`);
    const map = L.map(mapId).setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);
}

// Automatically open the first tab by default
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.tab-button').click();
});
