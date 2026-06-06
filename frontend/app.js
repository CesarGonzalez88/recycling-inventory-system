const API_URL = "http://127.0.0.1:8000";

let allMaterials = [];
let allMovements = [];

// MATERIALS
async function loadMaterials() {
    const response = await fetch(`${API_URL}/materials`);
    const data = await response.json();

    console.log("MATERIALS RESPONSE:", data);

    allMaterials = data.data;

    populateMaterialSelect(allMaterials);
    renderMaterials(allMaterials);
}

function renderMaterials(list) {
    const table = document.getElementById("materialsTable");
    table.innerHTML = "";

    list.forEach(item => {
        table.innerHTML += `
            <tr>
                <td>${item.name}</td>
                <td>${item.type}</td>
                <td>${item.quantity}</td>
                <td>${item.unit}</td>
            </tr>
        `;
    });
}

function filterByName(value) {
    const filtered = allMaterials.filter(m =>
        m.name.toLowerCase().includes(value.toLowerCase())
    );

    renderMaterials(filtered);
}

function filterByType(value) {
    const filtered = allMaterials.filter(m =>
        m.type.toLowerCase() === value.toLowerCase()
    );

    renderMaterials(filtered);
}

function sortByName() {
    const sorted = [...allMaterials].sort((a, b) =>
        a.name.localeCompare(b.name)
    );

    renderMaterials(sorted);
}

function sortByQuantity() {
    const sorted = [...allMaterials].sort((a, b) =>
        b.quantity - a.quantity
    );

    renderMaterials(sorted);
}

function sortByType() {
    const sorted = [...allMaterials].sort((a, b) =>
        a.type.localeCompare(b.type)
    );

    renderMaterials(sorted);
}

function populateMaterialSelect(materials) {
    console.log("Materials received:", materials);

    const select = document.getElementById("movementMaterial");

    select.innerHTML = "";

    materials.forEach(material => {

        select.innerHTML += `
            <option value="${material.id}">
                ${material.name}
            </option>
        `;

    });

}

// MOVEMENTS
async function loadMovements(type = null) {
    let url = `${API_URL}/movements`;

    if (type) {
        url += `?type=${type}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    const table = document.getElementById("movementsTable");
    table.innerHTML = "";

    data.data?.forEach(item => {
        const row = `
            <tr>
                <td>${item.id}</td>
                <td>${item.type}</td>
                <td>${item.quantity}</td>
                <td>${item.description}</td>
                <td>${item.created_at}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

// CREATE MATERIALS
async function createMaterial() {
    console.log("CREATE CLICKED");

    const name = document.getElementById("name").value;
    const type = document.getElementById("type").value;
    const quantity = document.getElementById("quantity").value;
    const unit = document.getElementById("unit").value;

    const response = await fetch(`${API_URL}/materials`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name,
            type,
            quantity: parseInt(quantity),
            unit
        })
    });

    console.log("POST DONE");

    await loadMaterials();

    console.log("RELOAD DONE");
}

async function createMovement() {

    const material_id = Number(
        document.getElementById("movementMaterial").value
    );

    const type =
        document.getElementById("movementType").value;

    const quantity = Number(
        document.getElementById("movementQuantity").value
    );

    const description =
        document.getElementById("movementDescription").value;

    const response = await fetch(
        `${API_URL}/movements`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                material_id,
                type,
                quantity,
                description
            })
        }
    );

    const data = await response.json();

    console.log(data);

    await loadMaterials();
    await loadMovements();

}

document.addEventListener("DOMContentLoaded", () => {
    loadMaterials();
    loadMovements();
});