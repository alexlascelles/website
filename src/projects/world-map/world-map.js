import { panZoomSetup } from './pan-zoom.js';

const MAP_SCALE = 123;
const SVG_WIDTH = 772;
const SVG_HEIGHT = 500;

// Base color scale for population
const color = d3
  .scaleThreshold()
  .domain([ 
    10000, 100000, 500000, 1000000, 5000000, 
    10000000, 50000000, 100000000, 500000000, 
    1500000000 
  ])
  .range([ 
    'rgb(247,251,255)', 'rgb(222,235,247)', 'rgb(198,219,239)',
    'rgb(158,202,225)', 'rgb(107,174,214)', 'rgb(66,146,198)',
    'rgb(33,113,181)', 'rgb(8,81,156)', 'rgb(8,48,107)', 'rgb(3,19,43)'
  ]);

// Tooltip and formatting
const format = d3.format(',');
const tooltip = d3.select('.tooltip');
const tooltipCountry = tooltip.select('.country');
const tooltipPopulation = tooltip.select('.population');

const baseHighlightColor = d3.rgb(70, 130, 180); // Starting blue color
const visitedCountries = new Set();
let highlightedCountries = [];

// Load country data and setup map
async function load(svg, path) {
  const countryDataRes = await fetch('world-countries.json');
  const countryData = (await countryDataRes.json()).features;
  
  const populationRes = await fetch('world-population.tsv');
  const populationData = await parsePopulationData(await populationRes.text());
  mergePopulationData(countryData, populationData);

  // Load highlighted countries and dates
  const highlightDataRes = await fetch('highlighted_countries.json');
  highlightedCountries = (await highlightDataRes.json()).sort((a, b) => new Date(a.date) - new Date(b.date));

  renderCountries(svg, path, countryData);
  initializeSlider();
  updateCountryCount(); // Initialize the count display
}

// Parse population TSV data into JSON format
function parsePopulationData(tsvText) {
  return tsvText.split('\n').map(line => {
    const [id, , population] = line.split('\t');
    return { id, population: +population };
  });
}

// Merge population data with country data
function mergePopulationData(countryData, populationData) {
  const populationById = {};
  populationData.forEach(d => populationById[d.id] = d.population);
  countryData.forEach(d => d.population = populationById[d.id]);
}

// Render each country path and set up tooltips
function renderCountries(svg, path, countryData) {
  svg.append('g')
    .attr('class', 'countries')
    .selectAll('path')
    .data(countryData)
    .enter()
    .append('path')
    .attr('d', path)
    .attr('id', d => `country-${d.id}`)
    .style('fill', d => color(d.population))
    .on('mouseenter', pathEntered)
    .on('mousemove', pathMoved)
    .on('mouseout', hideTooltip);
}

// Tooltip handling
function pathEntered() { this.parentNode.appendChild(this); }
function pathMoved(d) {
  tooltipCountry.text(d.properties.name);
  tooltipPopulation.text(format(d.population));
  tooltip
    .style('left', d3.event.pageX + 'px')
    .style('top', d3.event.pageY + 'px')
    .style('opacity', 0.7);
}
function hideTooltip() { tooltip.style('opacity', 0); }

// Highlight a country based on the slider’s index
function highlightCountry(index) {
  if (index < highlightedCountries.length) {
    const countryId = `country-${highlightedCountries[index].id}`;
    const countryPath = d3.select(`#${countryId}`);
    const countryKey = highlightedCountries[index].id;

    if (!visitedCountries.has(countryKey)) {
      visitedCountries.add(countryKey);
      updateCountryCount(); // Update the country count each time a new country is added
    }

    // Set color based on visit frequency
    const highlightCount = visitedCountries.has(countryKey) ? 2 : 1;
    const newColor = baseHighlightColor.darker(0.2 * (highlightCount - 1));
    countryPath.style('fill', newColor);
  }
}

// Update the country count display
function updateCountryCount() {
  document.getElementById("countryCount").textContent = "Number of Countries Visited: " + visitedCountries.size;
}

// Slider initialization for date-based highlights
function initializeSlider() {
  const slider = document.getElementById('dateSlider');
  slider.max = highlightedCountries.length - 1;
  slider.addEventListener('input', function () {
    const index = parseInt(this.value);
    resetCountries();  // Reset country colors before reapplying
    for (let i = 0; i <= index; i++) {
      highlightCountry(i);
    }

    // Update the date display
    const currentDate = highlightedCountries[index].date;
    document.getElementById("dateDisplay").textContent = "Date: " + formatDate(currentDate);
  });
}

// Function to format the date into a more readable format (e.g., Apr 13th, 1995)
function formatDate(date) {
  const d = new Date(date);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return d.toLocaleDateString('en-US', options);
}

// Reset country colors and clear visited states
function resetCountries() {
  d3.selectAll('.countries path').style('fill', d => color(d.population));
  visitedCountries.clear();
  updateCountryCount(); // Reset the country count on map reset
}

export function createWorldMap(svgId) {
  const svg = d3
    .select('#' + svgId)
    .attr('width', SVG_WIDTH)
    .attr('height', SVG_HEIGHT)
    .attr('viewBox', `0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`);

  panZoomSetup(svgId, SVG_WIDTH, SVG_HEIGHT);

  const projection = d3
    .geoMercator()
    .scale(MAP_SCALE)
    .translate([SVG_WIDTH / 2, SVG_HEIGHT / 1.41]);

  const path = d3.geoPath().projection(projection);

  load(svg, path);
}
