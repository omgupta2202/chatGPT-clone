document.addEventListener("DOMContentLoaded", function () {
    var approveBtn = document.getElementById("hideElement");

    approveBtn.addEventListener("click", function () {
        console.log("data");
        if (typeof jsPDF !== 'undefined') {
            console.log("data");
            var messageText = document.getElementById("live-response").innerText;
            var pdf = new jsPDF();
            pdf.text(messageText, 10, 10);
            pdf.save("approved_document.pdf");
        } else {
            console.error("jsPDF is not defined. Make sure the library is properly loaded.");
        }
    });
});