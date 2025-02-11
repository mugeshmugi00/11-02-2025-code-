import React, { useEffect, useLayoutEffect, useRef, useState } from 'react'
import debounce from 'lodash.debounce'
import {
  differenceInYears,
  format,
  startOfYear,
  subYears,
  isBefore
} from 'date-fns'
import axios from 'axios'
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert'
import PersonSearchIcon from '@mui/icons-material/PersonSearch'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { IoBedOutline } from 'react-icons/io5'
import profile from '../../Assets/profileimg.jpeg'
import '../../App.css'
import { handleKeyDownText } from '../../OtherComponent/OtherFunctions'
import { handleKeyDownPhoneNo } from '../../OtherComponent/OtherFunctions'
// handleKeyDownTextRegistration
import { handleKeyDownTextRegistration } from '../../OtherComponent/OtherFunctions'
import RoomDetialsSelect from './RoomDetialsSelect'
import Button from '@mui/material/Button'
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid'
import DeleteIcon from '@mui/icons-material/Delete'
import CameraswitchIcon from "@mui/icons-material/Cameraswitch";
import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import Typography from "@mui/material/Typography";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";


const OPVisitEntry = () => {
  const dispatchvalue = useDispatch()
  const navigate = useNavigate()

  const relationships = [
    'Spouse',
    'Father',
    'Mother',
    'Brother',
    'Sister',
    'Father-in-law',
    'Mother-in-law',
    'Grandfather',
    'Grandmother',
    'Son',
    'Daughter',
    'Grandson',
    'Granddaughter',
    'Son-in-law',
    'Daughter-in-law',
    'Uncle',
    'Aunt',
    'Nephew',
    'Niece',
    'Cousin',
    'Step-father',
    'Step-mother',
    'Step-son',
    'Step-daughter'
  ]

  const [AppointmentRegisType, setAppointmentRegisType] = useState('OP')
  const Registeredit = useSelector(state => state.Frontoffice?.Registeredit)

  const PatientDetails = useSelector(state => state.Frontoffice?.PatientDetails)

  const UrlLink = useSelector(state => state.userRecord?.UrlLink)
  const UserData = useSelector(state => state.userRecord?.UserData)
  console.log('Registeredit', Registeredit)
  console.log('PatientDetails', PatientDetails)

  const toast = useSelector(state => state.userRecord?.toast)
  const RegisterRoomShow = useSelector(
    state => state.Frontoffice?.RegisterRoomShow
  )
  const SelectRoomRegister = useSelector(
    state => state.Frontoffice?.SelectRoomRegister
  )
  const [loading, setLoading] = useState(false)
  const [SpecializationData, setSpecializationData] = useState([])
  const [DoctorData, setDoctorData] = useState([])
  const [TokenData, setTokenData] = useState([]);
  const [ReferralDoctorData, setReferralDoctorData] = useState([])
  const [EmployeeData, setEmployeeData] = useState([])
  console.log(DoctorData, 'DoctorData')
  console.log(SpecializationData, 'SpecializationData')

  const [DoctorIdData, setDoctorIdData] = useState([])
  const [FlaggData, setFlaggData] = useState([])
  const [ReligionData, setReligionData] = useState([])
  const [AllDoctorData, setAllDoctorData] = useState([])
  const [InsuranceData, setInsuranceData] = useState([])
  const [ClientData, setClientData] = useState([])
  const [CorporateData, setCorporateData] = useState([])
  const [DonationData, setDonationData] = useState([])
  const [BloodGroupData, setBloodGroupData] = useState([])
  const [TitleNameData, setTitleNameData] = useState([]);
  const [expanded, setExpanded] = useState(false);

  const [category, setcategory] = useState([]);
  const [subcategory, setsubcategory] = useState([]);

  console.log(TitleNameData, 'TitleNameData');


  // Function to format date as MM/DD/YYYY
  const formatDate = date => {
    const d = new Date(date)
    const month = (d.getMonth() + 1).toString().padStart(2, '0')
    const day = d.getDate().toString().padStart(2, '0')
    const year = d.getFullYear()
    return `${year}-${month}-${day}`
  }

  const [patientsearch, setpatientsearch] = useState({
    Search: PatientDetails.PatientId || Registeredit.PatientId || '',
  });
  const [FilterbyPatientId, setFilterbyPatientId] = useState([])

  console.log(FilterbyPatientId, 'FilterbyPatientId');

  const [FilteredFormdata, setFilteredFormdata] = useState(null)
  const [FilteredFormdataAddress, setFilteredFormdataAddress] = useState(null)
  const [FilteredFormdataRoute, setFilteredFormdataRoute] = useState(null)
  const [FilteredFormdataIpDetials, setFilteredFormdataIpDetials] =
    useState(null)
  const [FilteredFormdataIpRoomDetials, setFilteredFormdataIpRoomDetials] =
    useState(null)
  const [FilteredFormdataOPVisitEntry, setFilteredFormdataOPVisitEntry] = useState(null)
  const [FilteredFamilyDetails, setFilteredFamilyDetails] = useState(null)
  const [PatientCatg, setPatientCatg] = useState(null)
  const [FilteredFormdataServices, setFilteredFormdataServices] = useState(null)

  const [errors, setErrors] = useState({})


  const [RegisterData, setRegisterData] = useState({
    // PatientId: '',
    ABHA: PatientDetails.ABHA || Registeredit.ABHA || '',
    Title: PatientDetails.Title || Registeredit.TitleId || '',
    FirstName: PatientDetails.FirstName || Registeredit.FirstName || '',
    MiddleName: PatientDetails.MiddleName || Registeredit.MiddleName || '',
    SurName: PatientDetails.SurName || Registeredit.LastName || '',
    Gender: PatientDetails.Gender || Registeredit.Gender || '',
    MaritalStatus: PatientDetails.MaritalStatus || Registeredit.MaritalStatus || '',
    SpouseName: PatientDetails.SpouseName || Registeredit.SpouseName || '',
    FatherName: PatientDetails.FatherName || Registeredit.FatherName || '',
    DOB: PatientDetails.DOB || Registeredit.DOB || '',
    Age: PatientDetails.Age || Registeredit.Age || '',
    PhoneNo: PatientDetails.PhoneNo || Registeredit.PhoneNumber || '',
    Email: PatientDetails.Email || Registeredit.Email || '',
    BloodGroup: PatientDetails.BloodGroup || Registeredit.BloodGroup || '',
    Occupation: PatientDetails.Occupation || Registeredit.Occupation || '',
    Religion: PatientDetails.Religion || Registeredit.Religion || '',
    Nationality: PatientDetails.Nationality || Registeredit.Nationality || '',
    UHIDType: PatientDetails.UHIDType || Registeredit.UniqueIdType || '',
    UHIDNo: PatientDetails.UHIDNo || Registeredit.UniqueIdNo || '',
    PatientType: PatientDetails.PatientType || Registeredit.PatientType || '',

    Pincode: (PatientDetails.Pincode || PatientDetails.PermanentPincode) || Registeredit.Pincode || '',
    DoorNo: (PatientDetails.DoorNo || PatientDetails.PermanentdoorNo) || Registeredit.DoorNo || '',
    Street: (PatientDetails.Street || PatientDetails.PermanentStreet) || Registeredit.Street || '',
    Area: (PatientDetails.Area || PatientDetails.PermanentArea) || Registeredit.Area || '',
    City: (PatientDetails.City || PatientDetails.PermanentCity) || Registeredit.City || '',
    District: (PatientDetails.District || PatientDetails.PermanentDistrict) || Registeredit.District || '',
    State: (PatientDetails.State || PatientDetails.PermanentState) || Registeredit.State || '',
    Country: (PatientDetails.Country || PatientDetails.PermanentCountry) || Registeredit.Country || '',

  })


  const [OPVisitEntry, setOPVisitEntry] = useState({
    VisitType: '',
    // VisitType: Registeredit.VisitPurpose,
    Speciality: PatientDetails.SpecializationId || Registeredit.SpecializationId || '',
    DoctorName: PatientDetails.DoctorID || Registeredit.DoctorID || '',
    TokenNo: '',
    Complaint: '',
    IsMLC: 'No',
    IsReferral: 'No',

    ReferralSource: '',
    ReferredBy:'',

    NextToKinName: '',
    Relation: '',
    RelativePhoneNo: '',

    PatientCategory: '',

    InsuranceName: '',
    InsuranceType: '',

    ClientName: '',
    ClientType: 'Self',
    ClientEmployeeId: '',
    ClientEmployeeDesignation: '',
    ClientEmployeeRelation: '',

    CorporateName: '',
    CorporateType: '',
    CorporateEmployeeId: '',
    CorporateEmployeeDesignation: '',
    CorporateEmployeeRelation: '',

    EmployeeId: '',
    EmployeeRelation: '',
    EmployeeDesignation: '',

    DoctorId: '',
    DoctorRelation: '',

    DonationType: '',

    // BroughtBy: '',
    // BroughtContactNo: '',
    // ModeOfTransport: '',
    // ConditionOnArrival: '',
    // IsConsciousness: 'Yes',

    // Categoryid: "",
    // Categoryname:"",  
    ServiceCategory: '',
    ServiceSubCategory: '',
    // Subcategorypk:"",
    // SubCategoryid: "",
    // SubCategoryname: "",

  })

  const clearRegisterdata = () => {
    setRegisterData(prev => ({
      ...prev,

      // PatientId: '',
      Title: '',
      FirstName: '',
      MiddleName: '',
      SurName: '',
      Gender: '',
      MaritalStatus: '',
      SpouseName: '',
      FatherName: '',
      AliasName: '',
      DOB: '',
      Age: '',
      PhoneNo: '',
      Email: '',
      BloodGroup: '',
      Occupation: '',
      Religion: '',
      Nationality: '',
      UHIDType: '',
      UHIDNo: '',
      PatientType: '',

      Pincode: '',
      DoorNo: '',
      Street: '',
      Area: '',
      City: '',
      District: '',
      State: '',
      Country: '',
      ABHA: '',
      // Photo : null,
    }))
    setOPVisitEntry((prev) => ({
      ...prev,
      VisitType: '',
      Speciality: '',
      DoctorName: '',
      TokenNo: '',
      Complaint: '',
      IsMLC: '',
      IsReferral: '',

      ReferralSource: '',
      ReferredBy: '',

      NextToKinName: '',
      Relation: '',
      RelativePhoneNo: '',

      PatientCategory: '',
      InsuranceName: '',
      InsuranceType: '',
      ClientName: '',
      ClientType: '',
      ClientEmployeeId: '',
      ClientEmployeeDesignation: '',
      ClientEmployeeRelation: '',
      CorporateName: '',
      CorporateType: '',
      CorporateEmployeeId: '',
      CorporateEmployeeDesignation: '',
      CorporateEmployeeRelation: '',
      EmployeeId: '',
      EmployeeRelation: '',
      DoctorId: '',
      DoctorRelation: '',
      DonationType: '',

      // BroughtBy: '',
      // BroughtContactNo: '',
      // ModeOfTransport: '',
      // ConditionOnArrival: '',
      // IsConsciousness: 'Yes',

      ServiceCategory: '',
      ServiceSubCategory: '',
    }))
    setErrors({})

    setpatientsearch({
      Search: '',
    })

    setAppointmentRegisType('')


  }

  console.log('RegisterData', RegisterData)

  const [ServiceCategoryData, setServiceCategoryData] = useState([])
  const [ServiceSubCategoryData, setServiceSubCategoryData] = useState([])

  const formatLabel = label => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .replace(/^./, str => str.toUpperCase())
    } else {
      return label
    }
  }


  useEffect(() => {

    axios
      .get(`${UrlLink}Masters/Speciality_Detials_link`)
      .then((res) => setSpecializationData(res.data))
      .catch((err) => console.log(err));
  }, [UrlLink]);

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Insert_service_category_master`)
      .then((res) => {
        const ress = res.data
        console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

        setcategory(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink])

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Services_List_by_servicecategory?servicecategory=${OPVisitEntry.Categoryid}`)
      .then((res) => {
        const ress = res.data
        console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

        setsubcategory(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink, OPVisitEntry.Categoryid])







  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          // specializationResponse,
          referralDoctorResponse,
          EmployeeResponse,
          DoctorResponse,
          FlaggData,
          ReligionData,
          AllDoctorData,
          Insurancedata,
          ClientData,
          CorporateData,
          DonationData,
          BloodGroupData,
          TitleNameData,
        ] = await Promise.all([
          // axios.get(`${UrlLink}Masters/Speciality_Detials_link`),
          axios.get(`${UrlLink}Masters/get_referral_doctor_Name_Detials`),
          axios.get(`${UrlLink}Frontoffice/get_Employee_by_PatientCategory`),
          axios.get(`${UrlLink}Frontoffice/get_DoctorId_by_PatientCategory`),
          axios.get(`${UrlLink}Masters/Flagg_color_Detials_link`),
          axios.get(`${UrlLink}Masters/Relegion_Master_link`),
          axios.get(`${UrlLink}Masters/get_All_doctor_Name_Detials`),
          axios.get(`${UrlLink}Masters/get_insurance_data_registration`),
          axios.get(`${UrlLink}Masters/get_client_data_registration`),
          axios.get(`${UrlLink}Masters/get_corporate_data_registration`),
          axios.get(`${UrlLink}Masters/get_donation_data_registration`),
          axios.get(`${UrlLink}Masters/BloodGroup_Master_link`),
          axios.get(`${UrlLink}Masters/Title_Master_link`),
        ])

        // setSpecializationData(
        //   Array.isArray(specializationResponse.data)
        //     ? specializationResponse.data
        //     : []
        // )
        setReferralDoctorData(
          Array.isArray(referralDoctorResponse.data)
            ? referralDoctorResponse.data
            : []
        )
        setEmployeeData(
          Array.isArray(EmployeeResponse.data) ? EmployeeResponse.data : []
        )
        setDoctorIdData(
          Array.isArray(DoctorResponse.data) ? DoctorResponse.data : []
        )
        setFlaggData(Array.isArray(FlaggData.data) ? FlaggData.data : [])
        setReligionData(
          Array.isArray(ReligionData.data) ? ReligionData.data : []
        )
        setAllDoctorData(
          Array.isArray(AllDoctorData.data) ? AllDoctorData.data : []
        )
        setInsuranceData(
          Array.isArray(Insurancedata.data) ? Insurancedata.data : []
        )
        setClientData(Array.isArray(ClientData.data) ? ClientData.data : [])
        setCorporateData(Array.isArray(CorporateData.data) ? CorporateData.data : [])
        setDonationData(
          Array.isArray(DonationData.data) ? DonationData.data : []
        )
        setBloodGroupData(
          Array.isArray(BloodGroupData.data) ? BloodGroupData.data : []
        )
        setTitleNameData(
          Array.isArray(TitleNameData.data) ? TitleNameData.data : []
        )
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }

    fetchData()
  }, [UrlLink])

  useEffect(() => {
    const fetchdat = async () => {
      const postdata = {
        LocationId: UserData?.location,
        Date: formatDate(new Date()),
        Speciality: OPVisitEntry.Speciality || Registeredit.SpecilizationId || '',
        Department: PatientDetails.Department || Registeredit.Department || 'OP',
      }
      console.log('Doctrrrrr', postdata)

      try {
        const response = await axios.get(
          `${UrlLink}Frontoffice/get_available_doctor_by_speciality`,
          { params: postdata }
        )

        setDoctorData(response.data)
        console.log('Doctrrrrr', response.data)
      } catch (error) {
        setDoctorData([])
        console.error('Error fetching referral doctors:', error)
      }
    }

    console.log('jjjjjjj------', OPVisitEntry.Speciality, PatientDetails.Department);

    if (OPVisitEntry.Speciality || Registeredit.SpecilizationId && PatientDetails.Department || Registeredit.Department || 'OP') {
      fetchdat()
    }
  }, [UrlLink,
    UserData.location,
    OPVisitEntry.Speciality,
    PatientDetails.Department,
    Registeredit.SpecilizationId,
    Registeredit.Department
  ])





  // useEffect(() => {
  //   if (Object.keys(Registeredit).length === 0) {
  //     const postdata = {
  //       PatientId: RegisterData.PatientId,
  //       PhoneNo: RegisterData.PhoneNo,
  //       FirstName: RegisterData.FirstName,
  //       UHIDNo: RegisterData.UHIDNo,
  //       MiddleName: RegisterData.MiddleName,
  //       SurName: RegisterData.SurName,
  //       DoctorId: OPVisitEntry.DoctorName,
  //     }
  //     console.log('PosttttDDDD', postdata)

  //     axios
  //       .get(`${UrlLink}Frontoffice/Patients_Management_Filter`, {
  //         params: postdata
  //       })
  //       .then(res => {
  //         const data = res.data
  //         setFilterbyPatientId(data)
  //         axios
  //           .get(`${UrlLink}Frontoffice/get_patient_visit_details`, {
  //             params: {FirstName:Registeredit.FirstName || RegisterData.FirstName,PhoneNo: Registeredit.PhoneNo || RegisterData.PhoneNo,DoctorId: Registeredit.DoctorID || OPVisitEntry.DoctorName,Speciality: OPVisitEntry.Speciality || Registeredit.SpecializationId}
  //           })
  //           .then(res => {
  //             const visit = res.data?.VisitPurpose
  //             console.log('Vissssss', res.data?.VisitPurpose)

  //             setOPVisitEntry(prev => ({
  //               ...prev,
  //               VisitType: visit
  //             }))
  //           })
  //           .catch(err => {
  //             console.log(err)
  //           })
  //       })
  //       .catch(err => {
  //         console.log(err)
  //       })
  //   }
  // }, [
  //   UrlLink,
  //   Registeredit,
  //   RegisterData.PatientId,
  //   RegisterData.PhoneNo,
  //   RegisterData.FirstName,
  //   RegisterData.UHIDNo,
  //   RegisterData.MiddleName,
  //   RegisterData.SurName,
  //   OPVisitEntry.DoctorName,

  // ])


  //   useEffect(() => {
  //     console.log('qqqqqqqqqqqqqqqq');
  //     console.log('wwwwwwwwwwww',Registeredit);

  //     if (Registeredit.length > 0 ) {
  //       const data = {
  //         PatientId: Registeredit.PatientId,
  //         PhoneNo: Registeredit.PhoneNumber,
  //         FirstName: Registeredit.FirstName,
  //         DoctorId: Registeredit.DoctorID, 
  //         Speciality: Registeredit.SpecializationId,
  //       }

  //       console.log(data,'dataaaaaaaaaaaaaaaaa');

  //       console.log('Updated postdata with doctor and speciality:', data);
  //       axios
  //         .get(`${UrlLink}Frontoffice/get_patient_visit_details`, { params: data })
  //         .then((res) => {
  //             const visit = res.data?.VisitPurpose;
  //             console.log(visit, 'visitttttttttt');

  //             setOPVisitEntry((prev) => ({
  //                 ...prev,
  //                 VisitPurpose: visit,
  //             }));

  //             // if (UserData && UserData.location) {
  //             //     setSelectedLocations(UserData.location);
  //             // }
  //         })
  //         .catch((err) => {
  //             console.error("Error fetching visit details:", err);
  //         });
  //     }
  // }, [ UserData,Registeredit]);



  useEffect(() => {
    const isRegistereditEmpty = Object.keys(Registeredit).length === 0;

    if (isRegistereditEmpty) {
      const postdata = {
        PatientId: RegisterData.PatientId,
        PhoneNo: RegisterData.PhoneNo,
        FirstName: RegisterData.FirstName,
        UHIDNo: RegisterData.UHIDNo,
        MiddleName: RegisterData.MiddleName,
        SurName: RegisterData.SurName,
        DoctorId: OPVisitEntry.DoctorName,
      };
      console.log('PosttttDDDD', postdata);

      axios
        .get(`${UrlLink}Frontoffice/Patients_Management_Filter`, {
          params: postdata,
        })
        .then((res) => {
          const data = res.data;
          setFilterbyPatientId(data);

          axios
            .get(`${UrlLink}Frontoffice/get_patient_visit_details`, {
              params: {
                FirstName: Registeredit.FirstName || RegisterData.FirstName,
                PhoneNo: Registeredit.PhoneNo || RegisterData.PhoneNo,
                DoctorId: Registeredit.DoctorID || OPVisitEntry.DoctorName,
                Speciality: OPVisitEntry.Speciality || Registeredit.SpecializationId,
              },
            })
            .then((res) => {
              const visit = res.data?.VisitPurpose;
              console.log('Vissssss', visit);

              setOPVisitEntry((prev) => ({
                ...prev,
                VisitType: visit,
              }));
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      console.log('qqqqqqqqqqqqqqqq');
      console.log('wwwwwwwwwwww', Registeredit);

      const data = {
        PatientId: Registeredit.PatientId,
        PhoneNo: Registeredit.PhoneNumber,
        FirstName: Registeredit.FirstName,
        DoctorId: Registeredit.DoctorID || OPVisitEntry.DoctorName,
        Speciality: Registeredit.SpecializationId || OPVisitEntry.Speciality,
      };

      console.log(data, 'dataaaaaaaaaaaaaaaaa');

      console.log('Updated postdata with doctor and speciality:', data);
      axios
        .get(`${UrlLink}Frontoffice/get_patient_visit_details`, { params: data })
        .then((res) => {
          const visit = res.data?.VisitPurpose;
          console.log(visit, 'visitttttttttt');

          setOPVisitEntry((prev) => ({
            ...prev,
            VisitType: visit,
          }));
        })
        .catch((err) => {
          console.error('Error fetching visit details:', err);
        });
    }
  }, [
    UrlLink,
    Registeredit,
    RegisterData.PatientId,
    RegisterData.PhoneNo,
    RegisterData.FirstName,
    RegisterData.UHIDNo,
    RegisterData.MiddleName,
    RegisterData.SurName,
    OPVisitEntry.DoctorName,
    OPVisitEntry.Speciality,
  ]);


  useEffect(() => {
    const RegistrationId = Registeredit?.RegistrationId;

    console.log(RegistrationId, 'RegistrationId');


    if (RegistrationId) {
      axios.get(`${UrlLink}Frontoffice/get_OP_patient_details`,
        {
          params: { RegistrationId }
        })
        .then((res) => {
          const data = res.data; // Assume the response data contains the patient details

          console.log(data, 'dataaaa');
          console.log(data.TokenNo, 'data.TokenNo');


          if (data) {

            setRegisterData((prev) => ({
              ...prev, // Spread previous state

              // PatientId: data.PatientId || '', // Update PatientId
              PhoneNo: data.PhoneNo || '', // Update PhoneNo
              Title: data.Title || '',
              FirstName: data.FirstName || '',
              MiddleName: data.MiddleName || '',
              SurName: data.SurName || '',
              Gender: data.Gender || '',
              MaritalStatus: data.MaritalStatus || '',
              SpouseName: data.SpouseName || '',
              FatherName: data.FatherName || '',
              // AliasName: data.AliasName || '',
              DOB: data.DOB || '',
              Age: data.Age || '',
              Email: data.Email || '',
              BloodGroup: data.BloodGroup || '',
              Occupation: data.Occupation || '',
              Religion: data.Religion || '',
              Nationality: data.Nationality || '',
              UHIDType: data.UHIDType || '',
              UHIDNo: data.UHIDNo || '',
              DoorNo: data.DoorNo || '',
              PatientType: data.PatientType || '',
              Street: data.Street || '',
              Area: data.Area || '',
              City: data.City || '',
              District: data.District || '',
              State: data.State || '',
              Country: data.Country || '',
              Pincode: data.Pincode || '',
              ABHA: data.ABHA || '',
              // PatientType: data.PatientType || '',
              // Flagging: data.Flagging || '',



              // PatientType: OP?.PatientType || IP?.PatientType || Casuality?.PatientType || Diagnosis?.PatientType || Laboratory?.PatientType|| "",
              // PatientCategory: OP?.PatientCategory || IP?.PatientCategory || Casuality?.PatientCategory || Diagnosis?.PatientCategory || Laboratory?.PatientCategory ||  "",
              // InsuranceName: OP?.InsuranceName || IP?.InsuranceName || Casuality?.InsuranceName || Diagnosis?.InsuranceName || Laboratory?.InsuranceName ||  "",
              // InsuranceType: OP?.InsuranceType || IP?.InsuranceType || Casuality?.InsuranceType || Diagnosis?.InsuranceType || Laboratory?.InsuranceType ||  "",
              // ClientName: OP?.ClientName || IP?.ClientName || Casuality?.ClientName || Diagnosis?.ClientName || Laboratory?.ClientName ||  "",
              // ClientType: OP?.ClientType || IP?.ClientType || Casuality?.ClientType || Diagnosis?.ClientType || Laboratory?.ClientType ||  "",
              // ClientEmployeeId: OP?.ClientEmployeeId || IP?.ClientEmployeeId || Casuality?.ClientEmployeeId || Diagnosis?.ClientEmployeeId || Laboratory?.ClientEmployeeId ||  "",
              // ClientEmployeeDesignation: OP?.ClientEmployeeDesignation || IP?.ClientEmployeeDesignation || Casuality?.ClientEmployeeDesignation || Diagnosis?.ClientEmployeeDesignation || Laboratory?.ClientEmployeeDesignation ||  "",
              // ClientEmployeeRelation: OP?.ClientEmployeeRelation || IP?.ClientEmployeeRelation || Casuality?.ClientEmployeeRelation || Diagnosis?.ClientEmployeeRelation || Laboratory?.ClientEmployeeRelation ||  "",
              // EmployeeId: OP?.EmployeeId || IP?.EmployeeId || Casuality?.EmployeeId || Diagnosis?.EmployeeId || Laboratory?.EmployeeId ||  "",
              // EmployeeRelation: OP?.EmployeeRelation || IP?.EmployeeRelation || Casuality?.EmployeeRelation || Diagnosis?.EmployeeRelation || Laboratory?.EmployeeRelation ||  "",
              // DoctorId: OP?.DoctorId || IP?.DoctorId || Casuality?.DoctorId || Diagnosis?.DoctorId || Laboratory?.DoctorId ||  "",
              // DoctorRelation: OP?.DoctorRelation || IP?.DoctorRelation || Casuality?.DoctorRelation || Diagnosis?.DoctorRelation || Laboratory?.DoctorRelation ||  "",
              // DonationType: OP?.DonationType || IP?.DonationType || Casuality?.DonationType || Diagnosis?.DonationType || Laboratory?.DonationType ||  "",
              // Flagging:OP?.Flagging || IP?.Flagging || Casuality?.Flagging || Diagnosis?.Flagging || Laboratory?.Flagging || "",


            }));

            setOPVisitEntry((prev) => ({
              ...prev,
              VisitType: data.VisitType || '',
              Speciality: data.Speciality || '',
              DoctorName: data.PrimaryDoctor || '',
              TokenNo: data.TokenNo || '',
              Complaint: data.Complaint || '',
              IsMLC: data.IsMLC || '',
              IsReferral: data.IsReferral || '',
              ReferralSource: data.ReferralSource || '',
              ReferredBy: data.ReferredBy || '',
              NextToKinName: data.NextToKinName || '',

              Relation: data.Relation || '',
              RelativePhoneNo: data.RelativePhNo || '',
              PatientCategory: data.PatientCategory || '',
              InsuranceName: data.InsuranceName || '',
              InsuranceType: data.InsuranceType || '',
              ClientName: data.ClientName || '',
              ClientType: data.ClientType || '',
              ClientEmployeeId: data.ClientEmployeeId || '',
              ClientEmployeeDesignation: data.ClientEmployeeDesignation || '',
              ClientEmployeeRelation: data.ClientEmployeeRelation || '',

              CorporateName: data.CorporateName || '',
              CorporateType: data.CorporateType || '',
              CorporateEmployeeId: data.CorporateEmployeeId || '',
              CorporateEmployeeDesignation: data.CorporateEmployeeDesignation || '',
              CorporateEmployeeRelation: data.CorporateEmployeeRelation || '',

              EmployeeId: data.EmployeeId || '',
              EmployeeRelation: data.EmployeeRelation || '',

              DoctorId: data.DoctorId || '',
              DoctorRelation: data.DoctorRelation || '',

              DonationType: data.DonationType || '',
              ServiceCategory: data.ServiceCategory || '',
              ServiceSubCategory: data.ServiceSubCategory || '',

            }));
          }
        })
        .catch((err) => {
          console.error('Error fetching patient data:', err);
        });
    }
  }, [Registeredit, UrlLink]);


  const HandleSearchchange = (e) => {
    const { name, value } = e.target;
    setpatientsearch((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const HandlesearchPatient = (value) => {
    const exist = FilterbyPatientId.find((f) => f.PatientId === value);
    if (!exist) {
      const tdata = {
        message: "Please enter a valid Patient Id",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    } else {
      axios
        .get(
          `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?PatientId=${value}`
        )
        .then((res) => {
          const resss = res.data;

          console.log("paaatttttttttt", res.data);

          if (resss.warn) {
            const tdata = {
              message: resss.warn,
              type: "warn",
            };
            dispatchvalue({ type: "toast", value: tdata });
            return;
          }

          console.log("Patient details:", resss);


          setRegisterData((prev) => ({
            ...prev,
            // PatientId: resss.PatientId,
            ABHA: resss.ABHA,
            Title: resss.Title,
            FirstName: resss.FirstName,
            MiddleName: resss.MiddleName,
            SurName: resss.SurName,
            Gender: resss.Gender,
            MaritalStatus: resss.MaritalStatus,
            SpouseName: resss.SpouseName,
            FatherName: resss.FatherName,
            DOB: resss.DOB,
            Age: resss.Age,
            PhoneNo: resss.PhoneNo,
            Email: resss.Email,
            BloodGroup: resss.BloodGroup,
            Occupation: resss.Occupation,
            Religion: resss.Religion,
            Nationality: resss.Nationality,
            UHIDType: resss.UHIDType,
            UHIDNo: resss.UHIDNo,
            PatientType: resss.PatientType,
            Pincode: resss.Pincode,
            DoorNo: resss.DoorNo,
            Street: resss.Street,
            Area: resss.Area,
            City: resss.City,
            District: resss.District,
            State: resss.State,
            Country: resss.Country,
          }))
        })
        .catch((err) => console.log(err));
    }
  };


  // const HandlesearchPatient1 = value => {
  //   const exist = FilterbyPatientId.find(f => f.PatientId === value)
  //   if (!!!exist) {
  //     const tdata = {
  //       message: 'Please enter a valid Patient Id',
  //       type: 'warn'
  //     }

  //     dispatchvalue({ type: 'toast', value: tdata })
  //   } else {
  //     axios
  //       .get(
  //         `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?PatientId=${value}`
  //       )
  //       .then(res => {
  //         const { PatientProfile, ...resss } = res.data
  //         console.log(resss)
  //         // setpatientPhoto(PatientProfile)
  //         setRegisterData(prev => ({
  //           ...prev,
  //           ...resss
  //         }))
  //       })
  //       .catch(err => {
  //         console.log(err)
  //       })
  //   }
  // }



  const personalDetailsRef = useRef(null)
  const addressRef = useRef(null)
  const opvisitref = useRef(null)
  const referalref = useRef(null)
  const categoryref = useRef(null)
  const kinref = useRef(null)
  const serviceref = useRef(null)



  const handleResize = (ref) => {
    if (ref.current) {
      const { clientWidth } = ref.current;
      const updatedclientWidth = clientWidth - 20;
  
      const items = ref.current.querySelectorAll('.RegisForm_1');
      let totalWidth = 0;
      let currentRowItemsCount = 0;
  
      items.forEach(item => {
        const itemStyles = getComputedStyle(item);
        const itemWidth =
          item.offsetWidth +
          parseFloat(itemStyles.marginLeft) +
          parseFloat(itemStyles.marginRight);
  
        if (totalWidth + itemWidth <= updatedclientWidth) {
          totalWidth += itemWidth;
          currentRowItemsCount++;
        }
      });
  
      const remainingGap = updatedclientWidth - totalWidth;
      let gapBetweenItems = Math.floor(remainingGap / currentRowItemsCount);
  
      // Ensure gap doesn't fluctuate too much
      gapBetweenItems = Math.max(gapBetweenItems, 5); 
  
      const container = ref.current;
  
      if (updatedclientWidth > 800) {
        container.style.justifyContent = 'flex-start';
        container.style.columnGap = `${gapBetweenItems}px`;
      } else {
        container.style.justifyContent = 'center';
        container.style.columnGap = `10px`;
      }
    }
  };
  

  useLayoutEffect(() => {
    const resizeHandler = debounce(() => {
      handleResize(personalDetailsRef)
      handleResize(addressRef)
      handleResize(opvisitref)
      handleResize(referalref)
      handleResize(categoryref)
      handleResize(kinref)
      handleResize(serviceref)
    }, 200)

    const personalResizeObserver = new ResizeObserver(() => handleResize(personalDetailsRef))
    const addressResizeObserver = new ResizeObserver(() => handleResize(addressRef))
    const opvisitResizeObserver = new ResizeObserver(() => handleResize(opvisitref))
    const referalResizeObserver = new ResizeObserver(() => handleResize(referalref))
    const categoryResizeObserver = new ResizeObserver(() => handleResize(categoryref))
    const kinResizeObserver = new ResizeObserver(() => handleResize(kinref))
    const serviceResizeObserver = new ResizeObserver(() => handleResize(serviceref))

    if (personalDetailsRef.current) {
      personalResizeObserver.observe(personalDetailsRef.current)
    }

    if (addressRef.current) {
      addressResizeObserver.observe(addressRef.current)
    }
    if (opvisitref.current) {
      opvisitResizeObserver.observe(opvisitref.current)
    }
    if (referalref.current) {
      referalResizeObserver.observe(referalref.current)
    }
    if (categoryref.current) {
      categoryResizeObserver.observe(categoryref.current)
    }
    if (kinref.current) {
      kinResizeObserver.observe(kinref.current)
    }
    if (serviceref.current) {
      serviceResizeObserver.observe(serviceref.current)
    }

    window.addEventListener('resize', resizeHandler)

    return () => {
      if (personalDetailsRef.current) {
        personalResizeObserver.unobserve(personalDetailsRef.current)
      }
      if (addressRef.current) {
        addressResizeObserver.unobserve(addressRef.current)
      }
      if (opvisitref.current) {
        opvisitResizeObserver.unobserve(opvisitref.current)
      }
      if (referalref.current) {
        referalResizeObserver.observe(referalref.current)
      }
      if (categoryref.current) {
        categoryResizeObserver.unobserve(categoryref.current)
      }
      if (kinref.current) {
        kinResizeObserver.unobserve(kinref.current)
      }
      if (serviceref.current) {
        serviceResizeObserver.unobserve(serviceref.current)
      }

      window.removeEventListener('resize', resizeHandler)
    }
  }, [])

  const handleStopEvent = event => {
    document.body.style.pointerEvents = 'auto'
    event.preventDefault()
    event.stopPropagation()
  }

  const scrollToElement = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        document.body.style.pointerEvents = 'none';
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        setTimeout(() => {
            document.body.style.pointerEvents = 'auto';
            window.removeEventListener('scroll', handleStopEvent);
            window.removeEventListener('click', handleStopEvent);
        }, 500); // Allow time for scroll
    }
};




  const HandleOnchange = async e => {
    const { name, value, pattern } = e.target

    if (name === 'Speciality') {
      setOPVisitEntry(prev => ({
        ...prev,
        [name]: value,
        DoctorName: '',
        TokenNo: ''
      }))
    }
    else if (name === 'ServiceCategory') {

      if (value.includes('-')) {
        const value1 = value.split('-')
        const value2 = value1[0];
        const value3 = value1[1];
        console.log('serrrrrr', value1, value2, value3);
        setOPVisitEntry((prev) => ({
          ...prev,
          [name]: value3
        }))

        if (value2) {
          axios.get(`${UrlLink}Masters/services_Subcategory_details_by_category?ServiceCategory=${value2}`)
            .then((res) => {
              const ress = res.data
              console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

              setServiceSubCategoryData(ress)
            })
            .catch((err) => {
              console.log(err);
            })
        }
      }
    } else if (name === 'ServiceSubCategory') {
      if (value.includes('-')) {
        const value1 = value.split('-')
        const value2 = value1[0];
        const value3 = value1[1];
        const value4 = value1[2];
        setOPVisitEntry((prev) => ({
          ...prev,
          [name]: value4
        }))
      }
    }
    else if (name === 'DoctorName') {
      setOPVisitEntry(prev => ({
        ...prev,
        [name]: value
      }))
    }
    else if (name === 'RelativePhoneNo') {
      if (value.length <= 10) {
        setOPVisitEntry(prev => ({
          ...prev,
          [name]: value
        }))
      }
    }
    else {
      setOPVisitEntry(prev => ({
        ...prev,
        [name]: value
      }))
    }
    const validateField = (value, pattern) => {
      if (!value) {
        return 'Required'
      }
      if (pattern && !new RegExp(pattern).test(value)) {
        return 'Invalid'
      } else {
        return 'Valid'
      }
    }

    const error = validateField(value, pattern)
    console.log(error, 'error')

    setErrors(prevErrors => ({
      ...prevErrors,
      [name]: error
    }))
  }

  useEffect(() => {
    if (PatientDetails.referdoctorid) {
      setOPVisitEntry(prevState => ({
        ...prevState,
        IsReferral: 'Yes',
        ReferredBy: PatientDetails.referdoctorid, // Assign ReferredByDocID if needed
      }));
    }
  }, [PatientDetails.referdoctorid]);


  // useEffect(() => {
  //   let fdata = Object.keys(RegisterData).filter(
  //     p =>
  //       ![

  //         'InsuranceName',
  //         'InsuranceType',
  //         'ClientName',
  //         'ClientType',
  //         'CorporateName',
  //         'CorporateType',
  //         // 'VisitPurpose',
  //         'Specialization',
  //         'DoctorName',
  //         'EmployeeId',
  //         'EmployeeDesignation',
  //         'ClientEmployeeId',
  //         'ClientEmployeeDesignation',
  //         'ClientEmployeeRelation',
  //         'CorporateEmployeeId',
  //         'CorporateEmployeeDesignation',
  //         'CorporateEmployeeRelation',
  //         'EmployeeRelation',
  //         'DoctorId',
  //         'DoctorRelation',
  //         'DonationType',
  //         'ReferralSource',
  //         'ReferredBy',
  //         'InsuranceType',
  //         'Relation',
  //         'RelativePhoneNo',
  //         'TokenNo'
  //       ].includes(p)
  //   )

  //   // if (RegisterData.Title === 'Mrs' && RegisterData.Gender === 'Female') {
  //   //   const categoryIndex = fdata.indexOf('Gender')
  //   //   fdata.splice(categoryIndex + 1, 0, 'AliasName')
  //   // }

  //   if (
  //     RegisterData.MaritalStatus === 'Married' ||
  //     RegisterData.MaritalStatus === 'Widowed'
  //   ) {
  //     const categoryIndex = fdata.indexOf('MaritalStatus')
  //     fdata.splice(categoryIndex + 1, 0, 'SpouseName')
  //   }

  //   if (
  //     RegisterData.MaritalStatus === 'Single' ||
  //     RegisterData.MaritalStatus === 'Divorced'
  //   ) {
  //     const categoryIndex = fdata.indexOf('MaritalStatus')
  //     fdata.splice(categoryIndex + 1, 0, 'FatherName')
  //   }

  //   if (AppointmentRegisType === 'OP') {
  //     const categoryIndex = fdata.indexOf('UniqueIdNo')
  //     fdata.splice(categoryIndex + 1, 0, 'VisitPurpose')
  //     fdata.splice(categoryIndex + 2, 0, 'Specialization', 'DoctorName', 'TokenNo')
  //   }

  //   if (AppointmentRegisType !== 'OP') {
  //     const categoryIndex = fdata.indexOf('UniqueIdNo')
  //     fdata.splice(categoryIndex + 1, 0, 'Specialization', 'DoctorName', 'TokenNo')
  //   }
  //   if (AppointmentRegisType === 'Casuality') {
  //     fdata.unshift('IsConsciousness')
  //   }

  //   setFilteredFormdata(fdata)

  //   let Addressdata = Object.keys(RegisterData).filter(p =>
  //     [
  //       'DoorNo',
  //       'Street',
  //       'Area',
  //       'City',
  //       'District',
  //       'State',
  //       'Country',
  //       'Pincode'
  //     ].includes(p)
  //   )
  //   setFilteredFormdataAddress(Addressdata)

  //   let routedata = Object.keys(RegisterData).filter(p =>
  //     [
  //       'ReferralSource',
  //       'ReferredBy',
  //     ].includes(p)
  //   )
  //   setFilteredFormdataRoute(routedata)

  //   let Ipdetialdata = Object.keys(RegisterData).filter(p =>
  //     [
  //       'AdmissionPurpose',
  //       'DrInchargeAtTimeOfAdmission',
  //       'NextToKinName',
  //       'Relation',
  //       'RelativePhoneNo',
  //       'PersonLiableForBillPayment',
  //       'FamilyHead',
  //       'IpKitGiven'
  //     ].includes(p)
  //   )
  //   if (RegisterData.FamilyHead === 'No') {
  //     const categoryIndex = Ipdetialdata.indexOf('FamilyHead')
  //     Ipdetialdata.splice(categoryIndex + 1, 0, 'FamilyHeadName')
  //   }
  //   setFilteredFormdataIpDetials(Ipdetialdata)
  // }, [
  //   RegisterData,
  //   RegisterData.FamilyHead,
  //   // RegisterData.Title,
  //   RegisterData.Gender,
  //   RegisterData.MaritalStatus,
  //   RegisterData.Specialization,
  //   SpecializationData,
  //   AppointmentRegisType
  // ])



  useEffect(() => {
    let fdata = Object.keys(RegisterData).filter(
      p =>
        ![
          // 'MiddleName',
          // 'SurName',
          // 'BloodGroup',
          // 'Occupation',
          // 'IsConsciousness',
          'AliasName',
          'DoorNo',
          'Street',
          'Area',
          'City',
          'District',
          'State',
          'Country',
          'Pincode',
          'PatientProfile',
          'SpouseName',
          'FatherName',
          'InsuranceName',
          'InsuranceType',
          'ClientName',
          'ClientType',
          'CorporateName',
          'CorporateType',
          // 'VisitType',
          // 'Speciality',
          // 'DoctorName',
          'PatientCategory',
          'EmployeeId',
          'EmployeeDesignation',
          'ClientEmployeeId',
          'ClientEmployeeDesignation',
          'ClientEmployeeRelation',
          'CorporateEmployeeId',
          'CorporateEmployeeDesignation',
          'CorporateEmployeeRelation',
          'EmployeeRelation',
          'DoctorId',
          'DoctorRelation',
          'DonationType',
          // 'ReferralSource',
          // 'ReferredBy',
          // 'RouteNo',
          // 'RouteName',
          // 'TehsilName',
          // 'VillageName',
          // 'AdmissionPurpose',
          // 'DrInchargeAtTimeOfAdmission',
          // 'NextToKinName',
          // 'InsuranceType',
          // 'Relation',
          // 'RelativePhoneNo',
          // 'PersonLiableForBillPayment',
          // 'FamilyHead',
          // 'FamilyHeadName',
          // 'IpKitGiven',
          // 'Building',
          // 'Block',
          // 'Floor',
          // 'WardType',
          // 'RoomType',
          // 'RoomNo',
          // 'BedNo',
          // 'RoomId',
          // 'TokenNo'
        ].includes(p)
    )
    if (
      RegisterData.MaritalStatus === 'Married' ||
      RegisterData.MaritalStatus === 'Widowed'
    ) {
      const categoryIndex = fdata.indexOf('MaritalStatus')
      fdata.splice(categoryIndex + 1, 0, 'SpouseName')
    }

    if (
      RegisterData.MaritalStatus === 'Single' ||
      RegisterData.MaritalStatus === 'Divorced'
    ) {
      const categoryIndex = fdata.indexOf('MaritalStatus')
      fdata.splice(categoryIndex + 1, 0, 'FatherName')
    }
    setFilteredFormdata(fdata)

    let Addressdata = Object.keys(RegisterData).filter(p =>
      [
        'Pincode',
        'DoorNo',
        'Street',
        'Area',
        'City',
        'District',
        'State',
        'Country',
      ].includes(p)
    )
    setFilteredFormdataAddress(Addressdata)

    let routedata = Object.keys(OPVisitEntry).filter(p =>
      [
        'ReferralSource',
        'ReferredBy',
      ].includes(p)
    )
    setFilteredFormdataRoute(routedata)

    let roomdata = Object.keys(OPVisitEntry).filter(p =>
      [
        'Building',
        'Block',
        'Floor',
        'WardType',
        // 'RoomType',
        'RoomNo',
        'BedNo'
      ].includes(p)
    )
    setFilteredFormdataIpRoomDetials(roomdata)


    // let opdata = Object.keys(OPVisitEntry).filter(
    //   p =>
    //     ![

    //       'InsuranceName',
    //       'InsuranceType',
    //       'ClientName',
    //       'ClientType',
    //       'CorporateName',
    //       'CorporateType',
    //       'VisitPurpose',
    //       // 'DoctorName',
    //       // 'VisitType',  ///added on 09-01-2024
    //       'EmployeeId',
    //       'EmployeeDesignation',
    //       'ClientEmployeeId',
    //       'ClientEmployeeDesignation',
    //       'ClientEmployeeRelation',
    //       'CorporateEmployeeId',
    //       'CorporateEmployeeDesignation',
    //       'CorporateEmployeeRelation',
    //       'EmployeeRelation',
    //       'DoctorId',
    //       'DoctorRelation',
    //       'DonationType',
    //       'ReferralSource',
    //       'ReferredBy',

    //       // 'TokenNo',

    //       'ServiceCategory',
    //       'ServiceSubCategory',

    //       'NextToKinName',
    //       'Relation',
    //       'RelativePhoneNo',
    //       'PatientCategory',
    //     ].includes(p)
    // )

    let OpVisit = Object.keys(OPVisitEntry).filter(p => [
      'VisitType',
      'Speciality',
      'DoctorName',
      'TokenNo',
      'Complaint',
      'IsMLC',
      'IsReferral',
    ].includes(p))

    setFilteredFormdataOPVisitEntry(OpVisit)

    let FamilyDetails = Object.keys(OPVisitEntry).filter(p => [
      'NextToKinName',
      'Relation',
      'RelativePhoneNo',
    ].includes(p))
    setFilteredFamilyDetails(FamilyDetails)



    let PatCateg = Object.keys(OPVisitEntry).filter(p =>
      ![
        'InsuranceName', 'InsuranceType',
        'ClientName', 'ClientType', 'ClientEmployeeId', 'ClientEmployeeDesignation', 'ClientEmployeeRelation',
        'EmployeeId', 'EmployeeDesignation', 'EmployeeRelation',
        'DoctorId', 'DoctorRelation',
        'DonationType', 'VisitType', 'Speciality', 'DoctorName',
        'TokenNo', 'Complaint', 'IsMLC', 'IsReferral', 'ReferralSource', 'ReferredBy',
        'NextToKinName', 'Relation', 'RelativePhoneNo',
        'CorporateName', 'CorporateType', 'CorporateEmployeeId', 'CorporateEmployeeDesignation', 'CorporateEmployeeRelation',
        'ServiceCategory', 'ServiceSubCategory',

      ].includes(p)

    )

    if (OPVisitEntry.PatientCategory === 'Insurance') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'InsuranceName', 'InsuranceType')
    }
    if (OPVisitEntry.PatientCategory === 'Client') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'ClientName', 'ClientType')
    }
    if (OPVisitEntry.PatientCategory === 'Corporate') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'CorporateName', 'CorporateType')
    }
    if (
      OPVisitEntry.ClientType === 'Self' &&
      OPVisitEntry.PatientCategory === 'Client'
    ) {
      const categoryIndex = PatCateg.indexOf('ClientType')
      PatCateg.splice(
        categoryIndex + 1,
        0,
        'ClientEmployeeId',
        'ClientEmployeeDesignation'
      )
    }

    if (
      OPVisitEntry.ClientType === 'Family' &&
      OPVisitEntry.PatientCategory === 'Client'
    ) {
      const categoryIndex = PatCateg.indexOf('ClientType')
      PatCateg.splice(
        categoryIndex + 1,
        0,
        'ClientEmployeeId',
        'ClientEmployeeDesignation',
        'ClientEmployeeRelation'
      )
    }
    if (
      OPVisitEntry.CorporateType === 'Company' &&
      OPVisitEntry.PatientCategory === 'Corporate'
    ) {
      const categoryIndex = PatCateg.indexOf('CorporateType')
      PatCateg.splice(
        categoryIndex + 1,
        0,
        'CorporateEmployeeId',
        'CorporateEmployeeDesignation'
      )
    }

    if (
      OPVisitEntry.CorporateType === 'Individual' &&
      OPVisitEntry.PatientCategory === 'Corporate'
    ) {
      const categoryIndex = PatCateg.indexOf('CorporateType')
      PatCateg.splice(
        categoryIndex + 1,
        0,
        'CorporateEmployeeId',
        'CorporateEmployeeDesignation',
        'CorporateEmployeeRelation'
      )
    }
    if (OPVisitEntry.PatientCategory === 'Employee') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'EmployeeId')
    }
    if (OPVisitEntry.PatientCategory === 'EmployeeRelation') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'EmployeeId', 'EmployeeRelation')
    }
    if (OPVisitEntry.PatientCategory === 'Doctor') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'DoctorId')
    }
    if (OPVisitEntry.PatientCategory === 'DoctorRelation') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'DoctorId', 'DoctorRelation')
    }
    if (OPVisitEntry.PatientCategory === 'Donation') {
      const categoryIndex = PatCateg.indexOf('PatientCategory')
      PatCateg.splice(categoryIndex + 1, 0, 'DonationType')
    }

    setPatientCatg(PatCateg);


    let OPServicesdata = Object.keys(OPVisitEntry).filter(p => [
      'ServiceCategory',
      'ServiceSubCategory',
    ].includes(p))
    setFilteredFormdataServices(OPServicesdata)

    let Ipdetialdata = Object.keys(RegisterData).filter(p =>
      [
        'AdmissionPurpose',
        'DrInchargeAtTimeOfAdmission',
        'NextToKinName',
        'Relation',
        'RelativePhoneNo',
        'PersonLiableForBillPayment',
        'FamilyHead',
        'IpKitGiven'
      ].includes(p)
    )
    if (RegisterData.FamilyHead === 'No') {
      const categoryIndex = Ipdetialdata.indexOf('FamilyHead')
      Ipdetialdata.splice(categoryIndex + 1, 0, 'FamilyHeadName')
    }
    setFilteredFormdataIpDetials(Ipdetialdata)
  }, [
    OPVisitEntry,
    SpecializationData,
    AppointmentRegisType,
  ])


  useEffect(() => {
    axios.get(`${UrlLink}Masters/services_Group_list_details`)
      .then((res) => {
        const ress = res.data
        console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

        setServiceCategoryData(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink]);



  const handlesubmit = () => {
    setLoading(true);
    scrollToElement("RegisFormcon_11");

    // Define explicitly required fields
    const requiredFields = ["Title", "FirstName", "Gender", "PhoneNo"];

    let missingFields = [];

    // Identify missing fields from the explicitly required list
    requiredFields.forEach((field) => {
      if (!RegisterData[field]) {
        missingFields.push(formatLabel(field)); // Assuming formatLabel formats field names for display
      }
    });

    if (!RegisterData.DOB && !RegisterData.Age) {
      missingFields.push("DOB or Age");
    }

    console.log("missingFields", missingFields);

    // If any required fields are missing, show a warning
    if (missingFields.length > 0) {
      setLoading(false);
      const tdata = {
        message: `Please fill out the required fields: ${missingFields.join(", ")}`,
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    } else {
      const exist = Object.keys(errors).filter((p) => errors[p] === "Invalid");
      if (exist.length > 0) {
        setLoading(false);
        const tdata = {
          message: `please fill the field required pattern  :  ${exist.join(",")}`,
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      } else {
        const submitdata = {
          ...OPVisitEntry,
          // PatientPhoto: patientPhoto,
          Created_by: UserData?.username,
          RegisterType: AppointmentRegisType,
          PatientId: patientsearch.Search,
          RegistrationId: Registeredit?.RegistrationId || '',
          // RegisterId: Registeredit?.conversion
          //   ? null
          //   : Registeredit?.RegistrationId,
          // optoip_id: Registeredit?.conversion
          //   ? Registeredit?.RegistrationId
          //   : null,
          // Location: UserData?.location,
          // apptoreg: Registeredit?.appconversion ? Registeredit?.id : "",
        };
        console.log("datatosend", submitdata);

        axios
          .post(`${UrlLink}Frontoffice/Patient_OP_Registration`, submitdata)
          .then((res) => {
            setLoading(false);
            console.log(res.data);
            const resres = res.data;
            let typp = Object.keys(resres)[0];
            let mess = Object.values(resres)[0];
            const tdata = {
              message: mess,
              type: typp,
            };
            dispatchvalue({ type: "toast", value: tdata });
            clearRegisterdata();

            dispatchvalue({ type: "Registeredit", value: {} });

            dispatchvalue({ type: "PatientDetails", value: {} });

            dispatchvalue({ type: "HrFolder", value: "PatientRegisterList" });

            navigate("/Home/FrontOfficeFolder");
            dispatchvalue({ type: "setPreviousFolder", value: null });
            dispatchvalue({ type: "showMenu", value: true });


          })
          .catch((err) => {
            setLoading(false);
            console.log(err);
          });
      }
    }
  };


  // #-------------Final working code ------------------


  useEffect(() => {
    const fetchtoken = async () => {
      if (OPVisitEntry.TokenNo) return;
      const postdata = {
        LocationId: UserData?.location,
        Date: formatDate(new Date()),
        Speciality: OPVisitEntry.Speciality
      }
      console.log('token', postdata)

      try {
        const response = await axios.get(
          `${UrlLink}Frontoffice/get_available_tokenno_by_speciality`,
          { params: postdata }
        )

        // Set the token data to state
        setTokenData(response?.data?.next_available_token_no);
        console.log('Tokendata', response?.data)

        // Assuming response.data contains next_available_token_no
        if (response?.data) {
          const tokenno = response?.data?.next_available_token_no || 0
          setOPVisitEntry(prevData => {
            const updatedData = {
              ...prevData,
              TokenNo: tokenno,
            };
            console.log('Updated OPVisitEntry', updatedData);
            return updatedData;
          });
        }
        console.log('OPVisitEntryyyy', OPVisitEntry);


      } catch (error) {
        setTokenData([])
        console.error('Errortoken no:', error)
      }
    }

    if (OPVisitEntry.Speciality) {
      fetchtoken()
    }
  }, [UrlLink, UserData.location, OPVisitEntry.Speciality, TokenData])



  




  // useEffect(() => {
  //   if (Registeredit && Object.keys(Registeredit).length !== 0) {
  //     if (Registeredit?.appconversion) {
  //       axios
  //         .get(
  //           `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?FirstName=${Registeredit?.FirstName}&PhoneNumber=${Registeredit?.PhoneNumber}`
  //         )
  //         .then(res => {
  //           if (res.data) {
  //             setRegisterData(prev => ({
  //               ...prev,
  //               Title: Registeredit?.TitleId,
  //               FirstName: Registeredit?.FirstName,
  //               MiddleName: Registeredit?.MiddleName,
  //               SurName: Registeredit?.LastName,
  //               PhoneNo: Registeredit?.PhoneNumber,
  //               Email: Registeredit?.Email,
  //             }))
  //             setOPVisitEntry(prev => ({
  //               ...prev,
  //               DoctorName: Registeredit?.DoctorID,
  //               Speciality: Registeredit?.SpecializationId,
  //               VisitType: Registeredit?.VisitType
  //             }))
  //           }
  //         })
  //     }
  //   }
  // }, [UrlLink, Registeredit])


  // useEffect(() => {
  //   if (UserData && UserData.location && selectedDoctor && TodayDate) {
  //     axios
  //       .get(`${UrlLink}Frontoffice/calender_modal_display_data_by_day`, {
  //         params: {
  //           DoctorId: selectedDoctor,
  //           LocationId: UserData.location,
  //           Date: TodayDate,
  //         },
  //       })
  //       .then((response) => {
  //         const res = response.data;
  //         setDoctorDayData(res);
  //       })
  //       .catch((err) => {
  //         console.error("Error fetching filtered data:", err);
  //       });
  //   }
  // }, [UrlLink, UserData, UserData.location, selectedDoctor,TodayDate]);

  // useEffect(() => {
  //   if (Registeredit && Object.keys(Registeredit).length !== 0) {
  //     setAppointmentRegisType(Registeredit?.Type)
  //     if (Registeredit?.conversion) {
  //       axios
  //         .get(
  //           `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?PatientId=${Registeredit?.PatientId}`
  //         )
  //         .then(res => {
  //           const { PatientProfile, ...resss } = res.data
  //           console.log(resss)
  //           setpatientPhoto(PatientProfile)
  //           setRegisterData(prev => ({
  //             ...prev,
  //             ...resss
  //           }))
  //         })
  //         .catch(err => {
  //           console.log(err)
  //         })
  //     } else if (Registeredit?.appconversion) {
  //       axios
  //         .get(
  //           `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?FirstName=${Registeredit?.FirstName}&PhoneNumber=${Registeredit?.PhoneNumber}`
  //         )
  //         .then(res => {
  //           if (res.data?.warn) {
  //             setRegisterData(prev => ({
  //               ...prev,
  //               DoctorName: Registeredit?.DoctorID,
  //               Speciality: Registeredit?.SpecializationId,
  //               Title: Registeredit?.Title,
  //               FirstName: Registeredit?.FirstName,
  //               MiddleName: Registeredit?.MiddleName,
  //               SurName: Registeredit?.LastName,
  //               PhoneNo: Registeredit?.PhoneNumber,
  //               Email: Registeredit?.Email,
  //               VisitType: Registeredit?.VisitType
  //             }))
  //           } else {
  //             const { PatientProfile, ...resss } = res.data

  //             console.log(resss)
  //             setpatientPhoto(PatientProfile)

  //             setRegisterData(prev => ({
  //               ...prev,
  //               ...resss,
  //               DoctorName: Registeredit?.DoctorID,
  //               Speciality: Registeredit?.SpecializationId,
  //               VisitType: Registeredit?.VisitType
  //             }))
  //           }
  //         })
  //         .catch(err => {
  //           console.log(err)
  //         })
  //     } else {
  //       axios
  //         .get(`${UrlLink}Frontoffice/get_Registration_edit_details`, {
  //           params: {
  //             RegistrationId: Registeredit?.RegistrationId || '',
  //             RegistrationType: Registeredit?.Type || ''
  //           }
  //         })
  //         .then(response => {
  //           const resdata = response.data
  //           const {
  //             BuildingName,
  //             BlockName,
  //             FloorName,
  //             WardTypeName,
  //             RoomTypeName,
  //             PatientProfile,
  //             ...res
  //           } = resdata
  //           setRoomdeditalsShow({
  //             Building: BuildingName,
  //             Block: BlockName,
  //             Floor: FloorName,
  //             WardType: WardTypeName,
  //             RoomType: RoomTypeName,
  //             RoomNo: res.RoomNo,
  //             BedNo: res.BedNo,
  //             RoomId: res.RoomId
  //           })
  //           setpatientPhoto(PatientProfile)
  //           setRegisterData(prev => ({
  //             ...prev,
  //             IsConsciousness: res?.IsConsciousness || 'Yes',
  //             PatientId: res.PatientId || '',
  //             PhoneNo: res.PhoneNo || '',
  //             Title: res.Title || '',
  //             FirstName: res.FirstName || '',
  //             MiddleName: res.MiddleName || '',
  //             SurName: res.SurName || '',
  //             Gender: res.Gender || '',
  //             MaritalStatus: res.MaritalStatus || '',
  //             SpouseName: res.SpouseName || '',
  //             FatherName: res.FatherName || '',
  //             AliasName: res.AliasName || '',
  //             DOB: res.DOB || '',
  //             Age: res.Age || '',
  //             Email: res.Email || '',
  //             BloodGroup: res.BloodGroup || '',
  //             Occupation: res.Occupation || '',
  //             Religion: res.Religion || '',
  //             Nationality: res.Nationality || '',
  //             UHIDType: res.UHIDType || '',
  //             UHIDNo: res.UniqueIdNo || '',

  //             VisitType: res.VisitType || '',

  //             Speciality: res.Speciality || '',
  //             DoctorName: res.DoctorName || '',
  //             Complaint: res.Complaint || '',
  //             PatientType: res.PatientType || 'General',
  //             PatientCategory: res.PatientCategory || 'General',
  //             InsuranceName: res.InsuranceName || '',
  //             InsuranceType: res.InsuranceType || '',
  //             ClientName: res.ClientName || '',
  //             ClientType: res.ClientType || '',
  //             ClientEmployeeId: res.ClientEmployeeId || '',
  //             ClientEmployeeDesignation: res.ClientEmployeeDesignation || '',
  //             ClientEmployeeRelation: res.ClientEmployeeRelation || '',
  //             CorporateName: res.CorporateName || '',
  //             CorporateType: res.CorporateType || '',
  //             CorporateEmployeeId: res.CorporateEmployeeId || '',
  //             CorporateEmployeeDesignation:
  //               res.CorporateEmployeeDesignation || '',
  //             CorporateEmployeeRelation: res.CorporateEmployeeRelation || '',
  //             EmployeeId: res.EmployeeId || '',
  //             EmployeeRelation: res.EmployeeRelation || '',
  //             DoctorId: res.DoctorId || '',
  //             DoctorRelation: res.DoctorRelation || '',
  //             DonationType: res.DonationType || '',
  //             IsMLC: res.IsMLC || '',
  //             Flagging: res.Flagging || 1,
  //             IsReferral: res.IsReferal || '',

  //             ReferralSource: res.ReferralSource || '',
  //             ReferredBy: res.ReferredBy || '',
  //             RouteNo: res.RouteNo || '',
  //             RouteName: res.RouteName || '',
  //             TehsilName: res.TehsilName || '',
  //             VillageName: res.VillageName || '',

  //             DrInchargeAtTimeOfAdmission:
  //               res.DrInchargeAtTimeOfAdmission || '',
  //             NextToKinName: res.NextToKinName || '',
  //             Relation: res.Relation || '',
  //             RelativePhoneNo: res.RelativePhoneNo || '',
  //             PersonLiableForBillPayment: res.PersonLiableForBillPayment || '',
  //             FamilyHead: res.FamilyHead || '',
  //             FamilyHeadName: res.FamilyHeadName || '',
  //             IpKitGiven: res.IpKitGiven || '',

  //             DoorNo: res.DoorNo || '',
  //             Street: res.Street || '',
  //             Area: res.Area || '',
  //             City: res.City || '',
  //             District: res.District || '',
  //             State: res.State || '',
  //             Country: res.Country || '',
  //             Pincode: res.Pincode || '',

  //             Building: res.Building || '',
  //             Block: res.Block || '',
  //             Floor: res.Floor || '',
  //             WardType: res.WardType || '',
  //             RoomType: res.RoomType || '',
  //             RoomNo: res.RoomNo || '',
  //             BedNo: res.BedNo || '',
  //             RoomId: res.RoomId || ''
  //           }))
  //         })
  //         .catch(e => {
  //           console.error('Error fetching patient appointment details:', e)
  //         })
  //     }
  //   } else {
  //     clearRegisterdata()
  //   }
  // }, [Registeredit, UrlLink])
  // useEffect(() => {
  //   if (Object.keys(SelectRoomRegister).length !== 0) {
  //     setRegisterData(prev => ({
  //       ...prev,
  //       Building: SelectRoomRegister.BuildingId,
  //       Block: SelectRoomRegister.BlockId,
  //       Floor: SelectRoomRegister.FloorId,
  //       WardType: SelectRoomRegister.WardId,
  //       RoomType: SelectRoomRegister.RoomId,
  //       RoomNo: SelectRoomRegister.RoomNo,
  //       BedNo: SelectRoomRegister.BedNo,
  //       RoomId: SelectRoomRegister.id
  //     }))
  //     setRoomdeditalsShow({
  //       Building: SelectRoomRegister.BuildingName,
  //       Block: SelectRoomRegister.BlockName,
  //       Floor: SelectRoomRegister.FloorName,
  //       WardType: SelectRoomRegister.WardName,
  //       RoomType: SelectRoomRegister.RoomName,
  //       RoomNo: SelectRoomRegister.RoomNo,
  //       BedNo: SelectRoomRegister.BedNo,
  //       RoomId: SelectRoomRegister.RoomId
  //     })
  //   } else {
  //   }
  // }, [SelectRoomRegister])

  return (
    <>
      <div className='Main_container_app'>
        <h3>OP Visit Entry</h3>

        <br />
        <div className='RegisForm_12' >
            <label>
              Patient Search <span>:</span>
            </label>
            <div className="Search_patient_icons">
              <input
                type="text"
                onKeyDown={
                  patientsearch === "FirstName"
                    ? (e) => HandlesearchPatient(patientsearch.Search)
                    : null
                }
                list="Search_iddd"
                autoComplete="off"
                name="Search"
                pattern={
                  patientsearch === "PhoneNumber" ? "\\d{10}" : "[A-Za-z]+"
                }
                className={
                  errors["Search"] === "Invalid"
                    ? "invalid"
                    : errors["Search"] === "Valid"
                      ? "valid"
                      : ""
                }
                value={patientsearch.Search}
                onChange={HandleSearchchange}
              />
              <datalist id="Search_iddd">
                {FilterbyPatientId.map((row, indx) => (
                  <option key={indx} value={row.PatientId}>
                    {` Ph:${row.PhoneNo} | ${row.FirstName} ${row.MiddleName} ${row.SurName} | ${row.UHIDNo}`}
                  </option>
                ))}
              </datalist>
              {patientsearch.Search && (
                <span
                  onClick={() => HandlesearchPatient(patientsearch.Search)}
                >
                  <PersonSearchIcon />
                </span>
              )}
            </div>
          </div>
          <br />


        <div className="DivCenter_container">Personal Details</div>
        <br />

        <div className='RegisFormcon' id='RegisFormcon_1' ref={personalDetailsRef}>

          <div className='RegisForm_1' >
            <label htmlFor={AppointmentRegisType}>Visit Purpose <span>:</span></label>
            <select
              id={AppointmentRegisType}
              value={AppointmentRegisType}
              onChange={e => { setAppointmentRegisType(e.target.value) }}

            >
              <option value='OP'>Out-Patient</option>
              <option value='DayCare'>DayCare</option>
              <option value='Services'>Services</option>
              <option value='MHC'>MHC</option>
            </select>
          </div>

         

          {FilteredFormdata &&
            FilteredFormdata.filter((p) => p !== 'Photo').map((field, index) => (
              <div className='RegisForm_1' key={index}>
                <label htmlFor={`${field}_${index}`}>
                  {/* <div className=''> */}
                  {field === 'Title' || field === 'Gender' || field === 'PhoneNo' || field === 'FirstName' ? (
                    <>
                      {field === 'Title' && 'Title'}
                      {field === 'Gender' && 'Gender'}
                      {/* {field === 'UHIDType' && 'UHID Type'} */}
                      {field === 'PhoneNo' && 'Phone No'}
                      {field === 'FirstName' && 'First Name'}

                      <span className="requirreg12">*</span> {/* Single star for required fields */}
                    </>
                  ) : field === 'DOB' || field === 'Age' ? (
                    <>
                      {field === 'DOB' && 'DOB'}
                      {field === 'Age' && 'Age'}

                      <span className="requirreg12">**</span> {/* Two stars for DOB and Age */}
                    </>
                  ) : field === 'ANCNumber' ? (
                    'ANC Number'
                  ) : field === 'MCTSNo' ? (
                    'MCTS No'
                  ) : (
                    formatLabel(field)
                  )}
                  {/* </div> */}
                  <span>:</span>
                </label>


                {[
                  // 'VisitPurpose',
                  'Title',
                  'Gender',
                  'MaritalStatus',
                  'BloodGroup',
                  'Religion',
                  'Nationality',
                  'UHIDType',
                  // 'Speciality',
                  // 'DoctorName',
                  'PatientType',
                  // 'PatientCategory',
                  // 'ColorFlag',
                  // 'ReferralSource',


                  // 'Flagging',
                  // 'InsuranceName',
                  // 'DonationType',
                  // 'InsuranceType',
                  // 'ClientName',
                  // 'ClientEmployeeRelation',
                  // 'EmployeeRelation',
                  // 'EmployeeId',
                  // 'EmployeeRelation',
                  // 'Relation',
                  // 'DoctorId',
                  // 'DoctorRelation',
                  // 'CorporateName',
                  // 'CorporateEmployeeRelation'
                ].includes(field) ? (
                  <select
                    id={`${field}_${index}`}
                    name={field}
                    value={RegisterData[field]}
                    onChange={HandleOnchange}
                    disabled
                  >
                    <option value=''>Select</option>
                    {field === 'Title' &&
                      TitleNameData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Title}
                        </option>
                      ))}
                    {field === 'Gender' &&
                      ['Male', 'Female', 'TransGender'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}
                    {field === 'MaritalStatus' &&
                      ['Single', 'Married', 'Divorced', 'Widowed'].map(
                        (row, indx) => (
                          <option key={indx} value={row}>
                            {row}
                          </option>
                        )
                      )}
                    {field === 'BloodGroup' &&
                      BloodGroupData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.BloodGroup}
                        </option>
                      ))}
                    {field === 'Religion' &&
                      ReligionData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.religion}
                        </option>
                      ))}
                    {field === 'Nationality' &&
                      ['Indian', 'International'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}
                    {field === 'UHIDType' && (
                      <>
                        {RegisterData.Nationality === 'Indian' &&
                          ['Aadhar', 'VoterId', 'SmartCard'].map(
                            (row, indx) => (
                              <option key={indx} value={row}>
                                {row}
                              </option>
                            )
                          )}
                        {RegisterData.Nationality === 'International' &&
                          ['DrivingLicence', 'Passport'].map((row, indx) => (
                            <option key={indx} value={row}>
                              {row}
                            </option>
                          ))}
                      </>
                    )}
                    {field === 'PatientType' &&
                      ['General', 'VIP', 'Govt'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}


                    {/* {field === 'PatientCategory' &&
                      [
                        'General',
                        'Insurance',
                        'Client',
                        'Corporate',
                        'Donation',
                        'Employee',
                        'EmployeeRelation',
                        'Relation',
                        'Doctor',
                        'DoctorRelation'
                      ].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))} */}

                    {/* {field === 'ReferralSource' &&
                      ['Call', 'Letter', 'Oral'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {formatLabel(row)}
                        </option>
                      ))} */}
                    {/*                     
                    {field === 'Flagging' &&
                      FlaggData?.filter(p => p.Status === 'Active').map(
                        (row, indx) => (
                          <option
                            key={indx}
                            value={row.id}
                            style={{ backgroundColor: row.FlaggColor }}
                          >
                            {' '}
                            {row.FlaggName}
                          </option>
                        )
                      )}


                    {field === 'InsuranceType' &&
                      ['Cashless', 'Reimbursable'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))} */}

                    {/* {[
                      'ClientEmployeeRelation',
                      'CorporateEmployeeRelation',
                      'EmployeeRelation',
                      'Relation',
                      'DoctorRelation'
                    ].includes(field) &&
                      relationships?.map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))} */}

                    {/* {['EmployeeId', 'EmployeeRelation'].includes(field) &&
                      EmployeeData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))} */}

                    {/* {['DoctorId', 'DoctorRelation'].includes(field) &&
                      DoctorIdData?.filter(
                        p => p.id !== RegisterData.DoctorName
                      ).map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.ShortName}
                        </option>
                      ))} */}


                    {/* {field === 'ClientName' &&
                      ClientData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}

                    {field === 'CorporateName' &&
                      CorporateData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}
                    {field === 'InsuranceName' &&
                      InsuranceData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row?.Type === 'MAIN'
                            ? `${row?.Name} - ${row?.Type}`
                            : `${row?.Name} - ${row?.Type} - ${row?.TPA_Name}`}
                        </option>
                      ))} */}
                    {/* {field === 'DonationType' &&
                      DonationData?.map((row, indx) => (
                        <option
                          key={indx}
                          value={row.id}
                        >{`${row?.Type} - ${row?.Name}`}</option>
                      ))} */}
                  </select>
                ) : ['PhoneNo', 'FirstName', 'MiddleName'].includes(field) ? (
                  <div className='Search_patient_icons'>
                    <input
                      id={`${field}_${index}`}
                      type={'text'}
                      onKeyDown={
                        field === 'FirstName'
                          ? handleKeyDownText
                          : handleKeyDownPhoneNo
                      }
                      list={`${field}_iddd`}
                      autoComplete='off'
                      name={field}
                      pattern={field === 'PhoneNo' ? '\\d{10}' : '[A-Za-z]+'}
                      className={
                        errors[field] === 'Invalid'
                          ? 'invalid'
                          : errors[field] === 'Valid'
                            ? 'valid'
                            : ''
                      }
                      readOnly
                      required
                      value={RegisterData[field]}
                      onChange={HandleOnchange}
                    />
                  </div>
                ) : (
                  <input
                    id={`${field}_${index}`}
                    autoComplete='off'
                    type={field === 'DOB' ? 'date' : 'text'}
                    name={field}
                    pattern={
                      field === 'Email'
                        ? '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[cC][oO][mM]$'
                        : field === 'PhoneNo'
                          ? '\\d{10}'
                          : ['UHIDNo'].includes(field)
                            ? '[A-Za-z0-9]+'
                            : field === 'Age'
                              ? '\\d{1,3}'
                              : field === 'DOB'
                                ? ''
                                : '[A-Za-z]+'
                    }
                    className={
                      errors[field] === 'Invalid'
                        ? 'invalid'
                        : errors[field] === 'Valid'
                          ? 'valid'
                          : ''
                    }
                    required
                    readOnly
                    value={RegisterData[field]}
                    onKeyDown={
                      [
                        'MiddleName',
                        'SurName',
                        // 'AliasName',
                        'Occupation',
                        'NextToKinName',
                        'FamilyHeadName',
                        'Street',
                        'Area',
                        'City',
                        'District',
                        'State',
                        'Complaint',
                        'Country'
                      ].includes(field)
                        ? handleKeyDownTextRegistration
                        : field === 'PhoneNo'
                          ? handleKeyDownPhoneNo
                          : null
                    }
                    onChange={HandleOnchange}
                  />
                )}
              </div>

            ))}

        </div>






        {/* ----------------- Address --------------- */}

        <br />

        <div className="DivCenter_container">Address</div>
        <br />

        <div className="RegisFormcon" id='RegisFormcon_2' ref={addressRef}>
          {FilteredFormdataAddress &&
            FilteredFormdataAddress.map((field, index) => (
              <div className='RegisForm_1' key={index}>
                <label htmlFor={`${field}_${index}`}>
                  {formatLabel(field)}
                  <span>:</span>
                </label>
                <input
                  id={`${field}_${index}`}
                  autoComplete='off'
                  type={field === 'Pincode' ? 'number' : 'text'}
                  name={field}
                  pattern={
                    field === 'Pincode'
                      ? '\\d{6,7}'
                      : ['DoorNo'].includes(field)
                        ? '[A-Za-z0-9]+'
                        : '[A-Za-z]+'
                  }
                  className={
                    errors[field] === 'Invalid'
                      ? 'invalid'
                      : errors[field] === 'Valid'
                        ? 'valid'
                        : ''
                  }
                  value={RegisterData[field]}
                  onChange={HandleOnchange}
                  readOnly
                />
              </div>


            ))
          }
        </div>




        {/* ----------------- OP Visit --------------- */}
        <br />

        <div className="DivCenter_container">OP Visit</div>
        <br />

        <div className="RegisFormcon" id="RegisFormcon_3" ref={opvisitref}>

          {FilteredFormdataOPVisitEntry &&
            FilteredFormdataOPVisitEntry.map((field, index) => (
              <div className='RegisForm_1' key={index}>
                <label htmlFor={`${field}_${index}`}>
                  {formatLabel(field)}
                  <span>:</span>
                </label>
                {[
                  'Speciality',
                  'DoctorName',
                  'ReferralSource',
                  'ReferredBy',
                  'PatientCategory',
                  'ColorFlag',
                  // 'ReferralSource',
                  'Flagging',
                  'InsuranceName',
                  'DonationType',
                  'InsuranceType',
                  'ClientName',
                  'ClientEmployeeRelation',
                  'EmployeeRelation',
                  'EmployeeId',
                  'EmployeeRelation',
                  'DoctorId',
                  'DoctorRelation',
                  'CorporateName',
                  'CorporateEmployeeRelation',
                  'Relation',

                ].includes(field) ? (
                  <select
                    id={`${field}_${index}`}
                    name={field}
                    value={OPVisitEntry[field]}
                    onChange={HandleOnchange}
                  >
                    <option value=''>Select</option>
                    {field === 'Speciality' &&
                      SpecializationData?.filter(
                        p => p.Status === 'Active'
                      )?.map((Catg, indx) => (
                        <option key={indx} value={Catg.id}>
                          {Catg.SpecialityName}
                        </option>
                      ))}
                    {field === 'DoctorName' &&
                      DoctorData && Array.isArray(DoctorData) && DoctorData.length !== 0 && DoctorData?.filter(
                        p => p.schedule?.[0]?.working === 'yes'
                      ).map((row, indx) => (
                        <option key={indx} value={row.doctor_id}>
                          {row.doctor_name}
                        </option>
                      ))}

                    {field === 'PatientCategory' &&
                      [
                        'General',
                        'Insurance',
                        'Client',
                        // 'Corporate',
                        'Donation',
                        'Employee',
                        'EmployeeRelation',
                        'Doctor',
                        'DoctorRelation'
                      ].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}

                    {field === 'Flagging' &&
                      FlaggData?.filter(p => p.Status === 'Active').map(
                        (row, indx) => (
                          <option
                            key={indx}
                            value={row.id}
                            style={{ backgroundColor: row.FlaggColor }}
                          >
                            {' '}
                            {row.FlaggName}
                          </option>
                        )
                      )}
                    {field === 'InsuranceType' &&
                      ['Cashless', 'Reimbursable'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}


                    {[
                      'ClientEmployeeRelation',
                      'CorporateEmployeeRelation',
                      'EmployeeRelation',
                      'DoctorRelation',
                      'Relation',
                    ].includes(field) &&
                      relationships?.map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}

                    {['EmployeeId', 'EmployeeRelation'].includes(field) &&
                      EmployeeData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}

                    {['DoctorId', 'DoctorRelation'].includes(field) &&
                      DoctorIdData?.filter(
                        p => p.id !== OPVisitEntry.DoctorName
                      ).map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.ShortName}
                        </option>
                      ))}
                    {field === 'ClientName' &&
                      ClientData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}
                    {field === 'CorporateName' &&
                      CorporateData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}
                    {field === 'InsuranceName' &&
                      InsuranceData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row?.Type === 'MAIN'
                            ? `${row?.Name} - ${row?.Type}`
                            : `${row?.Name} - ${row?.Type} - ${row?.TPA_Name}`}
                        </option>
                      ))}
                    {field === 'DonationType' &&
                      DonationData?.map((row, indx) => (
                        <option
                          key={indx}
                          value={row.id}
                        >{`${row?.Type} - ${row?.Name}`}</option>
                      ))}


                  </select>
                ) : [
                  'IsMLC',
                  'IsReferral',
                  'ClientType',
                ].includes(field) ? (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "flex-start",
                      width: "120px",
                      gap: '10px',
                    }}
                  >
                    <label style={{ width: 'auto' }} htmlFor={`${field}_yes`}>
                      <input
                        required
                        id={`${field}_yes`}
                        type="radio"
                        name={field}
                        value={field === 'ClientType' ? 'Self' : 'Yes'}
                        style={{ width: '15px' }}
                        checked={
                          field === 'ClientType'
                            ? OPVisitEntry[field] === 'Self'
                            : OPVisitEntry[field] === 'Yes'
                        }
                        onChange={e =>
                          setOPVisitEntry(prevState => ({
                            ...prevState,
                            [field]: field === 'ClientType' ? 'Self' : 'Yes',
                          }))
                        }
                      />
                      {field === 'ClientType' ? 'Self' : 'Yes'}
                    </label>
                    <label style={{ width: 'auto' }} htmlFor={`${field}_No`}>
                      <input
                        required
                        id={`${field}_No`}
                        type="radio"
                        name={field}
                        value={field === 'ClientType' ? 'Family' : 'No'}
                        style={{ width: '15px' }}
                        checked={
                          field === 'ClientType'
                            ? OPVisitEntry[field] === 'Family'
                            : OPVisitEntry[field] === 'No'
                        }
                        onChange={e =>
                          setOPVisitEntry(prevState => ({
                            ...prevState,
                            [field]: field === 'ClientType' ? 'Family' : 'No',
                          }))
                        }
                      />
                      {field === 'ClientType' ? 'Family' : 'No'}
                    </label>
                  </div>
                ) : field === 'Complaint' ? (
                  <textarea
                    id={`${field}_${index}`}
                    autoComplete='off'
                    name={field}
                    required
                    value={OPVisitEntry[field]}
                    onChange={HandleOnchange}
                  />
                ) : (
                  field === 'VisitType' ? (
                    <input
                      autoComplete='off'
                      type='text'
                      name={field}
                      readOnly
                      value={OPVisitEntry[field]}
                      onChange={HandleOnchange}
                    />
                  ) : (field === 'TokenNo') ? (
                    <input
                      type="text"
                      value={OPVisitEntry[field]}
                      readOnly
                      onChange={HandleOnchange}

                    />
                  )
                    // : (field === 'TokenNo' && (TokenData || OPVisitEntry.TokenNo)) ? (
                    //   <input
                    //     type="number"
                    //     value={TokenData || OPVisitEntry.TokenNo}
                    //     readOnly
                    //   />
                    // )

                    : (
                      <input
                        autoComplete='off'
                        type={field === 'RelativePhoneNo' ? 'number' : 'text'}
                        name={field}
                        value={OPVisitEntry[field]}
                        onKeyDown={
                          [
                            'NextToKinName',
                          ].includes(field)
                            ? handleKeyDownTextRegistration
                            : null
                        }
                        onChange={HandleOnchange}
                      />
                    ))}
              </div>
            ))}
        </div>






        {/* ----------------- Referral --------------- */}


        {
          OPVisitEntry.IsReferral === 'Yes' && (
            <>
              <br />

              <div className="DivCenter_container">Referral</div>
              <br />

              <div className="RegisFormcon" id="RegisFormcon_4" ref={referalref}>
                {FilteredFormdataRoute &&
                  FilteredFormdataRoute.map((field, index) => (
                    <div className='RegisForm_1' key={index}>
                      <label htmlFor={`${field}_${index}`}>
                        {formatLabel(field)}
                        <span>:</span>
                      </label>
                      {['ReferralSource', 'ReferredBy'].includes(field) && (
                        <select
                          id={`${field}_${index}`}
                          name={field}
                          value={OPVisitEntry[field]}
                          onChange={HandleOnchange}
                          readOnly
                        >
                          <option value=''>Select</option>

                          {field === 'ReferralSource' &&
                            ['Call', 'Letter', 'Oral'].map((row, indx) => (
                              <option key={indx} value={row}>
                                {row}
                              </option>
                            ))}
                          {field === 'ReferredBy' &&
                            ReferralDoctorData.map((row, indx) => (
                              <option key={indx} value={row.id}>
                                {row.ShortName}
                              </option>
                              // <option value="">Select</option>
                            ))}
                          {/* <option value="">Others</option> */}
                        </select>
                      )}
                    </div>
                  ))}
              </div>



            </>
          )
        }




        {/* -----------------Patient Category --------------- */}
        <br />
        <div className="DivCenter_container">Patient Category</div>
        <br />

        <div className="RegisFormcon" id="RegisFormcon_5" ref={categoryref}>
          {PatientCatg &&
            PatientCatg.map((field, index) => (
              <div className='RegisForm_1' key={index}>
                <label htmlFor={`${field}_${index}`}>
                  {formatLabel(field)}
                  <span>:</span>
                </label>
                {[

                  'PatientCategory',
                  'InsuranceName',
                  'InsuranceType',
                  'ClientName',
                  'ClientEmployeeRelation',
                  'DonationType',

                  'EmployeeRelation',
                  'EmployeeId',
                  'EmployeeRelation',
                  'DoctorId',
                  'DoctorRelation',


                ].includes(field) ? (
                  <select
                    id={`${field}_${index}`}
                    name={field}
                    value={OPVisitEntry[field]}
                    onChange={HandleOnchange}
                  >
                    <option value=''>Select</option>


                    {field === 'PatientCategory' &&
                      [
                        'General',
                        'Insurance',
                        'Client',
                        // 'Corporate',
                        'Donation',
                        'Employee',
                        'EmployeeRelation',
                        'Doctor',
                        'DoctorRelation'
                      ].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}


                    {field === 'InsuranceType' &&
                      ['Cashless', 'Reimbursable'].map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}


                    {[
                      'ClientEmployeeRelation',
                      'EmployeeRelation',
                      'DoctorRelation',

                    ].includes(field) &&
                      relationships?.map((row, indx) => (
                        <option key={indx} value={row}>
                          {row}
                        </option>
                      ))}

                    {['EmployeeId', 'EmployeeRelation'].includes(field) &&
                      EmployeeData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}

                    {['DoctorId', 'DoctorRelation'].includes(field) &&
                      DoctorIdData?.filter(
                        p => p.id !== OPVisitEntry.DoctorName
                      ).map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.ShortName}
                        </option>
                      ))}
                    {field === 'ClientName' &&
                      ClientData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}
                    {field === 'CorporateName' &&
                      CorporateData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row.Name}
                        </option>
                      ))}
                    {field === 'InsuranceName' &&
                      InsuranceData?.map((row, indx) => (
                        <option key={indx} value={row.id}>
                          {row?.Type === 'MAIN'
                            ? `${row?.Name} - ${row?.Type}`
                            : `${row?.Name} - ${row?.Type} - ${row?.TPA_Name}`}
                        </option>
                      ))}
                    {field === 'DonationType' &&
                      DonationData?.map((row, indx) => (
                        <option
                          key={indx}
                          value={row.id}
                        >{`${row?.Type} - ${row?.Name}`}</option>
                      ))}


                  </select>
                ) : [

                  'ClientType',

                ].includes(field) ? (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "flex-start",
                      width: "120px",
                      gap: '10px',
                    }}
                  >
                    <label style={{ width: 'auto' }} htmlFor={`${field}_yes`}>
                      <input
                        required
                        id={`${field}_yes`}
                        type="radio"
                        name={field}
                        value={
                          field === 'ClientType'
                            ? 'Self'
                            : field === 'CorporateType'
                              ? 'Company'
                              : 'Yes'
                        }
                        style={{ width: '15px' }}
                        checked={
                          field === 'ClientType'
                            ? OPVisitEntry[field] === 'Self'
                            : field === 'CorporateType'
                              ? OPVisitEntry[field] === 'Company'
                              : OPVisitEntry[field] === 'Yes'
                        }
                        onChange={e =>
                          setOPVisitEntry(prevState => ({
                            ...prevState,
                            [field]:
                              field === 'ClientType'
                                ? 'Self'
                                : field === 'CorporateType'
                                  ? 'Company'
                                  : 'Yes'
                          }))
                        }
                      />
                      {field === 'ClientType'
                        ? 'Self'
                        : field === 'CorporateType'
                          ? 'Company'
                          : 'Yes'}
                    </label>
                    <label style={{ width: 'auto' }} htmlFor={`${field}_No`}>
                      <input
                        required
                        id={`${field}_No`}
                        type="radio"
                        name={field}
                        value={
                          field === 'ClientType'
                            ? 'Family'
                            : field === 'CorporateType'
                              ? 'Individual'
                              : 'No'
                        }
                        style={{ width: '15px' }}
                        checked={
                          field === 'ClientType'
                            ? OPVisitEntry[field] === 'Family'
                            : field === 'CorporateType'
                              ? OPVisitEntry[field] === 'Individual'
                              : OPVisitEntry[field] === 'No'
                        }
                        onChange={e =>
                          setOPVisitEntry(prevState => ({
                            ...prevState,
                            [field]:
                              field === 'ClientType'
                                ? 'Family'
                                : field === 'CorporateType'
                                  ? 'Individual'
                                  : 'No'
                          }))
                        }
                      />
                      {field === 'ClientType'
                        ? 'Family'
                        : field === 'CorporateType'
                          ? 'Individual'
                          : 'No'}
                    </label>
                  </div>
                ) : field === 'Complaint' ? (
                  <textarea
                    id={`${field}_${index}`}
                    autoComplete='off'
                    name={field}
                    required
                    value={OPVisitEntry[field]}
                    onChange={HandleOnchange}
                  />
                ) : (
                  <input
                    autoComplete='off'
                    type='text'
                    name={field}
                    value={OPVisitEntry[field]}
                    onChange={HandleOnchange}
                  />
                )}
              </div>
            ))}
        </div>


        {/* ----------------- Next to kin --------------- */}
        <br />
        <div className="DivCenter_container">Next To Kin</div>
        <br />

        <div className="RegisFormcon" id="RegisFormcon_6" ref={kinref}>
          {FilteredFamilyDetails?.map((field, index) => (
            <div className="RegisForm_1" key={index}>
              <label htmlFor={`${field}_${index}`}>
                {formatLabel(field)}
                <span>:</span>
              </label>
              {field === 'Relation' ? (
                <select
                  id={`${field}_${index}`}
                  name={field}
                  value={OPVisitEntry[field] || ''}
                  onChange={HandleOnchange}
                >
                  <option value="">Select</option>
                  {relationships?.map((row, indx) => (
                    <option key={indx} value={row}>
                      {row}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  autoComplete="off"
                  type={field === 'RelativePhoneNo' ? 'number' : 'text'}
                  name={field}
                  value={OPVisitEntry[field] || ''}
                  onKeyDown={
                    field === 'NextToKinName' ? handleKeyDownTextRegistration : undefined
                  }
                  onChange={HandleOnchange}
                />
              )}
            </div>
          ))}

        </div>





        {/* ----------------- Service --------------- */}
        <br />
        <div className="DivCenter_container">Service</div>
        <br />

        <div className="RegisFormcon" id="RegisFormcon_7" ref={serviceref}>

          {
            FilteredFormdataServices &&
            FilteredFormdataServices.map((field, index) => (
              <div className='RegisForm_1' key={index}>
                <label htmlFor={`${field}_${index}`}>
                  {formatLabel(field)}
                  <span>:</span>
                </label>
                {[
                  'ServiceCategory',
                  'ServiceSubCategory',
                ].includes(field) && (
                    <input
                      autoComplete='off'
                      type='text'
                      name={field}
                      value={OPVisitEntry[field]}
                      list={`${field}_iddd`}
                      onChange={HandleOnchange}
                    />
                  )}
                {
                  <datalist id={`${field}_iddd`}>
                    {field === 'ServiceCategory' && (
                      ServiceCategoryData?.map((row, indx) =>
                        <option key={indx} value={`${row.service_category_id}-${row.service_name}`}>
                          {row.service_name}
                        </option>
                      )
                    )}
                    {field === 'ServiceSubCategory' && (
                      Array.isArray(ServiceSubCategoryData) &&
                      ServiceSubCategoryData.map((row, indx) =>
                        <option key={indx} value={`${row.pk}-${row.service_subcategory}`}>
                          {row.service_subcategory}
                        </option>
                      )
                    )}
                  </datalist>
                }
              </div>
            ))
          }

        </div>



        <div className='Main_container_Btn'>
          <button onClick={handlesubmit}>
            {Registeredit?.RegistrationId ? 'Update' : 'Save'}
          </button>
        </div>
      </div>
      {loading && (
        <div className='loader'>
          <div className='Loading'>
            <div className='spinner-border'></div>
            <div>Loading...</div>
          </div>
        </div>
      )}
      <ToastAlert Message={toast.message} Type={toast.type} />

      {RegisterRoomShow.val && <RoomDetialsSelect />}
      <br />

    </>
  )
}

export default OPVisitEntry



