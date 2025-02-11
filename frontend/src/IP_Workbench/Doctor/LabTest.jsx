
import React, { useState, useEffect } from "react";
import axios from "axios";
// import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
// import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid"
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert"
import { useDispatch, useSelector } from "react-redux";
import Button from "@mui/material/Button";
import { FaTrash } from "react-icons/fa";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import ModelContainer from "../../OtherComponent/ModelContainer/ModelContainer";
import PlaylistAddIcon from "@mui/icons-material/PlaylistAdd";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";

const LabTest = () => {
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  console.log(userRecord);
  const toast = useSelector((state) => state.userRecord?.toast);
  const dispatchvalue = useDispatch();
  const IP_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.IP_DoctorWorkbenchNavigation
  );
  console.log(IP_DoctorWorkbenchNavigation);
  const [type, setType] = useState("Addtest");
  console.log(UrlLink);
  const [Department, setDepartment] = useState([]);
  const [MainDepartment, setMainDepartment] = useState([]);
  const [TestNameList, setTestNameList] = useState([]);
  const [SelectedTest, setSelectedTest] = useState([]);
  console.log(SelectedTest);
  const [testType, setTestType] = useState("Individual");
  const [ProfileData, setProfileData] = useState([]);
  const [SelectedGroupTestList, setSelectedGroupTestList] = useState([]);
  const [isViewTests, setisViewTests] = useState(false);
  const [pdfUrl, setPdfUrl] = useState(null);

  const [formData, setFormData] = useState({
    SubDepartment_Code: "",
    SubDepartment_Name: "",
    TestName: "",
    Test_Code: "",
    testType: testType,
    Remarks: "",
    Group_Code: "",
    Group_Name: "",
    GroupList: null,
    Department_Name: "",
    Department_Code: "",
    created_by: userRecord?.username,
    location: userRecord?.location,
  });
  console.log(formData);

  const handlePageChange = (event, newType) => {
    if (newType !== null && newType !== type) {
      setType(newType);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let SubDepartment_Code;
    let Test_Code;
    let Group_Code;
    let GroupList;
    let Department_Code;

    if (name === "SubDepartment_Name") {
      const selectedDepartment = Department?.find(
        (item) => item.SubDepartment_Name === value
      );
      SubDepartment_Code = selectedDepartment?.SubDepartment_Code;
    }
    if (name === "TestName") {
      const selectedTest = TestNameList?.find(
        (item) => item.Test_Name === value
      );
      Test_Code = selectedTest?.Test_Code;
    }
    if (name === "Group_Name") {
      const selectedProfile = ProfileData?.find(
        (item) => item.Group_Name === value
      );
      Group_Code = selectedProfile?.Group_Code;
      GroupList = selectedProfile?.GroupList;
    }
    if (name === "Department_Name") {
      const selectedDepartment = MainDepartment?.find(
        (item) => item.Department_Name === value
      );
      console.log(selectedDepartment);
      Department_Code = selectedDepartment?.Department_Code;
    }
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
      SubDepartment_Code: SubDepartment_Code || prevData.SubDepartment_Code,
      Test_Code: Test_Code || prevData.Test_Code,
      Group_Code: Group_Code || prevData.Group_Code,
      GroupList: GroupList,
      Department_Code: Department_Code || prevData.Department_Code,
    }));
  };

  const handleAddTest = () => {
    console.log(formData);
    console.log(SelectedTest);
    if (formData) {
      const isTestCodeExists = SelectedTest.some(
        (test) => test.Code === formData?.Test_Code
      );

      if (isTestCodeExists) {
        const mess =
          " This Test already exists in Selected Test : " +
          SelectedTest.find((test) => test.Code === formData?.Test_Code).Name;

        const tdata = {
          message: mess,
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
        setFormData((prev) => ({
          ...prev,
          TestName: "",
          Test_Code: "",
        }));
      } else {
        const newvalues = {
          id: SelectedTest.length + 1,
          SubDepartment_Code: formData.SubDepartment_Code,
          SubDepartment_Name: formData?.SubDepartment_Name,
          Name:
            testType === "Individual"
              ? formData?.TestName
              : formData?.Group_Name,
          Code:
            testType === "Individual"
              ? formData?.Test_Code
              : formData?.Group_Code,
          testType: testType,
          GroupList: formData?.GroupList,
          Department_Name: formData?.Department_Name,
          Department_Code: formData?.Department_Code,
        };
        console.log(newvalues);
        setSelectedTest((prev) => [...prev, newvalues]);
        const tdata = {
          message: "Added Successfully",
          type: "success",
        };
        dispatchvalue({ type: "toast", value: tdata });
        setFormData((prev) => ({
          ...prev,
          TestName: "",
          Test_Code: "",
          Remarks: "",
          Group_Code: "",
          Group_Name: "",
          GroupList: null,
        }));
      }
    } else {
      const tdata = {
        message: "Select Test",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };

  const handleDelete = (index) => {
    const updatedTests = SelectedTest.filter(
      (test) => test.Code !== index.Code
    );
    setSelectedTest(updatedTests);
  };

  const handleView = (row) => {
    console.log(row);
    setSelectedGroupTestList(row?.GroupList);
    setisViewTests(true);
  };

  const Testlistcolumns = [
    {
      key: "id",
      name: "S.No",
      width: 70,
      frozen: true,
    },

    {
      key: "testType",
      name: "Test Type",
      frozen: true,
    },
    {
      key: "Name",
      name: "Name",
      frozen: true,
    },
    {
      key: "View",
      name: "View",
      renderCell: (params) =>
        params.row.testType !== "Individual" ? (
          <Button onClick={() => handleView(params.row)}>
            <VisibilityIcon />
          </Button>
        ) : (
          "-"
        ),
    },

    {
      key: "EditAction",
      name: "Action",
      renderCell: (params) => (
        <Button onClick={() => handleDelete(params.row)}>
          <DeleteIcon />
        </Button>
      ),
    },
  ];

  const GroupTestlistcolumns = [
    {
      key: "id",
      name: "S.No",
      width: 70,
      frozen: true,
    },
    {
      key: "test_name",
      name: "Name",
      frozen: true,
    },
  ];

  useEffect(() => {
    axios
      .get(
        `${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=LabSubDepartment`
      )
      .then((response) => {
        const data = response.data;

        setDepartment(data);
      })
      .catch((error) => {
        console.error("Error fetching SubDepartment data:", error);
      });

    axios
      .get(
        `${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=Get_AllTests&gender=${IP_DoctorWorkbenchNavigation.Gender}&Department=${formData?.SubDepartment_Code}`
      )
      .then((response) => {
        setTestNameList(response.data);
      })
      .catch((error) => {
        //.error(error);
      });

    axios
      .get(
        `${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=GroupMaster`
      )
      .then((response) => {
        console.log(response.data);

        setProfileData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching test description data:", error);
      });

    axios
      .get(
        `${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=LabDepartment`
      )
      .then((response) => {
        console.log(response.data);
        const data = response.data.map((row, index) => ({
          id: index + 1,
          ...row,
        }));

        setMainDepartment(data);
      })
      .catch((error) => {
        console.error("Error fetching test description data:", error);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation.Gender, formData?.SubDepartment_Code]);

  const handleSubmitSelectedTest = () => {
    if (SelectedTest) {
      const data = {
        LabQueueId: formData.LabQueueId,
        created_by: userRecord?.username || "",
        Register_Id: IP_DoctorWorkbenchNavigation?.RegistrationId || "",
        RegisterType: "IP",
        SelectedTest: SelectedTest,
        location: formData?.location,
        Remarks: formData?.Remarks,
      };
      // console.log();

      console.log("data", data);
      axios
        .post(`${UrlLink}OP/Lab_Request_Detailslink`, data)
        .then((res) => {
          const resData = res.data;
          const type = Object.keys(resData)[0];
          const message = Object.values(resData)[0];
          const tdata = {
            message: message,
            type: type,
          };
          dispatchvalue({ type: "toast", value: tdata });
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      const tdata = {
        message: "Please Select TestNames Or Favourites Names.",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };

  useEffect(() => {
    const fetchPDF = async () => {
      try {
        const response = await axios.get(
          `${UrlLink}OP/ReportData?Request_Id=${IP_DoctorWorkbenchNavigation?.LabRequestId}`,
          {
            responseType: "arraybuffer", // Use arraybuffer to work with pdf-lib
          }
        );

        // Load the PDF data into pdf-lib
        const pdfDoc = response.data;

        const modifiedPdfUrl = URL.createObjectURL(
          new Blob([pdfDoc], { type: "application/pdf" })
        );

        setPdfUrl(modifiedPdfUrl); // Set the URL to the modified PDF
      } catch (error) {
        console.error("Error fetching or editing PDF:", error);
      }
    };

    fetchPDF();
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);

  return (
    <>
      <div className="for" style={{ width: "100%" }}>
        <br/>
        <div style={{ width: "100%", display: "grid", placeItems: "center" }}>
          <ToggleButtonGroup
            value={type}
            exclusive
            onChange={handlePageChange}
            aria-label="Platform"
          >
            <ToggleButton
              value="Addtest"
              style={{
                height: "30px",
                width: "180px",
                backgroundColor:
                  type === "Addtest"
                    ? "var(--selectbackgroundcolor)"
                    : "inherit",
              }}
              className="togglebutton_container"
            >
              Add Test
            </ToggleButton>
            <ToggleButton
              value="ViewReport"
              style={{
                backgroundColor:
                  type === "ViewReport"
                    ? "var(--selectbackgroundcolor)"
                    : "inherit",
                width: "180px",
                height: "30px",
              }}
              className="togglebutton_container"
            >
              View Report
            </ToggleButton>
          </ToggleButtonGroup>
        </div>

        <br></br>
        <br></br>
        {type === "Addtest" && (
          <>
            <div className="RegisFormcon_1">
              <div className="RegisForm_1">
                <label htmlFor="SubDepartment_Name" className="">
                  Main Department<span className="mandatory"></span>
                  <span>:</span>
                </label>
                <input
                  id="Department_Name"
                  name="Department_Name"
                  required
                  list="departments"
                  onChange={handleInputChange}
                  value={formData.Department_Name}
                  autoComplete="off"
                  disabled={
                    Array.isArray(MainDepartment) && MainDepartment.length === 0
                  }
                  placeholder={
                    Array.isArray(MainDepartment) && MainDepartment.length > 0
                      ? "Select Department"
                      : "No Department Available"
                  }
                />
                <datalist id="departments">
                  {Array.isArray(MainDepartment) &&
                    MainDepartment.map((department) => (
                      <option
                        key={department.Department_Code}
                        value={department.Department_Name}
                      >
                        {department.Department_Name}
                      </option>
                    ))}
                </datalist>
              </div>
              <div className="RegisForm_1">
                <label style={{ fontSize: "20px" }}>
                  Test Type <span>:</span>
                </label>
                <select
                  name="testType"
                  value={testType}
                  autoComplete="off"
                  onChange={(e) => setTestType(e.target.value)}
                >
                  <option value="Individual">Individual</option>
                  <option value="Profiles">Profiles</option>
                </select>
              </div>
              {formData?.Department_Name === "LABOROTORY" && (
                <>
                  {testType === "Individual" && (
                    <>
                      <div className="RegisForm_1">
                        <label htmlFor="SubDepartment_Name" className="">
                          SubDepartment Name<span className="mandatory"></span>
                          <span>:</span>
                        </label>
                        <input
                          id="SubDepartment_Name"
                          name="SubDepartment_Name"
                          required
                          list="subdepartments"
                          placeholder={
                            Array.isArray(Department) && Department.length > 0
                              ? "Select Sub Department"
                              : "No Department Available"
                          }
                          onChange={handleInputChange}
                          value={formData.SubDepartment_Name}
                          autoComplete="off"
                          disabled={
                            Array.isArray(Department) && Department.length === 0
                          }
                        />
                        <datalist id="subdepartments">
                          {Array.isArray(Department) &&
                            Department.map((department) => (
                              <option
                                key={department.SubDepartment_Code}
                                value={department.SubDepartment_Name}
                              >
                                {department.SubDepartment_Name}
                              </option>
                            ))}
                        </datalist>
                      </div>
                      <div className="RegisForm_1">
                        <label className="" htmlFor="TestName">
                          Test Name <span className="mandatory"></span>
                          <span>:</span>
                        </label>

                        <input
                          id="TestName"
                          name="TestName"
                          list="browsers1"
                          onChange={handleInputChange}
                          value={formData?.TestName}
                          required
                          autoComplete="off"
                          placeholder={
                            Array.isArray(TestNameList) &&
                            TestNameList.length > 0
                              ? "Select Test"
                              : "No Test available"
                          }
                          disabled={
                            Array.isArray(TestNameList) &&
                            TestNameList.length === 0
                          }
                        />
                        <datalist id="browsers1">
                          {TestNameList && TestNameList.length > 0 ? (
                            TestNameList.map((item, index) => (
                              <option
                                key={item.Test_Code}
                                value={item.Test_Name}
                              >
                                {item.Test_Name}
                              </option>
                            ))
                          ) : (
                            <option value="" disabled>
                              No tests available
                            </option>
                          )}
                        </datalist>
                      </div>
                    </>
                  )}
                  {testType === "Profiles" && (
                    <div className="RegisForm_1">
                      <label className="" htmlFor="Group_Name">
                        Profile Name <span className="mandatory"></span>
                        <span>:</span>
                      </label>

                      <input
                        id="Group_Name"
                        name="Group_Name"
                        list="browsers1"
                        onChange={handleInputChange}
                        value={formData?.Group_Name}
                        required
                        autoComplete="off"
                        // placeholder="Select Test"
                        placeholder={
                          Array.isArray(ProfileData) && ProfileData.length > 0
                            ? "Select Profile"
                            : "No Profiles available"
                        }
                        disabled={
                          Array.isArray(ProfileData) && ProfileData.length === 0
                        }
                      />
                      {console.log(ProfileData)}
                      <datalist id="browsers1">
                        {ProfileData && ProfileData.length > 0 ? (
                          ProfileData.map((item, index) => (
                            <option
                              key={item.Group_Code}
                              value={item.Group_Name}
                            >
                              {item.Group_Name}
                            </option>
                          ))
                        ) : (
                          <option value="" disabled>
                            No tests available
                          </option>
                        )}
                      </datalist>
                    </div>
                  )}
                  <button onClick={handleAddTest}>
                    <PlaylistAddIcon />
                  </button>
                  {Array.isArray(SelectedTest) && SelectedTest.length > 0 && (
                    <div className="Main_container_app">
                      <ReactGrid
                        columns={Testlistcolumns}
                        RowData={SelectedTest}
                      />
                    </div>
                  )}
                  {Array.isArray(SelectedTest) && SelectedTest.length > 0 && (
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        width: "100%",
                      }}
                    >
                      <div className="RegisForm_1">
                        <label>
                          Remarks<span>:</span>
                        </label>
                        <textarea
                          name="Remarks"
                          value={formData.Remarks}
                          onChange={handleInputChange}
                        />
                      </div>
                    </div>
                  )}
                </>
              )}

              <div className="Main_container_Btn">
                <button onClick={handleSubmitSelectedTest}>save</button>
              </div>
            </div>
          </>
        )}

        {type === "ViewReport" && (
          <>
            {pdfUrl ? (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <iframe
                  style={{
                    height: "400px",
                    width: "800px",
                    backgroundColor: "#f0f0f0",
                    border: "none",
                  }}
                  src={pdfUrl}
                />
              </div>
            ) : (
              <>
                <span>Report is Not Ready</span>
              </>
            )}
          </>
        )}
      </div>

      {isViewTests && (
        <div className="loader" onClick={() => setisViewTests(false)}>
          <div
            className="loader_register_roomshow"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="DivCenter_container">View Test</div>

            <ReactGrid
              columns={GroupTestlistcolumns}
              RowData={SelectedGroupTestList}
            />
            <div className="Main_container_Btn">
              <button onClick={() => setisViewTests(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
      <ModelContainer />

      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
};

export default LabTest;
