import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Grid from "@mui/material/Grid";
import { BarChart } from "@mui/x-charts/BarChart";
import AccessibilityNewIcon from '@mui/icons-material/AccessibilityNew'; import LinearProgress, {
  linearProgressClasses,
} from "@mui/material/LinearProgress";
import { Bar } from "react-chartjs-2";
import { styled } from "@mui/material/styles";
import { Doughnut, Pie } from "react-chartjs-2";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faCalendarCheck,
  faCheckCircle,
  faTimesCircle,
} from "@fortawesome/free-solid-svg-icons";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  LineElement,
  LineController,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  RadialLinearScale,
  Filler,
  DoughnutController,
  PieController,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);




const Item = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
  padding: theme.spacing(2),
  textAlign: "center",
}));

// const BarChart = ({ data }) => {
//   return (
//     <div className="bar-chart">
//       {data.map((item, index) => (
//         <div key={index} className="bar-container">
//           <div
//             className="bar"
//             style={{ width: `${item.value}%`, backgroundColor: item.color }}
//           >
//             <span className="bar-value">{item.value}%</span>{" "}
//             {/* Display value */}
//           </div>
//           <div className="bar-label">{item.label}</div>
//         </div>
//       ))}
//     </div>
//   );
// };

const data = [
  { label: "New", value: 50, color: "#C7253E" },
  { label: "Followup", value: 75, color: "#347928" },
];



// Specility Wise chart



// export const dataset = [
//   { specialty: "Cardiologists", value: 320 },
//   { specialty: "Audiologists", value: 150 },
//   { specialty: "Dentist", value: 450 },
//   { specialty: "ENT Specialist", value: 250 },
//   { specialty: "Gynecologist", value: 500 },
//   { specialty: "Orthopedic Surgeon", value: 600 },
//   { specialty: "Paediatrician", value: 550 },
//   { specialty: "Psychiatrists", value: 180 },
//   { specialty: "Veterinarian", value: 300 },
//   { specialty: "Radiologist", value: 220 },
//   { specialty: "Pulmonologist", value: 190 },
//   { specialty: "Endocrinologist", value: 210 },
//   { specialty: "Oncologist", value: 330 },
//   { specialty: "Neurologist", value: 400 },
// ];
// Department Wise
// const doughnutData = {
//   labels: [
//     //   "Biochemistry",
//     //   "Hematology",
//     //   "Clinical Pathology",
//     //   "Microbiology",
//     //   "Molecular Biology",
//     //   "Virology",
//     //   "Histopathology",
//     //   "Cytopathology",
//   ],
//   datasets: [
//     {
//       data: [500, 400, 300, 200, 150, 100, 50, 30],
//       backgroundColor: [
//         "#FF6384",
//         "#36A2EB",
//         "#FFCE56",
//         "#E7E9ED",
//         "#4BC0C0",
//         "#F7464A",
//         "#FFB6C1",
//         "#C2C2C2",
//       ],
//     },
//   ],
// };

// Formatting function to display values with unit
export const valueFormatter = (value) => `${value} doctors`;

