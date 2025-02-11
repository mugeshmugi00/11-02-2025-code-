import React, { useRef } from "react";
import Barcode from "react-barcode";
import ReactToPrint from "react-to-print";

// Function to generate sample data dynamically
const generateSampleData = (count) => {
  const sampleData = [];
  for (let i = 0; i < count; i++) {
    sampleData.push({
      name: `Person ${i + 1}`,
      age: `${20 + (i % 30)}`, // Random age between 20 and 50
      gender: i % 2 === 0 ? 'M' : 'F', // Alternate gender
      department: ['Radiology', 'Cardiology', 'Neurology', 'Surgery', 'Pediatrics'][i % 5], // Cycle through departments
      barcode: `1234567890${i.toString().padStart(3, '0')}` // Generate a barcode number like 123456789001, 123456789002, etc.
    });
  }
  return sampleData;
};

// CSS for printing (A4 paper size, 3 columns, 8 rows)
const printBarcodeStyles = `
@page {
  size: A4 portrait !important; /* Set paper size to A4 portrait */
  margin: 10mm !important;     /* Set margin around the page */
}
@media print {
  body {
    margin: 0;
    padding: 0;
  }

  .parent_barcode_div_new_hims {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* 3 columns */
    grid-template-rows: repeat(8, auto);    /* 8 rows */
    gap: 5mm;                             /* Space between barcodes */
    width: 100%;
    padding: 0;
    box-sizing: border-box;
  }

  .barcodeRow {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2mm;
  }

  .barcode_image_content_new_hims {
    margin-bottom: 1mm;
    width: 5cm;           /* Set barcode width to 5cm */
    height: 2.5cm;        /* Set barcode height to 2.5cm */
  }

  .barcode_patient_new,
  .barcode_dept_hims {
    font-size: 9pt;  /* Smaller font size for print */
    margin: 1mm 0;  /* Margins between lines of text */
  }

  .Register_btn_con {
    display: none; /* Hide the print button during print */
  }

  .parent_barcode_div_new_hims {
    page-break-inside: avoid;
  }

  /* Force page breaks for rows after the 24th barcode */
  .parent_barcode_div_new_hims > div:nth-child(n+25) {
    page-break-before: always !important;  /* Start a new page after 24 items */
  }
}
`;

const IpBarcodeDetails = () => {
  const componentRef = useRef();

  // Generate 30 sample barcode entries (you can change the count as needed)
  const sampleData = generateSampleData(30);

  const getCurrentDateTime = () => {
    const today = new Date();
    const dd = String(today.getDate()).padStart(2, "0");
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const yy = today.getFullYear().toString().slice(-2);
    const hh = String(today.getHours()).padStart(2, "0");
    const min = String(today.getMinutes()).padStart(2, "0");
    return `${dd}-${mm}-${yy} ${hh}:${min}`;
  };

  return (
    <div className="div_grand_parent_hims">
      <div className="parent_barcode_div_new_hims" ref={componentRef}>
        {sampleData.map((data, index) => (
          <div className="barcodeRow" key={index}>
            <div className="barcode_patient_new">
              <p>{data.name}</p>/<p>{data.age}</p>/<p>{data.gender}</p>
            </div>
            <div className="barcode_image_content_new_hims">
              <Barcode
                value={data.barcode}
                lineColor="Black"
                height={35}
                width={1}
                fontSize={11}
                displayValue={false}
              />
            </div>
            {/* <div className="barcode_dept_hims">
              <p>{getCurrentDateTime()}</p>
            </div> */}
          </div>
        ))}
      </div>
      <ReactToPrint
        trigger={() => (
          <div className="Register_btn_con">
            <button className="RegisterForm_1_btns">Print</button>
          </div>
        )}
        content={() => componentRef.current}
        pageStyle={printBarcodeStyles}
      />
    </div>
  );
};

export default IpBarcodeDetails;
