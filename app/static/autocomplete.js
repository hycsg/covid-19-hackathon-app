const last = {}
const input = {}

function attach(name) {
    last[name] = ""
    input[name] = document.getElementById(`${name}_input`)
    suggest = document.getElementById(`${name}_suggest`)
    setInterval(() => {
        if(input[name].value == last[name]) return
        last[name] = input[name].value

        let query;
        const val = input[name].value.toLowerCase();
        if(name == "state") {
            query = `get_${name}?s=${val}`
        } else {
            query = `get_${name}?s=${input["state"].value}&c=${val}`
        }

        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                options = xhttp.responseText.split(";");
                suggest.innerHTML = options.join("<br>")
            }
        };
        xhttp.open("GET", query, true);
        xhttp.send();
    }, 200);
}

attach("state");
attach("county");