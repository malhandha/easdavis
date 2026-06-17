// ====================================
// CONFIG
// ====================================

// LOCAL
const API_URL = "http://127.0.0.1:5000";

// ONLINE
// const API_URL = "https://backend-kamu.up.railway.app";


// ====================================
// KPI
// ====================================

async function loadKPI() {

    try {

        const category =
            document.getElementById("categoryFilter").value;

        const territory =
            document.getElementById("territoryFilter").value;

        const segment =
            document.getElementById("segmentFilter").value;

        const response = await fetch(
            `${API_URL}/kpi?category=${category}&territory=${territory}&segment=${segment}`
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

    } catch (error) {

        console.error(error);

        document.getElementById("sales").innerText =
            "Error";

        document.getElementById("profit").innerText =
            "Error";

        document.getElementById("orders").innerText =
            "Error";

        document.getElementById("margin").innerText =
            "Error";
    }
}


// ====================================
// FILTERS
// ====================================

async function loadFilters() {

    try {

        const response = await fetch(
            `${API_URL}/filters`
        );

        const data = await response.json();

        const categorySelect =
            document.getElementById("categoryFilter");

        const territorySelect =
            document.getElementById("territoryFilter");

        const segmentSelect =
            document.getElementById("segmentFilter");

        data.categories.forEach(category => {

            const option =
                document.createElement("option");

            option.value = category;
            option.textContent = category;

            categorySelect.appendChild(option);
        });

        data.territories.forEach(territory => {

            const option =
                document.createElement("option");

            option.value = territory;
            option.textContent = territory;

            territorySelect.appendChild(option);
        });

        data.segments.forEach(segment => {

            const option =
                document.createElement("option");

            option.value = segment;
            option.textContent = segment;

            segmentSelect.appendChild(option);
        });

    } catch (error) {

        console.error(error);
    }
}


// ====================================
// FILTER EVENTS
// ====================================

document
.getElementById("categoryFilter")
.addEventListener("change", loadKPI);

document
.getElementById("territoryFilter")
.addEventListener("change", loadKPI);

document
.getElementById("segmentFilter")
.addEventListener("change", loadKPI);


// ====================================
// AI ASSISTANT
// ====================================

async function askAI() {

    try {

        const prompt =
            document.getElementById("prompt").value;

        const responseDiv =
            document.getElementById("response");

        responseDiv.innerHTML =
            "Generating insight...";

        const response = await fetch(
            `${API_URL}/ask-ai`,
            {
                method: "POST",
                headers: {
                    "Content-Type":
                    "application/json"
                },
                body: JSON.stringify({
                    prompt: prompt
                })
            }
        );

        const data =
            await response.json();

        responseDiv.innerHTML =
            data.response;

    } catch (error) {

        console.error(error);

        document.getElementById("response")
        .innerHTML =
        "Failed to generate insight.";
    }
}


// ====================================
// INIT
// ====================================

window.onload = () => {

    loadKPI();

    loadFilters();
};