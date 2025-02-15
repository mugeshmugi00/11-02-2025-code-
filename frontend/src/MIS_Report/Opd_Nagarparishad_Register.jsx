import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';

const Opd_Nagarparishad_Register = () => {
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);

  const [MctsRegisterGet, setMctsRegisterGet] = useState([]);
  const [MctsSearchQuery, setMctsSearchQuery] = useState('');

  const [dateOption, setDateOption] = useState('current');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  

  const MctsColumns = [
    {
        key: "id",
        name: "S.No",
        frozen: true
    },
    {
        key: "Date",
        name: "Date",
        frozen: true
    },
    {
        key: "PatientId",
        name: "Patient Id",
        frozen: true
    },
   
    {
        key: "PatientName",
        name: "Patient Name",
        frozen: true
    },
    
    {
        key: "VisitId",
        name: "VisitId",
    },
    {
        key: "MenstrualLMP",
        name: "LMP",
    },
    
    {
        key: "MenstrualEDD",
        name: "EDD",
    },
    {
        key: "ObstHistory",
        name: "ObstHistory",
    },
    {
        key: "BloodGroup",
        name: "Blood Group",
    },
    {
        key: "AmenorrheaDelivery",
        name: "Amenorrhea",
    },
    {
        key: "BPDelivery",
        name: "BP",
    },
    {
        key: "weightDelivery",
        name: "weight",
    },
    {
        key: "Hb",
        name: "Hb",
    },
    {
        key: "BSLText",
        name: "BSL",
    },
    {
        key: "TT1",
        name: "TT1st",
    },
    {
        key: "TT2",
        name: "TT2nd",
    },
    {
        key: "TT3",
        name: "TT2rd",
    },
    {
        key: "Betnesol",
        name: "Inj.Betnesol",
    },
    {
        key: "FolicAcid",
        name: "FolicAcid",
    },
    {
        key: "Calcium",
        name: "Calcium",
    },
    {
        key: "FTNDLSCS",
        name: "FTND/LSCS",
    },
    {
        key: "FTNDTL",
        name: "FTND/TL",
    },
    {
        key: "PostDelivery",
        name: "PostDelivery",
    },
    {
        key: "VDRLText",
        name: "VDRL",
    },
    {
        key: "OGCTText",
        name: "OGCT",
    },
    {
        key: "MctsNo",
        name: "MctsNo",
    },
    {
        key: "UniqueIdNo",
        name: "UniqueIdNo",
    },

   
    
]



// useEffect(() => {
//   if (MctsSearchQuery.trim() === '') {
//     // Fetch the default 10 rows
//     axios.get(`${UrlLink}MisReports/MisAncCard_Detials_link`, {
//       params: {
//         limit: 10 // Assuming the backend supports a limit parameter to fetch a limited number of rows
//       }
//     })
//     .then((res) => {
//       setMctsRegisterGet(res.data);
//     })
//     .catch((err) => {
//       console.log(err);
//     });
//   } else {
//     // Fetch filtered data based on MctsSearchQuery
//     axios.get(`${UrlLink}MisReports/MisAncCard_Detials_link`, {
//       params: {
//         search: MctsSearchQuery
//       }
//     })
//     .then((res) => {
//       setMctsRegisterGet(res.data);
//     })
//     .catch((err) => {
//       console.log(err);
//     });
//   }
// }, [MctsSearchQuery, UrlLink]);



  
useEffect(() => {
    const params = {};

    if (MctsSearchQuery.trim() !== '') {
      params.search = MctsSearchQuery;
    }

    if (dateOption === 'custom') {
      if (fromDate && toDate) {
        params.fromDate = fromDate;
        params.toDate = toDate;
      } else {
        setMctsRegisterGet([]); // Clear the data if both dates are not provided
        return;
      }
    } else if (dateOption === 'current') {
      const today = new Date().toISOString().split('T')[0]; // Get today's date in YYYY-MM-DD format
      params.fromDate = today;
      params.toDate = today;
    }

    axios.get(`${UrlLink}MisReports/MisAncCard_Detials_link`, { params })
      .then((res) => {
        setMctsRegisterGet(res.data);
      })
      .catch((err) => {
        console.log(err);
      });

  }, [MctsSearchQuery, dateOption, fromDate, toDate, UrlLink]);



  const handleChange = (e) => {
    setMctsSearchQuery(e.target.value);
  };

  const handleDateOptionChange = (e) => {
    setDateOption(e.target.value);
    // Clear the dates if switching back to "Current Date"
    if (e.target.value === 'current') {
      setFromDate('');
      setToDate('');
    }
  };

  const handleFromDateChange = (e) => {
    setFromDate(e.target.value);
  };

  const handleToDateChange = (e) => {
    setToDate(e.target.value);
  };

  return (
    <>
      <div className="Main_container_app">
        <div className="RegisFormcon_1">
          <div className="RegisForm_1">
            <label> Search Here <span>:</span> </label>
            <input
              type="text"
              placeholder='Enter PatientId, PatientName, or CasesheetNo'
              value={MctsSearchQuery}
              onChange={handleChange}
            />
          </div>
          <div className="RegisForm_1">
            <label> Date <span>:</span> </label>
            <select 
                value={dateOption} 
                onChange={handleDateOptionChange}
            >
                <option value="current">Current Date</option>
                <option value="custom">Custom Date</option>
            </select>
            {dateOption === 'custom' && (
                <div className="RegisForm_1">
                <label> From  <span>:</span> </label>

                <input
                    type="date"
                    placeholder="From Date"
                    value={fromDate}
                    onChange={handleFromDateChange}
                />
                <label> To  <span>:</span> </label>

                <input
                    type="date"
                    placeholder="To Date"
                    value={toDate}
                    onChange={handleToDateChange}
                />
                </div>
            )}
          </div>
        </div>
        {MctsRegisterGet.length>0 &&
            <ReactGrid columns={MctsColumns} RowData={MctsRegisterGet} />
          }

       
      </div>
    </>
  );
}

export default Opd_Nagarparishad_Register;
