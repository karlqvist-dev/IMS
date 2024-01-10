$(document).ready(function() {

    // Add an event listener to the checkbox using jQuery
    $('#incoming').change(function() {
        // Get the date input element using jQuery
        var dateInput = $('#date');

        // Disable or enable the date input based on the checkbox state
        dateInput.prop('disabled', this.checked);

        // Clear the date value if the checkbox is checked
        if (this.checked) {
            dateInput.val('');
        }
    });

    //Add even listener for the exportButton to call the export function using jQuery
    $('#exportButton').click(function() {
        exportToExcel('inventory');
    });
});