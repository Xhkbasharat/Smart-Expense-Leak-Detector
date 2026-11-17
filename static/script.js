
document.addEventListener("DOMContentLoaded", function () {

    // Set today's date as the default expense date
    const dateInput = document.querySelector(
        'input[name="expense_date"]'
    );

    if (dateInput && !dateInput.value) {
        dateInput.value = new Date().toISOString().split("T")[0];
    }

    // Confirm before deleting an expense
    const deleteForms = document.querySelectorAll(
        ".expense-item form"
    );

    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const confirmed = confirm(
                "Are you sure you want to delete this expense?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

});
