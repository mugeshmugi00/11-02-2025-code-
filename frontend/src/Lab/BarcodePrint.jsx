import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useSelector } from "react-redux";
import Barcode from "react-barcode";
import ReactToPrint from "react-to-print";
import "../Lab/barcode.css"

const printBarcodeStyles = `
@page {
  size: 5cm 2.5cm !important; /* Ensure that the size fits the content properly */
  margin: 0 !important; /* Remove margins to prevent extra space */
  padding: 0 !important;
  margin-bottom: 0 !important;
}
@media print {
  .pageBreak {
    page-break-before: always !important; /* Ensure that page breaks are handled */
  }
  .barcode_container_print_data_new {
    margin: 0 !important;
    page-break-inside: avoid !important; /* Avoid breaking a single barcode item into pages */
  }
  .parent_barcode_div_new{
  margin: 0 !important;
  padding : 0 !important;
  gap: 0px !important;
  }
}
`;

export const BarcodePrint = () => {
    // const [value, setValue] = useState(null);
    const componentRef = useRef();
    const [department, setDepartment] = useState([]);
    const urllink = useSelector((state) => state.userRecord?.UrlLink);
    const Printdata = useSelector((state) => state.Frontoffice?.PrintBarcode);
    console.log("Printdata", Printdata);
    const [selectedDepartment, setSelectedDepartment] = useState("All"); // State for selected department
    // const [barcodeimages, setBarcodeImages] = useState([]);




    useEffect(() => {
        if (Printdata && Object.keys(Printdata).length > 0) {
            setDepartment(Printdata?.filterSpecimen)
        }
    }, [Printdata])


    //   useEffect(() => {
    //     axios
    //       .get(
    //         `${urllink}Billing/getfor_barcode_details_print?invoice=${Printdata?.Billing_Invoice}`
    //       )
    //       .then((response) => {
    //         console.log(response);
    //         setDepartment(response.data);
    //       })
    //       .catch((error) => {
    //         console.log(error);
    //       });
    //   }, [Printdata, urllink]);

    // const handleSubmit = async () => {
    //   if (department.length > 0 && Printdata) {
    //     try {
    //       const dataToSend = department.map((test) => ({
    //         invoice_no: Printdata.Billing_Invoice,
    //         barcode_id: test.barcode_id,
    //         patientid: Printdata.Patient_Id,
    //         visitid: Printdata.Visit_Id,
    //         patientname: Printdata.Patient_Name,
    //         test_name: test.Test_Name,
    //         test_code: test.Test_Code,
    //       }));

    //       const formData = new FormData();
    //       dataToSend.forEach((item, index) => {
    //         Object.keys(item).forEach((key) => {
    //           formData.append(`${key}[${index}]`, item[key]);
    //         });
    //       });

    //       const response = await axios.post(
    //         `${urllink}Billing/insertbarcode_id`,
    //         formData
    //       );
    //       console.log("Barcode IDs inserted:", response.data);

    //       const barcodeResponse = await axios.get(
    //         `${urllink}Billing/getbarcodeimage?patientid=${Printdata.Patient_Id}&visitid=${Printdata.Visit_Id}&invoice=${Printdata.Billing_Invoice}`
    //       );
    //       console.log("Barcode images fetched:", barcodeResponse.data);
    //       setBarcodeImages(barcodeResponse.data);
    //     } catch (error) {
    //       console.error("Error inserting or fetching barcode data:", error);
    //     }
    //   }
    // };
    const getCurrentDateTime = () => {
        const today = new Date();

        // Format date
        const dd = String(today.getDate()).padStart(2, "0");
        const mm = String(today.getMonth() + 1).padStart(2, "0"); // January is 0!
        const yyyy = today.getFullYear();
        const yy = yyyy.toString().slice(-2); // Get the last two digits of the year

        // Format time
        const hh = String(today.getHours()).padStart(2, "0");
        const min = String(today.getMinutes()).padStart(2, "0");
        const sec = String(today.getSeconds()).padStart(2, "0");

        return `${dd}-${mm}-${yy}  ${hh}:${min}:${sec}`;
    };

    const currentDateTime = getCurrentDateTime();
    const filteredDepartments =
        selectedDepartment === "All"
            ? department
            : department.filter((department) => department.value === selectedDepartment);

    return (
        <>
            <div className="div_grand_parent">
                <div className="department-select">
                    <label htmlFor="department">Select Department: </label>
                    <select
                        id="department"
                        value={selectedDepartment}
                        onChange={(e) => setSelectedDepartment(e.target.value)}
                    >
                        <option value="All">All</option>
                        {department.map((dept, index) => (
                            <option key={index} value={dept.value}>
                                {dept.value}
                            </option>
                        ))}
                    </select>
                </div>
                <div
                    className="parent_barcode_div_new"
                    id="requestbarcode"
                    ref={componentRef}
                >
                    {filteredDepartments.map((test, index) => (
                        <div className="barcode_container_print_data_new" key={index}>
                            <div className="barcode_patient_new wuduwuff">
                                <p>
                                    {Printdata?.Patient_Name} / {Printdata?.Age}/
                                    {Printdata?.Gender}
                                </p>
                            </div>

                            <Barcode
                                value={Printdata?.BarcodeInvoice}
                                lineColor="Black"
                                height={30}
                                width={1}
                                fontSize={10}
                                displayValue={false}
                            />

                            <div className="barcode_patient_new wuduwuff22 uuuu_ppp">
                                <p>{test.value}</p>
                            </div>
                        </div>
                    ))}

                    {/* {barcodeimages.length === 0 && (
            <div className="Register_btn_con">
              <button
                className="RegisterForm_1_btns"
                onClick={handleSubmit}
                disabled={department.length === 0}
              >
                Submit
              </button>
            </div>
          )} */}
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
        </>
    );
};



