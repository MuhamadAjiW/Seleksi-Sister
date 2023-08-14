// Display related functions
function showadd() {
    var addform = document.getElementById("addform");
    var delform = document.getElementById("delform");

    if(addform.style.display = "none"){
        addform.style.display = "block";
        delform.style.display = "none";
    }
}
function showdel() {
    var addform = document.getElementById("addform");
    var delform = document.getElementById("delform");

    if(delform.style.display = "none"){
        addform.style.display = "none";
        delform.style.display = "block";
    }
}
function hide() {
    var addform = document.getElementById("addform");
    var delform = document.getElementById("delform");
    addform.style.display = "none";
    delform.style.display = "none";
}
function toHome() {
    window.location.href = "home";
}

function toPersonPage(index){
    window.location.href = "info?index=" + index;
}

function loadContentList() {
    fetch('/data/people.json')
        .then(response => response.json())
        .then(data => {
            const peopleList = document.getElementById('people-list');

            data.forEach((person, index) => {
                const personElement = document.createElement('li');
                const spacing = document.createElement('span');
                personElement.innerText = person.name;
                personElement.style.marginBottom = '10px';
                spacing.style.marginRight = '10px';

                const viewButton = document.createElement('button');
                viewButton.innerText = 'View Details';
                viewButton.addEventListener('click', () => toPersonPage(index));

                personElement.appendChild(spacing);
                personElement.appendChild(viewButton);

                peopleList.appendChild(personElement);
            });
        }).catch(error => console.error('Error fetching JSON: ', error));
}


// API related functions
function add(){
    const niName = document.getElementById("anameinput").value;
    const niDesc = document.getElementById("adescinput").value;

    const reqData = {
        name: niName,
        description: niDesc
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/add", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(reqData));
}
function del() {
    const niName = document.getElementById("dnameinput").value;

    const reqData = {
        name: niName,
    }
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/add", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(reqData));
}
function info(){
    window.location.href = "home";
}

// Button Logics
document.getElementById("addbt").addEventListener("click", add);
document.getElementById("delbt").addEventListener("click", del);
document.getElementById("showaddbt").addEventListener("click", showadd);
document.getElementById("showdelbt").addEventListener("click", showdel);
document.getElementById("hidebt").addEventListener("click", hide);
document.getElementById("homebt").addEventListener("click", toHome);

// Initializations
loadContentList();