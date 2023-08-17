// Display related functions
function toContent() {
    window.location.href = "content";
}
function showEditForm(){
    let index = getQueryParam('index');
    var editform = document.getElementById("editform");

    if(index != null){
        if(editform.style.display == "none"){
            editform.style.display = "block";
            accessPersonDetails();
        }
        else{
            editform.style.display = "none";
        }
    }
}

// API related functions
function getQueryParam(name){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}
async function accessPersonDetails() {
    const persondeets = document.getElementById('person-deets');
    
    document.getElementById("enameinput").value = document.getElementById("nameinfo").textContent;
    document.getElementById("edescinput").value = document.getElementById("descinfo").textContent;
}
async function loadPersonDetails(){
    let index = getQueryParam('index');
    if(index != null){

        fetch(`/api/info?index=${index}`)
            .then(response => {
                if(!response.ok){
                    throw new Error('HTTP error! Status: ${response.status}');
                }
                return response.json();
            })
            .then(data => {
                if(data){
                    const persondeets = document.getElementById('person-deets');
                    
                    const nameinfo = document.createElement('h2');
                    nameinfo.innerText = data.name;
                    nameinfo.id = "nameinfo";

                    const descinfo = document.createElement('p');
                    descinfo.innerText = data.desc;
                    descinfo.id = "descinfo";

                    persondeets.appendChild(nameinfo);
                    persondeets.appendChild(descinfo);                    
                }
            }).catch(error => console.error('Error fetching JSON: ', error));
    } else{
        console.error("No index provided")
    }
}
async function edit(){
    let index = getQueryParam('index');
    const niName = document.getElementById("enameinput").value;
    const niDesc = document.getElementById("edescinput").value;

    const reqData = {
        name: niName,
        desc: niDesc
    }
    console.log(index);

    try{
        const response = await fetch(`/api/info?index=${index}`, {
            method: 'PUT',
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
        window.location.href = `info?index=${index}`;
    }
    catch(error){
        console.error('Error sending add request: ', error);
    }
}
// Button Logics
document.getElementById("contentbt").addEventListener("click", toContent);
document.getElementById("editbt").addEventListener("click", showEditForm);
document.getElementById("confirmbt").addEventListener("click", edit);


loadPersonDetails();