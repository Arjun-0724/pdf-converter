const dropArea =
    document.getElementById("drop-area");

const fileInput =
    document.getElementById("file-input");

const fileName =
    document.getElementById("file-name");

const fileBadge =
    document.getElementById("file-badge");

const sourceSelect =
    document.getElementById("source-format");

const targetSelect =
    document.getElementById("target-format");

const conversionSection =
    document.getElementById(
        "conversion-section"
    );

const convertForm =
    document.getElementById(
        "convert-form"
    );

const statusMessage =
    document.getElementById(
        "status-message"
    );


/* --------------------------
   Click Upload
--------------------------- */

if (dropArea && fileInput) {
    dropArea.addEventListener(
        "click",
        () => fileInput.click()
    );
}


/* --------------------------
   Drag & Drop
--------------------------- */

if (dropArea && fileInput) {

    dropArea.addEventListener(
        "dragover",
        (e) => {
            e.preventDefault();
            dropArea.classList.add(
                "dragover"
            );
        }
    );

    dropArea.addEventListener(
        "dragleave",
        () => {
            dropArea.classList.remove(
                "dragover"
            );
        }
    );

    dropArea.addEventListener(
        "drop",
        (e) => {
            e.preventDefault();

            dropArea.classList.remove(
                "dragover"
            );

            const files =
                e.dataTransfer.files;

            if (files.length) {
                fileInput.files = files;

                fileInput.dispatchEvent(
                    new Event("change")
                );
            }
        }
    );
}


/* --------------------------
   File Selected
--------------------------- */

if (fileInput) {

    fileInput.addEventListener(
        "change",
        function () {

            const file =
                fileInput.files[0];

            if (!file) {

                fileName.textContent =
                    "No file selected";

                fileBadge.style.display =
                    "none";

                conversionSection.style.display =
                    "none";

                return;
            }

            fileName.textContent =
                file.name;

            const extension =
                file.name
                    .split(".")
                    .pop()
                    .toLowerCase();

            fileBadge.style.display =
                "inline-block";

            fileBadge.textContent =
                `Detected: ${extension.toUpperCase()}`;

            sourceSelect.innerHTML =
                `<option>
                    ${extension.toUpperCase()}
                 </option>`;

            fetch(
                `/formats/?source=${extension}`
            )
                .then(
                    response =>
                        response.json()
                )
                .then(
                    data => {

                        targetSelect.innerHTML =
                            "";

                        if (
                            data.formats.length === 0
                        ) {

                            targetSelect.innerHTML =
                                `
                                <option>
                                    No conversions available
                                </option>
                                `;

                            conversionSection.style.display =
                                "block";

                            return;
                        }

                        data.formats.forEach(
                            format => {

                                const option =
                                    document.createElement(
                                        "option"
                                    );

                                option.value =
                                    format;

                                option.textContent =
                                    format.toUpperCase();

                                targetSelect.appendChild(
                                    option
                                );
                            }
                        );

                        conversionSection.style.display =
                            "block";
                    }
                )
                .catch(
                    () => {

                        targetSelect.innerHTML =
                            `
                            <option>
                                Error loading formats
                            </option>
                            `;

                        conversionSection.style.display =
                            "block";
                    }
                );
        }
    );
}


/* --------------------------
   Conversion Status
--------------------------- */

if (
    convertForm &&
    statusMessage
) {
    convertForm.addEventListener(
        "submit",
        function () {

            statusMessage.classList.remove(
                "d-none"
            );

            statusMessage.classList.remove(
                "alert-success"
            );

            statusMessage.classList.add(
                "alert-info"
            );

            statusMessage.innerHTML =
                "⏳ Converting file...";
        }
    );
}