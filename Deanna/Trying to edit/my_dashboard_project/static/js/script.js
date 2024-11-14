// Function to load HTML content into the tab
function loadTabContent(tabId, fileName) {
    console.log(`Loading content for ${fileName} into ${tabId}`); // Debugging log
    fetch(`/html_files/${fileName}.html`)  // Add .html extension here
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            console.log(`Successfully loaded content for ${fileName}`); // Debugging log
            document.getElementById(tabId).innerHTML = html;
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
    document.getElementById(tabId).classList.add('active');

    // Add active class to the clicked tab button
    evt.currentTarget.classList.add('active');

    // Load content for the selected tab if not already loaded
    const contentDiv = document.getElementById(`${tabId}-content`);
    if (!contentDiv.innerHTML.trim()) {
        const fileName = tabId.replace('tab', 'file');  // Change tab name to file name (e.g., 'tab1' -> 'file1')
        loadTabContent(`${tabId}-content`, fileName);  // Pass file1.html, file2.html, etc.
    }
}

// Automatically open the first tab by default
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.tab-button').click();
});

