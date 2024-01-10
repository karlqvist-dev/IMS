//Function to get data from the server and export it as an Excel file. 
//Expects a string parameter for the type of data to be exported (inventory/deliveries).
$.get('/export', { type: sheetType })
    .done(function(data) {
        // Convert returned JSON data to worksheet
        var workSheet = XLSX.utils.json_to_sheet(data);

        // Create a workbook and add the worksheet
        var workBook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workBook, workSheet, 
            sheetType == "inventory" ? "Inventory" :
            sheetType == "deliveries" ? "Delivery" :
            "Sheet1");

        /* Save to file */
        XLSX.writeFile(workBook, sheetType + ".xlsx");
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        console.error("Request failed: " + textStatus + ", " + errorThrown);
    });