$(document).ready(function() {
    //Add event listener for the exportButton to call the export function using jQuery
    $('#exportButton').click(function() {
        exportToExcel('deliveries');
    });
});

