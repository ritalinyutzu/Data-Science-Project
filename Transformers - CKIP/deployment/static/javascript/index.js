let input = document.querySelector("input.file_input");
let button = document.querySelector("button");
let div_preview = document.querySelector("div.preview");
let div_result = document.querySelector("div.result");
let div_b = document.querySelector("div.b");
let div_r = document.querySelector("div.r");

input.addEventListener("change", (e) => {
    div_preview.innerText = input.files[0].name;
});

button.addEventListener("click", (e) => {
    e.preventDefault();
    div_b.innerText = "DATA ANALYSING......";
    div_preview.innerText = "No files currently selected for";
    let file = input.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = (e) => {
        let file_text = reader.result;
        let file_array = csv_to_array(file_text);
        let file_json = {
            brand: file_array[1][0],
            element: file_array[1][1],
        };
        async function send_to_api() {
            let response = await fetch("/pred", {
                method: "POST",
                body: JSON.stringify(file_json),
                headers: {
                    "content-type": "application/json",
                },
            });
            let response_body_json = await response.json();
            div_result.classList.add("add2");
            div_b.innerText = file_array[1][0];
            div_r.classList.add("add");
            div_r.innerText =
                response_body_json[Object.keys(response_body_json)[0]];
        }
        send_to_api();
    };
});

function csv_to_array(strData, strDelimiter) {
    // Check to see if the delimiter is defined. If not,
    // then default to comma.
    strDelimiter = strDelimiter || ",";

    // Create a regular expression to parse the CSV values.
    var objPattern = new RegExp(
        // Delimiters.
        "(\\" +
            strDelimiter +
            "|\\r?\\n|\\r|^)" +
            // Quoted fields.
            '(?:"([^"]*(?:""[^"]*)*)"|' +
            // Standard fields.
            '([^"\\' +
            strDelimiter +
            "\\r\\n]*))",
        "gi"
    );

    // Create an array to hold our data. Give the array
    // a default empty first row.
    var arrData = [[]];

    // Create an array to hold our individual pattern
    // matching groups.
    var arrMatches = null;

    // Keep looping over the regular expression matches
    // until we can no longer find a match.
    while ((arrMatches = objPattern.exec(strData))) {
        // Get the delimiter that was found.
        var strMatchedDelimiter = arrMatches[1];

        // Check to see if the given delimiter has a length
        // (is not the start of string) and if it matches
        // field delimiter. If id does not, then we know
        // that this delimiter is a row delimiter.
        if (
            strMatchedDelimiter.length &&
            strMatchedDelimiter !== strDelimiter
        ) {
            // Since we have reached a new row of data,
            // add an empty row to our data array.
            arrData.push([]);
        }

        var strMatchedValue;

        // Now that we have our delimiter out of the way,
        // let's check to see which kind of value we
        // captured (quoted or unquoted).
        if (arrMatches[2]) {
            // We found a quoted value. When we capture
            // this value, unescape any double quotes.
            strMatchedValue = arrMatches[2].replace(new RegExp('""', "g"), '"');
        } else {
            // We found a non-quoted value.
            strMatchedValue = arrMatches[3];
        }

        // Now that we have our value string, let's add
        // it to the data array.
        arrData[arrData.length - 1].push(strMatchedValue);
    }

    // Return the parsed data.
    return arrData;
}
