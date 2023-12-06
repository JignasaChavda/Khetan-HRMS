// Copyright (c) 2023, Jignasha and contributors
// For license information, please see license.txt
/* eslint-disable */

function stripHtmlTags(html) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    return doc.body.textContent || "";
}
frappe.query_reports["Labour Payment"] = {
    "filters": [
        {
            "fieldname": "month",
            "label": __("Month"),
            "fieldtype": "Select",
            "options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
            "default": frappe.datetime.get_today().split("-")[1],
            "reqd": 1
        },
        {
            "fieldname": "year",
            "label": __("Year"),
            "fieldtype": "Data",
            "default": frappe.datetime.get_today().split("-")[0],
            "reqd": 1
        },
        {
            "fieldname": "employee_type",
            "label": __("Employee Type"),
            "fieldtype": "Link",
            "options": "Employee Type",  // Replace with the actual doctype for Employee Type
            "get_query": function () {
                return {
                    "filters": {
                        "company": "Khetan Udyog"
                    }
                };
            },
            "default": "Plant Labours - SU1"
        }
    ],
   
    "onload": function (report) {
        report.page.add_inner_button(__('Download Report'), function () {
            var filters = report.get_values();
    
            frappe.call({
                method: "khetanhrms.khetan_hrms.report.labour_payment.labour_payment.get_excel_data",
                args: filters,
                callback: function (r) {
                    if (r.message && r.message.data.length > 0) {
                        var data = r.message.data;
                        console.log(data)
                        var columnsToHide = ["Total Minutes", "Total Hour"];
                        var columns = r.message.columns.filter((column, index) => !columnsToHide.includes(column.label)).map(column => column.label);
                        console.log(columns)
                        if (data.length > 0) {
                            const lastRow = data[data.length - 1];
                            lastRow.employee_name = "";
                            lastRow.is_last_row = "Total";
                        }
    
                        var excelContent =
                            '<?xml version="1.0"?>\n' +
                            '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"\n' +
                            ' xmlns:o="urn:schemas-microsoft-com:office:office"\n' +
                            ' xmlns:x="urn:schemas-microsoft-com:office:excel"\n' +
                            ' xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">\n' +
                            ' <Worksheet ss:Name="Labour_Payment_Report">\n' +
                            '  <Table>\n' +
                            '   <Row>\n' +
                            columns.map(column => `<Cell><Data ss:Type="String">${column}</Data></Cell>`).join('\n') +
                            '   </Row>\n' +
                            data.map((row, index) => {
                                return '   <Row>\n' +
                                    Object.values(row).filter((value, colIndex) => !columnsToHide.includes(r.message.columns[colIndex].label)).map((value, colIndex) => {
                                        // if (colIndex === 34) {
                                        //     const columnIndex33 = 33;
                                        //     const columnIndex42 = 42;
                                        //     const columnIndex43 = colIndex;
                                        
                                        //     const columnLabel33 = getExcelColumnLabel(columnIndex33 + 1).toUpperCase();
                                        //     const columnLabel42 = getExcelColumnLabel(columnIndex42 + 1).toUpperCase();
                                        //     const columnLabel43 = getExcelColumnLabel(columnIndex43 + 1).toUpperCase();
                                        
                                        //     const rowNumber = index + 2; // Assuming index is zero-based
                                        
                                        //     // Calculate total payments
                                        //     const totalHoursCell = `${columnLabel33}${rowNumber}`;
                                        //     const rateCell = `${columnLabel42}${rowNumber}`;
                                        //     const totalPaymentsFormula = `=${totalHoursCell} * ${rateCell}`;
                                        
                                        //     // Debugging log
                                        //     console.log(totalPaymentsFormula);
                                        
                                        //     // XML creation
                                        //     const xmlForDebugging = `<Cell ss:Formula="<![CDATA[${totalPaymentsFormula}]]>">
                                        //                                 <Data ss:Type="Number">${totalPaymentsFormula}</Data>
                                        //                                 <Style ss:ID="cellStyleUppercase" ss:Name="Normal"/>
                                        //                              </Cell>`;
                                        
                                        //     // Debugging log
                                        //     console.log(xmlForDebugging);
                                        
                                        //     return xmlForDebugging;
                                        // }
                                        
                                    
                                        
                                        function getExcelColumnLabel(columnIndex) {
                                            let label = '';
                                        
                                            while (columnIndex > 0) {
                                                const remainder = (columnIndex - 1) % 26;
                                                label = String.fromCharCode(65 + remainder) + label;
                                                columnIndex = Math.floor((columnIndex - 1) / 26);
                                            }
                                        
                                            return label;
                                        }
                                        
                                        if (colIndex === 42) { // Assuming column index 42 is the rate column
                                            // Create a new cell for the "Rate" label with the rate value
                                            return `<Cell><Data ss:Type="${typeof value === 'number' ? 'Number' : 'String'}">${stripHtmlTags(value)}</Data></Cell>`;
                                        }
                            
                                        return `<Cell><Data ss:Type="${typeof value === 'number' ? 'Number' : 'String'}">${stripHtmlTags(value)}</Data></Cell>`;
                                    }).join('\n') +
                                    '   </Row>';
                            }).join('\n') +
                            '  </Table>\n' +
                            ' </Worksheet>\n' +
                            '</Workbook>';
    
                        var blob = new Blob([excelContent], { type: 'application/vnd.ms-excel' });
                        var anchor = document.createElement('a');
                        anchor.href = URL.createObjectURL(blob);
                        anchor.target = '_blank';
                        anchor.download = 'Labour_Payment_Report.xls';
    
                        document.body.appendChild(anchor);
                        anchor.click();
                        document.body.removeChild(anchor);
                    }
                }
            });
        });
    }
    
    
};    
