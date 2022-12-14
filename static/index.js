const form = document.getElementById("form");
const inputFile = document.getElementById("file");

const formData = new FormData();

const handleSubmit = (event) => {
    event.preventDefault();

    for (const file of inputFile.files) {
        formData.append("files", file);
    }

    fetch("http://localhost:5000/upload_file/2342", {
        method: "post",
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => ("Something went wrong!", error));

    formData.delete("files");
};

form.addEventListener("submit", handleSubmit);
