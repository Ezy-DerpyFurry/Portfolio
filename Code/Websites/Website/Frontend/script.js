// Variables \\.
const S_PORT = 5501; // Not sure why but theres an error that says "Uncaught SyntaxError: Identifier 'S_PORT' has already been declared (at script.js:1:1)" \\.
const URL = `http://127.0.0.1:${S_PORT}`;

// vv This is to send data (Only the email box) to the server \\.
function sendinfo() {
    const inputElement = document.getElementById('email');
    const inputValue = inputElement.value;

    document.getElementById('output').innerText = "Input Value: " + inputValue; // Okay so this is... stoopid it shouldn't used in a real thing this is just logging the input \\.
                                                                                    // I'm to lazy to remove it \\.

    fetch(URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "data=" + encodeURIComponent(inputValue)
    }).then(res => res.text()).then(text => {
        console.log("Response from server:", text);
    });
}

// vv This gets all the data from the output.txt file it doesnt do much right now but logs "Sent" \\.
function getinfo() {
    fetch(URL, {
        method: "GET"
    })
    .then(res => res.text()).then(text => {
        console.log("Data retrieved: ", text);
    })
    .catch(error => {
        console.log("ERROR: ", error)
    })
}