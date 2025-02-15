import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import '../../OtManagement/OtManagement.css';
import axios from 'axios';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';


const IpHandoverDetial = () => {

  const Registeredit = useSelector(state => state.Frontoffice?.Registeredit);
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const toast = useSelector((state) => state.userRecord?.toast);
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const [getdata, setgetdata] = useState(false)
  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [HandoverData, setHandoverData] = useState({
    ReasonForAdmission: "",
    PatientConditionOnAdmission: "",
    PatientFileGiven: "PatientFileGivenNo",
    AadharGiven: "AadharGivenNo",
    getdata: false
  })
  const handleonchange = (e) => {
    const { name, value } = e.target
    setHandoverData((prev) => ({
      ...prev,
      [name]: value
    }))
  }
  const handlesave = () => {
    const exist = Object.keys(HandoverData).filter(p => !HandoverData[p])
    if (exist.length === 0) {
      const data = {
        ...HandoverData,
        RegistrationId: Registeredit?.RegistrationId,
        created_by: UserData?.username
      }
      axios.post(`${UrlLink}Frontoffice/post_ip_handover_details`, data)
        .then((res) => {
          const resres = res.data;
          let typp = Object.keys(resres)[0];
          let mess = Object.values(resres)[0];
          const tdata = {
            message: mess,
            type: typp,
          };
          setgetdata(prev => !prev)
          dispatchvalue({ type: 'toast', value: tdata });
        })
        .catch((err) => {
          console.log(err);

        })
    } else {
      const tdata = {
        message: `Please fill the detials : ${exist.join(',')}`,
        type: 'warn',
      };
      dispatchvalue({ type: 'toast', value: tdata });
    }

  }

  useEffect(() => {
    axios.get(`${UrlLink}Frontoffice/post_ip_handover_details?RegistrationId=${Registeredit?.RegistrationId},`)
      .then((res) => {
        const ress = res.data;
        setHandoverData({
          ReasonForAdmission: ress.ReasonForAdmission,
          PatientConditionOnAdmission: ress.PatientConditionOnAdmission,
          PatientFileGiven: ress.PatientFileGiven,
          AadharGiven: ress.AadharGiven,
          getdata: true
        });

      })
      .catch((err) => {
        setHandoverData({
          ReasonForAdmission: "",
          PatientConditionOnAdmission: "",
          PatientFileGiven: "PatientFileGivenNo",
          AadharGiven: "AadharGivenNo",
          getdata: false
        });
        console.log(err);
      });
  }, [getdata, UrlLink, Registeredit])


  const handleHandover = () => {
    const data={
      RegistrationId: Registeredit?.RegistrationId,
      type:'Admit',
      Reason:''
    }
    axios.post(`${UrlLink}Frontoffice/post_ip_submit_handover_or_cancel_details`, data)
      .then((res) => {
        const resres = res.data;
        let typp = Object.keys(resres)[0];
        let mess = Object.values(resres)[0];
        const tdata = {
          message: mess,
          type: typp,
        };
        setgetdata(prev => !prev)
        dispatchvalue({ type: 'toast', value: tdata });
        dispatchvalue({ type: 'Registeredit', value: {} });
        navigate("/Home/WardManagementFolder");
        dispatchvalue({ type: "HrFolder", value:"IPHandOverList"});
        dispatchvalue({ type: "setPreviousFolder", value: null });
        dispatchvalue({ type: "showMenu", value: true });
        
      })
      .catch((err) => {
        console.log(err);

      })
  }
  return (
    <>
      <div className="form-section5 handover_con">
        <div className="Otdoctor_intra_Con handover">
          {
            Object.keys(HandoverData).filter(p => p !== 'getdata' && p !== 'PatientFileGiven' && p !== 'AadharGiven').map((field, indx) => (
              <div className="text_adjust_mt_Ot" key={indx}>
                <label htmlFor={`${field}_${indx}`}>
                  {
                    field
                  }
                  <span>:</span>
                </label>
                <textarea
                  id={`${field}_${indx}`}
                  name={field}
                  value={HandoverData[field]}
                  onChange={handleonchange}
                />
              </div>
            ))
          }
        </div>

        {/* Separate div for PatientFileGiven */}
        <div className="text_adjust_mt_Ot">
          <label htmlFor="PatientFileGiven">
            Patient File Given
            <span>:</span>
          </label>
          <div className="text_adjust_mt_Ot_rado_0">
            <input
              type="radio"
              id="PatientFileGiven_yes"
              name="PatientFileGiven"
              value="PatientFileGivenYes"
              checked={HandoverData.PatientFileGiven === "PatientFileGivenYes"}
              onChange={handleonchange}
            />
            <label htmlFor="PatientFileGiven_yes">Yes</label>

            <input
              type="radio"
              id="PatientFileGiven_no"
              name="PatientFileGiven"
              value="PatientFileGivenNo"
              checked={HandoverData.PatientFileGiven === "PatientFileGivenNo"}
              onChange={handleonchange}
            />
            <label htmlFor="PatientFileGiven_no">No</label>
          </div>
        </div>

        {/* Separate div for AadharGiven */}
        <div className="text_adjust_mt_Ot">
          <label htmlFor="AadharGiven">
            Aadhar Given
            <span>:</span>
          </label>
          <div className="text_adjust_mt_Ot_rado_0">
            <input
              type="radio"
              id="AadharGiven_yes"
              name="AadharGiven"
              value="AadharGivenYes"
              checked={HandoverData.AadharGiven === "AadharGivenYes"}
              onChange={handleonchange}
            />
            <label htmlFor="AadharGiven_yes">Yes</label>

            <input
              type="radio"
              id="AadharGiven_no"
              name="AadharGiven"
              value="AadharGivenNo"
              checked={HandoverData.AadharGiven === "AadharGivenNo"}
              onChange={handleonchange}
            />
            <label htmlFor="AadharGiven_no">No</label>
          </div>
        </div>

      </div>
      <div className="Main_container_Btn">
        <button onClick={!HandoverData.getdata ? handlesave : handleHandover}>{!HandoverData.getdata ? 'save' : 'Hand Over'}</button>
      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  )
}

export default IpHandoverDetial;
