async function fetchShelters(sector = "") {
  const url = sector ? `/shelters?sector=${sector}` : "/shelters";
  const response = await fetch(url);
  const data = await response.json();
  return data.data;
}

function renderChart(data) {
  const ctx = document.getElementById("shelterChart").getContext("2d");
  const names = data.map(s => s.Name);
  const available = data.map(s => s.Available);
  const capacity = data.map(s => s.Capacity);

  new Chart(ctx, {
    type: "bar",
    data: {
      labels: names,
      datasets: [
        {
          label: "Available Beds",
          data: available,
          backgroundColor: "green"
        },
        {
          label: "Total Capacity",
          data: capacity,
          backgroundColor: "gray"
        }
      ]
    }
  });
}

document.getElementById("sectorFilter").addEventListener("change", async (e) => {
  const shelters = await fetchShelters(e.target.value);
  renderChart(shelters);
});

fetchShelters().then(renderChart);