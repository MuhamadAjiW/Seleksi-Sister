// Display related functions
function toContent() {
    window.location.href = "content";
}

// API related functions
async function getQueryParam(name){
    try{
        const response = await fetch('/info/query');
        const data = await response.json();
        console.log(data);
        console.log(data[name]);
        return data[name];
    } catch (error){
        console.error("Error fetching JSON: ", error);
    }
}

async function loadPersonDetails(){
    let index = await getQueryParam('index');
    if(index != null){

        fetch('/data/people.json')
            .then(response => response.json())
            .then(data => {
                index = parseInt(index);
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