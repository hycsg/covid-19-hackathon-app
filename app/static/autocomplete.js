const inputs = {
    "submit": document.getElementById("submit")
};
let count = 0;

function autocomplete(name) {
    let inp = document.getElementById(`${name}_input`)
    inputs[name] = inp
    let currentFocus;
    let listOpen = false;

    inp.addEventListener("input", function(e) {
        let a, b, i, val = this.value;
        if (!val) { return false; }
        currentFocus = -1;

        let query;
        const v = inp.value.toLowerCase();
        if (name == "state") {
            query = `get_${name}?s=${v}`
        } else {
            query = `get_${name}?s=${inputs["state"].value.toLowerCase()}&c=${v}`
        }
        query += `&i=${count}`;

        const xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200 && this.responseURL.split("&i=")[1] == count) {
                closeAllLists();
                arr = xhttp.responseText.split(";");
                a = document.createElement("DIV");
                a.setAttribute("id", inp.id + "autocomplete-list");
                a.setAttribute("class", "autocomplete-items");

                inp.parentNode.appendChild(a);

                let valid = false;
                for (i = 0; i < arr.length; i++) {
                    arr[i] = arr[i].replace(/^\w/, c => c.toUpperCase());
                    if (arr[i].toUpperCase() == val.toUpperCase()) {
                        valid = true;
                    }
                    if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                        b = document.createElement("DIV");
                        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                        b.innerHTML += arr[i].substr(val.length);
                        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                        const itemVal = arr[i]
                        b.addEventListener("click", function(e) {
                            inp.value = itemVal
                            validate(true);
                        });
                        a.appendChild(b);
                    }
                }

                if (arr.length > 0) {
                    currentFocus = 0;
                    addActive(document.getElementById(inp.id + "autocomplete-list").getElementsByTagName("div"))
                }

                listOpen = true;
                validate(valid);
            }
        };
        xhttp.open("GET", query, true);
        xhttp.send();
    });

    inp.addEventListener("keydown", function(e) {
        let x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode == 40) {
            currentFocus++;
            addActive(x);
        } else if (e.keyCode == 38) {
            currentFocus--;
            addActive(x);
        } else if (e.keyCode == 13 || e.keyCode == 9) {
            if (currentFocus == -1) currentFocus = 0;
            if (listOpen) {
                e.preventDefault();
                if (x) x[currentFocus].click();
            }
        }
    });

    function validate(valid) {
        if (valid) {
            inp.classList.add("is-valid");
            if (inp == inputs.state) {
                inputs.county.value = ""
                inputs.county.classList.remove("is-valid");
                inputs.county.classList.remove("d-none");
                inputs.county.focus();
            } else if (inp == inputs.county) {
                inputs.submit.disabled = false;
            }
            closeAllLists();
        } else {
            inp.classList.remove("is-valid");
            if (inp == inputs.state) {
                inputs.county.classList.add("d-none");
            } else if (inp == inputs.county) {
                inputs.submit.disabled = true;
            }
        }
    }

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        listOpen = false;
        let x = document.getElementsByClassName("autocomplete-items");
        for (let i = 0; i < x.length; i++) {
            if (elmnt != x[i] && elmnt != inp) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }

    document.addEventListener("click", function(e) {
        closeAllLists(e.target);
    });
}

autocomplete("state")
autocomplete("county")

window.onload = () => {
    inputs["state"].focus()
}