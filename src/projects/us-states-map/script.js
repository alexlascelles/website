var svg = d3.select("svg");
var path = d3.geoPath();
var currentIndex = 0;
var highestIndex = 0;  // Track the highest index highlighted so far
var highlightedStates = [];
var stateHighlightCount = {}; // Track how many times each state has been highlighted
var stateFirstHighlight = {}; // Track the first highlight index of each state
var visitedStates = new Set(); // Set to keep track of unique visited states

// Load the US states topojson file
d3.json("https://d3js.org/us-10m.v1.json").then(function (us) {
  // Create the states group
  var states = svg
    .append("g")
    .attr("class", "states")
    .selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
    .enter()
    .append("path")
    .attr("d", path)
    .attr("id", function (d) {
      return "state-" + d.id; // Update the id to be 'state-<id>'
    });

  // Append state borders
  svg
    .append("path")
    .attr("class", "state-borders")
    .attr(
      "d",
      path(
        topojson.mesh(us, us.objects.states, function (a, b) {
          return a !== b;
        })
      )
    );

  // Load the highlighted states JSON (with ids, names, and dates)
  d3.json("highlighted_states_AL.json").then(function (data) {
    highlightedStates = data.sort(function (a, b) {
      return new Date(a.date) - new Date(b.date);
    });
    updateSlider();
  });

  // Function to highlight a state
  function highlightState(index) {
    if (index < highlightedStates.length) {
      var stateId = "state-" + highlightedStates[index].id; // Use 'state-' prefix
      var statePath = svg.select("#" + stateId);

      // Track first highlight index for each state
      var stateKey = highlightedStates[index].id;

      if (!(stateKey in stateFirstHighlight)) {
        stateFirstHighlight[stateKey] = index; // Set first time it was highlighted
      }

      // Increment the highlight count for this state
      stateHighlightCount[stateKey] = (stateHighlightCount[stateKey] || 0) + 1;

      // Determine the current highlight count for the state and base color
      var highlightCount = stateHighlightCount[stateKey];
      var baseColor = d3.rgb(70, 130, 180); // Initial steel blue color

      // Darken the color progressively for each highlight
      var color = baseColor.darker(0.1 * (highlightCount - 1));

      // If we're moving backward to the first highlight, reset to base color
      if (index === stateFirstHighlight[stateKey]) {
        color = baseColor;
      }

      // Apply the progressively darkened color to the state
      statePath.style("fill", color);

      // Add the state to the visited set if not already added
      visitedStates.add(stateKey);
    }
  }

  function formatDate(dateStr) {
    const [year, month, day] = dateStr.split('-');
    const date = new Date(year, month - 1, day); // Month is zero-indexed

    const formattedDay = date.getDate();
    const formattedMonth = date.toLocaleString("default", { month: "short" });
    const formattedYear = date.getFullYear();

    let suffix = ["st", "nd", "rd", "th"][
      (formattedDay % 10 > 3 || [11, 12, 13].includes(formattedDay) || formattedDay % 10 === 0) ? 3 : formattedDay % 10 - 1
    ];

    return `${formattedMonth} ${formattedDay}${suffix}, ${formattedYear}`;
}

  // Function to update the slider range and text
  function updateSlider() {
    document.getElementById("dateSlider").max = highlightedStates.length - 1;
    document.getElementById("dateSlider").value = currentIndex;
    document.getElementById("dateDisplay").textContent = "Date: " + formatDate(highlightedStates[currentIndex].date);
    updateStateCount();  // Update the state count on each slider change
  }

  // Function to count unique states visited so far
  function updateStateCount() {
    document.getElementById("stateCount").textContent = "Number of States Visited: " + visitedStates.size;
  }

  // Handle the date slider input to change state highlighting
  document.getElementById("dateSlider").addEventListener("input", function (event) {
    var newIndex = event.target.value;

    // Only highlight new states if moving forward (increasing index)
    if (newIndex > highestIndex) {
      currentIndex = newIndex;
      svg.selectAll(".states path").style("fill", ""); // Clear all highlights
      svg.selectAll(".states path").style("opacity", ""); // Clear opacity
      for (var i = 0; i <= currentIndex; i++) {
        highlightState(i); // Highlight states up to the current index
      }
      highestIndex = currentIndex; // Update the highest index
      updateSlider();
    } else {
      // If moving backward, don't change the highlight colors
      currentIndex = newIndex;
      svg.selectAll(".states path").style("fill", ""); // Clear all highlights
      svg.selectAll(".states path").style("opacity", ""); // Clear opacity
      for (var i = 0; i <= currentIndex; i++) {
        highlightState(i); // Highlight states up to the current index
      }

      // Remove states from the visited set as we move backward
      visitedStates.clear(); // Reset visited states
      for (var i = 0; i <= currentIndex; i++) {
        visitedStates.add(highlightedStates[i].id); // Add states up to current index
      }

      updateStateCount();
      updateSlider();
    }
  });

  // Refresh Button - Reset and Restart Animation
  document.getElementById("refreshButton").addEventListener("click", function () {
    currentIndex = 0;
    highestIndex = 0; // Reset the highest index to 0
    visitedStates.clear(); // Clear the visited states set
    svg.selectAll(".states path").style("fill", ""); // Clear all state colors
    svg.selectAll(".states path").style("opacity", ""); // Reset opacity
    stateHighlightCount = {}; // Reset highlight counts
    stateFirstHighlight = {}; // Reset first highlight tracking
    updateSlider();
    updateStateCount();  // Reset state count on refresh
  });
});
