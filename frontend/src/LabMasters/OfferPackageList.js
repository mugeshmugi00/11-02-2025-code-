import React, { useState, useEffect, useCallback } from "react";
import "./GroupMaster.css";
// import { DataGrid } from '@mui/x-data-grid';
import EditIcon from "@mui/icons-material/Edit";
// import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import Button from "@mui/material/Button";

const OfferPackageList = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [searchQueryCode, setSearchQueryCode] = useState("");
  const [value, setValue] = useState([]);
  const [filteredRows, setFilteredRows] = useState([]);
  // const [selectedRow, setSelectedRow] = useState([]);
  const dispatchValue = useDispatch();

  const urllink = useSelector((state) => state.userRecord?.UrlLink);

  const handleSearchChangeCode = (event) => {
    setSearchQueryCode(event.target.value);
  };

  const fetchget_offer_package_data = useCallback(() => {
    axios
      .get(`${urllink}usercontrol/get_offer_package_data`)
      .then((response) => {
        console.log("response", response.data);
        const data = response.data.map((row) => ({
          id: row.offer_package_id, // Ensure each row has a unique `id`
          ...row,
        }));
        setValue(data);
      })
      .catch((error) => {
        console.error("Error fetching test description data:", error);
      });
  }, [urllink]);

  useEffect(() => {
    fetchget_offer_package_data();
  }, [fetchget_offer_package_data]);

  const handleEditClick = (params) => {
    console.log(params);
    axios
      .get(
        `${urllink}usercontrol/get_packagedata_forupdate?package_code=${params?.package_code}`
      )
      .then((res) => {
        console.log(res);
        dispatchValue({ type: "OfferPackageData", value: res.data });
        navigate("/Home/OfferPackage");
      })
      .catch((err) => {
        console.error(err);
      });
  };

  useEffect(() => {
    const lowerCaseQuery = searchQuery.toLowerCase();
    const filteredData = value.filter((row) => {
      const lowerCasePackageName = row.package_name
        ? row.package_name.toLowerCase()
        : "";
      return lowerCasePackageName.includes(lowerCaseQuery);
    });
    setFilteredRows(filteredData);
  }, [searchQuery, value]);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handlenavigate = () => {
    dispatchValue({ type: "OfferPackageData", value: [] });

    navigate("/Home/OfferPackage");
  };

  const hadleeditstatus = (params) => {
    console.log(params);

    let newstatus;
    if (params.Status === "Active") {
      newstatus = "Inactive";
    } else if (params.Status === "Inactive") {
      newstatus = "Active";
    }

    axios
      .post(
        `${urllink}usercontrol/update_packagestatus?package_code=${params.package_code}&newstatus=${newstatus}`
      )
      .then((res) => {
        console.log(res);
        fetchget_offer_package_data();
      })

      .catch((err) => {
        console.error();
      });
  };

  const offerMastercolumns = [
    {
      key: "id",
      name: "S.No",
      width: 70,
      frozen: true,
    },
    {
      key: "package_name",
      name: "Package Name",
      width: 300,
      frozen: true,
    },
    {
      key: "gender",
      name: "Gender",
    },
    {
      key: "authorized_user",
      name: "Authorized User",
      width: 180,
    },
    {
      key: "cost",
      name: "Package Cost",
    },
    {
      key: "EditAction1",
      name: "Status",
      renderCell: (params) => (
        <Button onClick={() => hadleeditstatus(params.row)}>
          <span style={{ color: "black" }}>{params.row.Status}</span>
        </Button>
      ),
    },
    {
      key: "EditAction",
      name: "Action",
      renderCell: (params) => (
        <p
          onClick={() => handleEditClick(params.row)}
          style={{ width: "130px", textAlign: "center", cursor: "pointer" }}
        >
          <EditIcon />
        </p>
      ),
    },
  ];

  return (
    <div className="appointment">
      <div className="h_head">
        <h4>Profile Master List</h4>
      </div>
      <br />

      <div className="con_1 ">
        <div className="inp_1">
          <label htmlFor="input">
            Package Name <span>:</span>
          </label>
          <input
            type="text"
            value={searchQuery}
            onChange={handleSearchChange}
            placeholder="Enter the GroupName"
          />
        </div>
        <div className="inp_1">
          <label htmlFor="input">
            Package Code <span>:</span>
          </label>
          <input
            type="text"
            value={searchQueryCode}
            onChange={handleSearchChangeCode}
            placeholder="Enter the GroupCode"
          />
        </div>

        <button
          className="RegisterForm_1_btns"
          type="submit"
          onClick={handlenavigate}
        >
          <AddCircleOutlineIcon />
        </button>
      </div>

      <div className="Main_container_app">
        <ReactGrid columns={offerMastercolumns} RowData={filteredRows} />
      </div>
    </div>
  );
};

export default OfferPackageList;
