// Display related functions
function toContent() {
    window.location.href = "content";
}

// API related functions
function getQueryParam(name){
    //TODO: Ini querynya make library, Coba handle make backendnya
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

function loadPersonDetails(){
    const index = getQueryParam('index');
    if(index != null){

        fetch('/data/people.json')
            .then(response => response.json())
            .then(data => {
                const person = data[index];
                console.log(person);
                if(person){
                    const persondeets = document.getElementById('person-deets');
                    const deets =`
                        <h2>${person.name}</h2>
                        <p>${person.description}</p>
                    `;
                    persondeets.innerHTML = deets;
                }
            }).catch(error => console.error('Error fetching JSON: ', error));
    } else{
        console.error("No index provided")
    }
}

// Button Logics
document.getElementById("contentbt").addEventListener("click", toContent);

loadPersonDetails();