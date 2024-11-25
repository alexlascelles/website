// Set up SVG dimensions based on the .outer-container size
const width = 750; // Matches the .outer-container size in CSS
const height = 750; // Matches the .outer-container size in CSS

// Radius of the Earth image in pixels (adjust this as needed)
const earthRadius = 47.7825; // 6,371 km

// Define scaling factors for normal and zoomed-in view
const normalKmToPixels = 750 / 100000; // 1 km = 0.0075 pixels (Normal view)
const zoomedInKmToPixels = 750 / 20000; // 1 km = 0.0375 pixels (Zoomed-in view)

let currentKmToPixels = normalKmToPixels; // Start with normal scaling factor
let zoomedIn = false; // Track zoom state
let selectedDateRange = "All"; // Default date range to show all satellites

// Select the SVG and set its dimensions
const svg = d3.select(".satellite-orbit")
    .attr("width", width)
    .attr("height", height);

// Load satellite data from the CSV file
d3.csv("earth_orbiting_satellites_50k.csv").then(data => {
    window.satelliteData = data; // Store data globally for re-filtering
    renderSatellites(data);  // Initial render with "All" satellites
    renderEarth();
});

// Function to filter satellites by date range
function filterSatellitesByDate(data, range) {
    return data.filter(d => {
        const launchDate = new Date(d.LAUNCH_DATE);
        if (range === "2020-present") return launchDate >= new Date("2020-01-01");
        else if (range === "2000-2020") return launchDate >= new Date("2000-01-01") && launchDate < new Date("2020-01-01");
        else if (range === "1980-2000") return launchDate >= new Date("1980-01-01") && launchDate < new Date("2000-01-01");
        else if (range === "1958-1980") return launchDate >= new Date("1958-01-01") && launchDate < new Date("1980-01-01");
        return true; // "All" selected, return all satellites
    });
}

// Function to render Earth image and update ruler
function renderEarth() {
    // Remove any existing Earth image
    svg.selectAll(".earth-image").remove();

    // Add Earth image with size depending on zoom state
    const earthSize = zoomedIn ? earthRadius * 5 : earthRadius;
    const earthImageSize = earthSize * 2;  // Adjust to fit the size of the image

    svg.append("image")
        .attr("class", "earth-image")
        .attr("x", width / 2 - earthImageSize / 2)  // Center the image
        .attr("y", height / 2 - earthImageSize / 2)  // Center the image
        .attr("width", earthImageSize)
        .attr("height", earthImageSize)
        .attr("xlink:href", "earth.png");  // Use the earth image
}

// Function to render satellites based on current scale and filtered data
function renderSatellites(data) {
    // Filter satellite data based on selected date range
    const filteredData = filterSatellitesByDate(data, selectedDateRange).map(d => ({
        x: width / 2 + (+d.X_COORD * currentKmToPixels),  // Convert X_COORD to pixels, centered on Earth
        y: height / 2 + (+d.Y_COORD * currentKmToPixels) // Convert Y_COORD to pixels, centered on Earth
    }));

    // Update satellite count display
    document.getElementById('satellite-count').textContent = filteredData.length;

    // Clear existing circles and re-add them with new scaling
    svg.selectAll("circle").remove();

    // Append updated circles
    svg.selectAll("circle")
        .data(filteredData)
        .enter()
        .append("circle")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", .5) // Set a small radius for the satellites
        .attr("fill", "white");
}

// Function to toggle zoom view and switch rulers
function toggleZoom() {
    zoomedIn = !zoomedIn; // Toggle zoom state
    currentKmToPixels = zoomedIn ? zoomedInKmToPixels : normalKmToPixels; // Adjust satellite scaling factor

    // Toggle visibility of rulers
    const normalRuler = document.querySelector('.normal-ruler');
    const zoomedRuler = document.querySelector('.zoomed-ruler');

    if (zoomedIn) {
        normalRuler.style.display = 'none';
        zoomedRuler.style.display = 'block';
    } else {
        normalRuler.style.display = 'block';
        zoomedRuler.style.display = 'none';
    }

    // Reload the satellite data with the new scaling factor and date range filter
    renderSatellites(window.satelliteData); // Render satellites with the selected range
    renderEarth();
}

// Add event listeners for date range buttons and update active state
function setupDateRangeButtons() {
    const buttons = {
        allButton: "All",
        range2020Button: "2020-present",
        range2000Button: "2000-2020",
        range1980Button: "1980-2000",
        range1958Button: "1958-1980"
    };

    for (const [buttonId, range] of Object.entries(buttons)) {
        document.getElementById(buttonId).addEventListener("click", () => {
            selectedDateRange = range;
            renderSatellites(window.satelliteData);

            // Remove active class from all buttons and add to the clicked button
            document.querySelectorAll(".button-container button").forEach(button => button.classList.remove("active"));
            document.getElementById(buttonId).classList.add("active");
        });
    }
}

// Select the buttons and the info panels
const openAboutButton = document.getElementById('open-info-about');
const openDebrisButton = document.getElementById('open-info-debris');
const infoAbout = document.getElementById('info-about');
const infoDebris = document.getElementById('info-debris');

// Function to toggle visibility of info panels
function togglePanel(panel) {
    panel.classList.toggle('visible');
}

// Event listeners to open the panels
openAboutButton.addEventListener('click', () => togglePanel(infoAbout));
openDebrisButton.addEventListener('click', () => togglePanel(infoDebris));

// Optional: Close info panels when clicking outside
document.body.addEventListener('click', (event) => {
    if (!infoAbout.contains(event.target) && !openAboutButton.contains(event.target)) {
        infoAbout.classList.remove('visible');
    }
    if (!infoDebris.contains(event.target) && !openDebrisButton.contains(event.target)) {
        infoDebris.classList.remove('visible');
    }
});

// Initialize button setup and default active state for "All" button
setupDateRangeButtons();
document.getElementById("allButton").classList.add("active");

// Add event listener for the zoom button
document.getElementById('zoomButton').addEventListener('click', toggleZoom);