const HrDashboard = () => {


  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const [patientStats, setPatientStats] = useState({
    totalPatients: 0,
    outPatients: 0,
    ipPatients: 0,
    ccuPatients: 0,
    dsPatients: 0,
    labPatients: 0,
    newConsultationPercentage: 0,
    followUpPercentage: 0,
    male_percentage: 0,
    female_percentage: 0,
    bed_occ_per: 0,
    ip_admission: 0,
    ip_discharge: 0,
  });



  // const [maleageStats, setmaleageStats] = useState({
  //   three:0,
  //   four:0,
  //   eleven:0,
  //   twentyone:0,
  //   thirtysix:0,
  //   fifty:0
  // });

  // const [femaleageStats, setfemaleageStats] = useState({
  //   three:0,
  //   four:0,
  //   eleven:0,
  //   twentyone:0,
  //   thirtysix:0,
  //   fifty:0
  // });

  const [opdoctorname, setopdoctorname] = useState([]);
  const [ipdoctorname, setipdoctorname] = useState([]);
  const [agestats, setagestats] = useState([]);

  const xAxisData = opdoctorname.map(doctor => doctor.doctorname);
  const yAxisData = opdoctorname.map(doctor => doctor.PatientCount);

  const xAxisipData = ipdoctorname.map(doctor => doctor.doctorname);
  const yAxisipData = ipdoctorname.map(doctor => doctor.PatientCount);

  const doughnutData = {
    labels: ["OP", "IP", "CCU", "Diagnosis", "Lab"],
    datasets: [
      {
        data: [patientStats.outPatients, patientStats.ipPatients, patientStats.ccuPatients, patientStats.dsPatients, patientStats.labPatients],
        backgroundColor: ["#FFCE56", "#E7E9ED", "#4BC0C0", "#F7464A", "#F7664A"],
      },
    ],
  };

  // AGE CHART

  // const AgeChart = ({ data }) => {
  //   return (
  //     <div className="agev_chart">
  //       {data.map((item, index) => (
  //         <div key={index} className="agev_container">
  //           <div className="agev_label">{item.label}</div>
  //           <div
  //             className="agev"
  //             style={{ width: `${item.value}%`, backgroundColor: item.color }}
  //           >
  //             <span className="agev_value">{item.value}%</span>{" "}
  //             {/* Display value */}
  //           </div>
  //         </div>
  //       ))}
  //     </div>
  //   );
  // };
  const AgeChart = ({ data }) => {
    return (
      <div className="agev_chart">
        {data.map((item, index) => (
          <div key={index} className="agev_container">
            <div className="agev_label">{item.label}</div>

            {/* Male Percentage Bar */}
            <div
              className="agev"
              style={{ width: `${item.male_percentage}%`, backgroundColor: item.male_color }}
            >
              <span className="agev_value">{item.male}</span>
            </div>

            {/* Female Percentage Bar */}
            <div
              className="agev"
              style={{ width: `${item.female_percentage}%`, backgroundColor: item.female_color }}
            >
              <span className="agev_value">{item.female}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  // // const Agedata = [
  // //   agestats.map(age => { label: age.age_ranges;value: age.male_percentage;color: "#4CAF50" })

  // // ];

  // // ,
  // // { label: agestats[1].age_ranges, value: agestats.male_percentage[1], color: "#FF9800" },
  // // { label: agestats[2].age_ranges, value: agestats.male_percentage[2], color: "#2196F3" },
  // // { label: agestats[3].age_ranges, value: agestats.male_percentage[3], color: "#F44336" },
  // // { label: agestats[4].age_ranges, value: agestats.male_percentage[4], color: "#4CAF50" },
  // // { label: agestats[5].age_ranges, value: agestats.male_percentage[5], color: "#F44336" },

  const Agedata1 = agestats.map((stat, index) => ({
    label: stat.age_ranges, // Fallback label in case of index mismatch
    male: stat.male || 0,
    female: stat.female || 0,
    male_percentage: stat.male_percentage || 0,
    female_percentage: stat.female_percentage || 0,
    male_color: "#36a2eb",
    female_color: "#ff6384",
  }));
  // const Agedata2 = {
  //   labels: ["0<3", "4-10", "11-20", "21-35","36-50","50+"],
  //   datasets: [
  //     {
  //       data: [femaleageStats.three, femaleageStats.four,femaleageStats.eleven,femaleageStats.twentyone,femaleageStats.thirtysix,femaleageStats.fifty],
  //       backgroundColor: ["#4CAF50", "#FF9800", "#2196F3", "#F44336","#4CAF50","#F44336"],
  //     },
  //   ],
  // };
  useEffect(() => {
    // Fetch data from the backend when the component mounts
    axios.get(`${UrlLink}Frontoffice/get_patient_stats`) // Replace with your actual API endpoint
      .then((response) => {
        const data = response.data;
        setPatientStats({
          totalPatients: data.totalPatients,
          outPatients: data.outPatients,
          ipPatients: data.ipPatients,
          ccuPatients: data.ccuPatients,
          dsPatients: data.dsPatients,
          labPatients: data.labPatients,
          newConsultationPercentage: data.new_percentage,
          followUpPercentage: data.follow_up_percentage,
          male_percentage: data.male_percentage,
          female_percentage: data.female_percentage,
          bed_occ_per: data.bed_occ_per,
          ip_admission: data.ip_admission,
          ip_discharge: data.ip_discharge
        });
      })
      .catch((error) => {
        console.error("Error fetching patient stats:", error);
      });
  }, [UrlLink]);


  useEffect(() => {
    // Fetch data from the backend when the component mounts
    axios.get(`${UrlLink}Frontoffice/op_doctor_wise`) // Replace with your actual API endpoint
      .then((response) => {
        const data = response.data;
        console.log(data, "data-------");
        setopdoctorname(data);
        console.log(opdoctorname, "kjuhygfgh");
      })
      .catch((error) => {
        console.error("Error fetching patient stats:", error);
      });
  }, [UrlLink]);

  useEffect(() => {
    // Fetch data from the backend when the component mounts
    axios.get(`${UrlLink}Frontoffice/ip_doctor_wise`) // Replace with your actual API endpoint
      .then((response) => {
        const data = response.data;
        console.log(data, "data-------");
        setipdoctorname(data);
        console.log(ipdoctorname, "kjuhygfgh");
      })
      .catch((error) => {
        console.error("Error fetching patient stats:", error);
      });
  }, [UrlLink]);

  //  const xAxisData = ipdoctorname.map(doctor => doctor.doctorname);
  //  console.log(xAxisData,"jhgfhj");



  // useEffect(() => {
  //   // Fetch data from the backend when the component mounts
  //   axios.get(`${UrlLink}Frontoffice/get_age_distribution_for_male`) // Replace with your actual API endpoint
  //     .then((response) => {
  //       const data = response.data;
  //       setmaleageStats({ 
  //         three:data.three,
  //         four:data.four,
  //         eleven:data.eleven,
  //         twentyone:data.twentyone,
  //         thirtysix:data.thirtysix,
  //         fifty:data.fifty
  //       });
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching patient stats:", error);
  //     });
  // }, [UrlLink]);


  // useEffect(() => {
  //   // Fetch data from the backend when the component mounts
  //   axios.get(`${UrlLink}Frontoffice/get_age_distribution_for_female`) // Replace with your actual API endpoint
  //     .then((response) => {
  //       const data = response.data;
  //       setfemaleageStats({
  //         three:data.three,
  //         four:data.four,
  //         eleven:data.eleven,
  //         twentyone:data.twentyone,
  //         thirtysix:data.thirtysix,
  //         fifty:data.fifty
  //       });
  //     })
  //     .catch((error) => {
  //       console.error("Error fetching patient stats:", error);
  //     });
  // }, [UrlLink]);
  useEffect(() => {
    // Fetch data from the backend when the component mounts
    axios.get(`${UrlLink}Frontoffice/get_age_distribution`) // Replace with your actual API endpoint
      .then((response) => {
        const data = response.data;
        if (Array.isArray(data)) {
          console.log(data, "prem-------");
          setagestats(data);
          console.log(agestats, "data------------");
        }
      })
      .catch((error) => {
        console.error("Error fetching patient stats:", error);
      });
  }, [UrlLink]);

  // Gender wise chart
  const pieData2 = {
    labels: ["female", "male"],
    datasets: [
      {
        data: [patientStats.female_percentage, patientStats.male_percentage],
        backgroundColor: ["#ff6384", "#36a2eb"],
      },
    ],
  };
  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: "#fff",
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
    ...theme.applyStyles("dark", {
      backgroundColor: "#1A2027",
    }),
  }));

  const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
    height: 10,
    borderRadius: 5,
    [`&.${linearProgressClasses.colorPrimary}`]: {
      backgroundColor: theme.palette.grey[200],
      ...theme.applyStyles("dark", {
        backgroundColor: theme.palette.grey[800],
      }),
    },
    [`& .${linearProgressClasses.bar}`]: {
      borderRadius: 5,
      backgroundColor: "#1a90ff",
      ...theme.applyStyles("dark", {
        backgroundColor: "#308fe8",
      }),
    },
  }));

  const [leaveAbsenceData, setLeaveAbsenceData] = useState([]);

  useEffect(() => {
    axios
      .get(`YOUR_API_URL`) // Replace with your API endpoint
      .then((response) => {
        setLeaveAbsenceData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching leave and absence data:", error);
      });
  }, []);

  const leaveAbsenceChartData = {
    labels: Array.isArray(leaveAbsenceData) && leaveAbsenceData.map((data) => data.department), // X-axis labels
    datasets: [
      {
        label: "Leaves",
        data: Array.isArray(leaveAbsenceData) && leaveAbsenceData.map((data) => data.leaves), // Y-axis data for leaves
        backgroundColor: "#36a2eb", // Bar color for leaves
      },
      {
        label: "Absences",
        data: Array.isArray(leaveAbsenceData) && leaveAbsenceData.map((data) => data.absences), // Y-axis data for absences
        backgroundColor: "#ff6384", // Bar color for absences
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Leave and Absence by Department",
      },
    },
  };



  return (
    <div className="dashboard_v_con">
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={1} style={{ padding: "5px", justifyContent: 'center' }}>
          <Grid item xs={12} md={6} lg={6}>
            <Item style={{ height: "220px" }}>
              <h6
                style={{
                  textAlign: "center",
                  fontSize: "15px",
                  margin: "5px",
                }}
              >
                Employee Details
              </h6>

              <Box sx={{ flexGrow: 1 }}>
                <Grid container spacing={2} justifyContent="center" alignItems="center" >
                  <Grid item xs={8}>
                    <Item
                      style={{
                        height: "130px",
                        backgroundColor: "rgb(247 156 240 / 74%)",
                        gap: "10px",
                        textAlign: "left",
                        borderRadius: "20px",
                        marginTop: "10px",
                      }}
                    >
                      <Grid container spacing={2}>
                        <Grid item xs={4}>
                          <Item
                            style={{
                              backgroundColor: "transparent",
                              boxShadow: "none",
                              textAlign: "left",
                            }}
                          >
                            <span
                              style={{
                                textAlign: "left",
                                fontSize: "18px",
                                fontWeight: "bold",
                                marginBottom: "16px",
                                display: "block",
                              }}
                            >
                              Total count
                            </span>
                            <AccessibilityNewIcon
                              style={{ fontSize: "50px" }}
                            />
                            <span
                              style={{
                                textAlign: "left",
                                fontSize: "20px",
                                fontWeight: "bold",
                                marginBottom: "8px",
                                display: "block",
                              }}
                            >
                              56
                            </span>
                          </Item>
                        </Grid>
                        <Grid item xs={8}>
                          <Item
                            style={{
                              textAlign: "left",
                              backgroundColor: "transparent",
                              boxShadow: "none",
                            }}
                          >
                            <span
                              style={{
                                display: "block",
                                fontSize: "12px",
                                fontWeight: "bold",
                              }}
                            >
                              Total Hiring
                            </span>
                            <div style={{ display: "flex", gap: "8px" }}>
                              <BorderLinearProgress
                                variant="determinate"
                                value={40}
                                style={{ width: "80%" }}
                              />
                              <span
                                style={{
                                  display: "inline-block",
                                  fontSize: "12px",
                                  color: "#C7253E",
                                }}
                              >
                                40
                              </span>
                            </div>
                            <span
                              style={{
                                display: "block",
                                fontSize: "12px",
                                fontWeight: "bold",
                              }}
                            >
                              Employees Joined This Month
                            </span>
                            <div style={{ display: "flex", gap: "8px" }}>
                              <BorderLinearProgress
                                variant="determinate"
                                value={10}
                                style={{ width: "80%", color: "#347928" }}
                              // color="#347928"
                              />
                              <span
                                style={{
                                  display: "inline-block",
                                  fontSize: "12px",
                                  color: "#347928",
                                }}
                              >
                                10
                              </span>
                            </div>
                            <span
                              style={{
                                display: "block",
                                fontSize: "12px",
                                fontWeight: "bold",
                              }}
                            >
                              Employees Left This Month
                            </span>
                            <div style={{ display: "flex", gap: "8px" }}>
                              <BorderLinearProgress
                                variant="determinate"
                                value={35}
                                style={{ width: "80%" }}
                                barColor="#F87A53"
                              />
                              <span
                                style={{
                                  display: "inline-block",
                                  fontSize: "12px",
                                  color: "#347928",
                                }}
                              >
                                35
                              </span>
                            </div>

                          </Item>
                        </Grid>
                      </Grid>
                    </Item>
                  </Grid>
                </Grid>
              </Box>
            </Item>
          </Grid>


          <Grid item xs={12} md={3} lg={3}>
            <Item style={{ height: "220px" }}>
              <h3 style={{
                textAlign: "center",
                fontSize: "15px",

              }}> Age Wise</h3>
              {" "}
              <AgeChart data={Agedata1} height={100} width={200} />
            </Item>
          </Grid>

          <Grid item xs={12} md={3} lg={3}>
            <Item style={{ height: "220px" }}>
              <div className="patient-details">
                <h3
                  style={{
                    textAlign: "center",
                    fontSize: "15px",
                    marginBottom: '5px',

                  }}
                >Gender Wise</h3>
                <div className="pie-chart">
                  <Pie data={pieData2} />
                </div>
              </div>
            </Item>
          </Grid>






          <Grid item xs={12} md={4} lg={4}>
            <Item style={{ height: "280px" }}>
              <h3
                style={{
                  textAlign: "center",
                  fontSize: "15px",
                  marginBottom: "5px",
                }}
              >Department Wise</h3>
              <div className="customers_p93_Doughnt">
                <Doughnut
                  data={doughnutData}
                  options={{
                    responsive: true, // Chart will resize based on screen size
                    maintainAspectRatio: false, // Allow dynamic resizing based on the defined width/height
                  }}
                  width={220}
                  height={220}
                />
              </div>
            </Item>
          </Grid>

          <Grid item xs={12} md={6} lg={6}>
            <Item style={{ height: "280px" }}>
              <Bar data={leaveAbsenceChartData} options={options}
              // width={220} 
              // height={220} 
              />
            </Item>
          </Grid>


        </Grid>
      </Box>


    </div>
  );
};

export default HrDashboard;
