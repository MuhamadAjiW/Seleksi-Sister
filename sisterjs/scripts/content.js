// Display related functions
function showadd() {
    var addform = document.getElementById("addform");

    if(addform.style.display == "none"){
        addform.style.display = "block";
    }
    else{
        addform.style.display = "none";
    }
}
function toHome() {
    window.location.href = "home";
}

function toPage(index){
    window.location.href = "info?index=" + index;
}

function loadContentList() {
    fetch('/api/infoall')
        .then(response => {
            if(!response.ok){
                throw new Error('HTTP error! Status: ${response.status}');
            }
            return response.json();
        })
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
                viewButton.addEventListener('click', () => toPage(index));

                const delButton = document.createElement('button');
                delButton.innerText = 'Delete';
                delButton.addEventListener('click', () => del(index));

                personElement.appendChild(spacing);
                personElement.appendChild(viewButton);
                personElement.appendChild(delButton);

                peopleList.appendChild(personElement);
            });
        }).catch(error => console.error('Error fetching JSON: ', error));
}


// API related functions
async function add(){
    const niName = document.getElementById("anameinput").value;
    const niDesc = document.getElementById("adescinput").value;

    const reqData = {
        name: niName,
        desc: niDesc
    }

    try{
        const response = await fetch(`/api/info`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reqData)
        });
        if(response.ok){
            console.log("Add request successful")
        }
        else{
            console.log("Add request failed")
        }
        window.location.href = "content";
    }
    catch(error){
        console.error('Error sending add request: ', error);
    }
}

function del(index){
    fetch(`/api/info?index=${index}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok){
            console.log("Delete request successful")
        }
        else{
            console.log("Delete request failed")
        }
        window.location.href = "content";
    })
    .catch(error => console.error('Error sending delete request: ', error));
}

// Button Logics
document.getElementById("addbt").addEventListener("click", add);
document.getElementById("showaddbt").addEventListener("click", showadd);
document.getElementById("homebt").addEventListener("click", toHome);

// Initializations
loadContentList();