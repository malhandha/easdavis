// ==============================
// KPI FETCH
// ==============================

async function loadKPI() {

    const category =
        document.getElementById("categoryFilter").value;

    const territory =
        document.getElementById("territoryFilter").value;

    const segment =
        document.getElementById("segmentFilter").value;

    const response = await fetch(
        `http://127.0.0.1:5000/kpi?category=${category}&territory=${territory}&segment=${segment}`
    );

    const data = await response.json();

    document.getElementById("sales").innerText =
        "$" + (data.sales / 1000000).toFixed(2) + "M";

    document.getElementById("profit").innerText =
        "$" + (data.profit / 1000000).toFixed(2) + "M";

    document.getElementById("orders").innerText =
        data.orders;

    document.getElementById("margin").innerText =
        data.margin + "%";
}

// ==============================
// LOAD FILTER
// ==============================

async function loadFilters() {

    const response = await fetch("http://127.0.0.1:5000/filters");
    const data = await response.json();

    const categorySelect = document.getElementById("categoryFilter");
    const territorySelect = document.getElementById("territoryFilter");
    const segmentSelect = document.getElementById("segmentFilter");

    // CATEGORY
    data.categories.forEach(category => {

        const option = document.createElement("option");
        option.value = category;
        option.textContent = category;

        categorySelect.appendChild(option);
    });

    // TERRITORY
    data.territories.forEach(territory => {

        const option = document.createElement("option");
        option.value = territory;
        option.textContent = territory;

        territorySelect.appendChild(option);
    });

    // SEGMENT
    data.segments.forEach(segment => {

        const option = document.createElement("option");
        option.value = segment;
        option.textContent = segment;

        segmentSelect.appendChild(option);
    });
}
// ==============================
// FILTER EVENT
// ==============================

document
.getElementById("categoryFilter")
.addEventListener("change", loadKPI);

document
.getElementById("territoryFilter")
.addEventListener("change", loadKPI);

document
.getElementById("segmentFilter")
.addEventListener("change", loadKPI);
// ==============================
// AI CHAT
// ==============================

async function askAI() {

    const prompt = document.getElementById("userQuestion").value;

    const response = await fetch("http://127.0.0.1:5000/ask-ai", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            prompt: prompt
        })
    });

    const data = await response.json();

    document.getElementById("aiResponse").innerText =
        data.response;
}

// ==============================
// INIT
// ==============================

loadKPI();
loadFilters();