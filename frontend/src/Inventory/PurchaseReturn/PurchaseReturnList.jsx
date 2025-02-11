
import React, { useCallback, useEffect, useState } from 'react'
import LoupeIcon from "@mui/icons-material/Loupe";
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import axios from 'axios';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import ListIcon from '@mui/icons-material/List';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import EditIcon from "@mui/icons-material/Edit";
import Button from "@mui/material/Button";
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import DeleteSweepIcon from '@mui/icons-material/DeleteSweep';



const PurchaseReturnList = () => {

  const navigate = useNavigate();

  const dispatchvalue = useDispatch();

  const today = new Date();
  const currentDate = today.toISOString().split('T')[0];

  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const toast = useSelector(state => state.userRecord?.toast);

  const [supplierArray, setsupplierArray] = useState([])
  const [LocationData, setLocationData] = useState([]);

  const [PurchaseReturnList, setPurchaseReturnList] = useState([])


  const [Itemlist, setItemlist] = useState([])

  const [selectRoom, setselectRoom] = useState(false);

  const [SerchOptions, setSerchOptions] = useState({
    StatusCheck: '',
    DateType: '',
    CurrentDate: currentDate,
    FromDate: '',
    ToDate: '',
    SupplierId: '',
    SupplierName: '',
    Location: '',
  })


  useEffect(() => {

    axios.get(`${UrlLink}Inventory/PO_Supplier_Data_Get?SupplierTwo=${true}`)
      .then((res) => {
        console.log('pppp----', res.data);
        let Rdata = res.data
        if (Array.isArray(Rdata)) {
          setsupplierArray(Rdata)

        }
      })
      .catch((err) => {
        console.log(err);

      })


    axios.get(`${UrlLink}Masters/Location_Detials_link`)
      .then((res) => {
        const ress = res.data
        setLocationData(ress)
      })
      .catch((err) => {
        console.log(err);
      })


  }, [UrlLink])


  const PurchaseReturn_getFun = useCallback(() => {

    axios.get(`${UrlLink}Inventory/PurchaseReturn_Report_Link`, {
      params: SerchOptions,
    })
      .then((res) => {
        console.log(res.data);
        let data = res.data
        if (data && Array.isArray(data) && data.length !== 0) { setPurchaseReturnList(data) }
        else { setPurchaseReturnList([]) }

      })
      .catch((err) => {
        console.log(err);
      })
  }, [SerchOptions])

  useEffect(() => {
    PurchaseReturn_getFun()
  }, [PurchaseReturn_getFun])


  const handleNewMaster = () => {
    //  navigate('/Home/PurchaseReturn');
    navigate("/Home/InventoryMaster");
    dispatchvalue({ type: "HrFolder", value: "PurchaseReturn" });
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });
    dispatchvalue({ type: 'PurchaseReturnList', value: {} });

  };



  const Handeleonchange = (e) => {

    const { name, value } = e.target

    if (name === 'SupplierId') {

      let Finddata = supplierArray.find((ele) => ele.id === value)
      if (Finddata) {
        setSerchOptions((prev) => ({
          ...prev,
          [name]: value,
          SupplierName: Finddata.SupplierName,
        }))
      }
      else {
        setSerchOptions((prev) => ({
          ...prev,
          [name]: value,
          SupplierName: '',

        }))
      }
    }
    if (name === 'SupplierName') {

      let Finddata = supplierArray.find((ele) => ele.SupplierName === value)
      if (Finddata) {
        setSerchOptions((prev) => ({
          ...prev,
          [name]: value,
          SupplierId: Finddata.id,
        }))
      }
      else {
        setSerchOptions((prev) => ({
          ...prev,
          [name]: value,
          SupplierId: '',

        }))
      }
    }
    else {
      setSerchOptions((prev) => ({
        ...prev,
        [name]: value

      }))
    }


  }

  const ItemView = (row) => {

    let Item = row.Items

    if (Item && Item.length !== 0) {
      setselectRoom(true)
      setItemlist(Item)
    }
    else {

      const tdata = {
        message: 'There is no data to view.',
        type: 'warn'
      };
      dispatchvalue({ type: 'toast', value: tdata });

    }

  }

  const HandelEditdata = (row) => {

    dispatchvalue({ type: 'PurchaseReturnList', value: row });
    navigate("/Home/InventoryMaster");
    dispatchvalue({ type: "HrFolder", value: "PurchaseReturn" });
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });
    dispatchvalue({ type: 'PurchaseReturnList', value: {} });

  }


  const HandelApprovedata = (row, status) => {

    const POconfirm = window.confirm(`Are You Sure You Want to ${status} the Purchase Return for P.R.Number ${row.id} ?`);

    if (POconfirm) {

      let Senddata = {
        EditStatus: status,
        PRreturnid: row.id
      }

      axios.post(`${UrlLink}Inventory/PurchaseReturn_StatusUpdate`, Senddata)
        .then((res) => {
          console.log(res.data);
          let resdata = res.data
          let type = Object.keys(resdata)[0]
          let mess = Object.values(resdata)[0]
          const tdata = {
            message: mess,
            type: type,
          }
          dispatchvalue({ type: 'toast', value: tdata });
          PurchaseReturn_getFun()
        })
        .catch((err) => {
          console.log(err);
        })
    }

  }

  const PurchaseOrderColumn = [
    {
      key: 'id',
      name: 'P.R.Number',
      frozen: true
    },
    {
      key: 'ReturnDate',
      name: 'ReturnDate',
      frozen: true
    },
    {
      key: 'SupplierCode',
      name: 'Supplier Code',
      frozen: true
    }, {
      key: 'SupplierName',
      name: 'Supplier Name',
      frozen: true
    },
    {
      key: 'Items',
      name: 'Item Details',
      renderCell: (params) => (
        <>
          <Button className="cell_btn"
            onClick={() => ItemView(params.row)}
          >
            <ListIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      )
    }, {
      key: 'SupplierMailId',
      name: 'Supplier MailId',

    }, {
      key: 'SupplierContactNumber',
      name: 'Contact Number',

    }, {
      key: 'SupplierContactPerson',
      name: ' Contact Person',
    },
    {
      key: 'Location',
      name: 'Location',
    }, {
      key: 'StoreLocation',
      name: 'Store Location',
    },
    {
      key: 'ReturnTotalItem',
      name: 'Return Total Item',
    },
    {
      key: 'ReturnTotalQuantity',
      name: 'Return Total Quantity',
    },
    {
      key: 'ReturnTotalAmount',
      name: 'Return Total Amount',
    },
    {
      key: 'Status',
      name: 'Status',
    },
    {
      key: 'Edit',
      name: 'Edit',
      renderCell: (params) => (
        <>
          {params.row.Status === 'Pending' ?
            <Button className="cell_btn"
              onClick={() => HandelEditdata(params.row)}
            >
              <EditIcon className="check_box_clrr_cancell" />
            </Button> :
            <>No Action</>}
        </>
      )
    },
    {
      key: 'Action',
      name: 'Action',
      renderCell: (params) => (
        <>
          {params.row.Status === 'Pending' ?
            <>
              <Button className="cell_btn"
                onClick={() => HandelApprovedata(params.row, 'Approved')}
              >
                <CheckCircleOutlineIcon className="check_box_clrr_cancell" />
              </Button>
              <Button className="cell_btn"
                onClick={() => HandelApprovedata(params.row, 'cancelled')}
              >
                <DeleteSweepIcon className="check_box_clrr_cancell" />
              </Button>
            </>
            :
            <Button className="cell_btn">
              No Action
            </Button>}
        </>
      )
    }
  ]



  const ItemColumn = [
    {
      key: 'id',
      name: 'S.No',
      frozen: true
    },
    {
      key: 'ItemCode',
      name: 'Item Code',
      frozen: true
    },
    {
      key: 'ItemName',
      name: 'Item Name',
      frozen: true
    },
    {
      key: 'GenericName',
      name: 'Generic Name'
    },
    {
      key: 'CompanyName',
      name: 'Manufacturer Name'
    },
    {
      key: 'HSNCode',
      name: 'HSN Code'
    },
    {
      key: 'ProductType',
      name: 'Product Type',
    },
    {
      key: 'Strength',
      name: 'Strength'
    },
    {
      key: 'Volume',
      name: 'Volume',
    },
    {
      key: 'PackType',
      name: 'Pack Type',
    },
    {
      key: 'PackQuantity',
      name: 'Pack Quantity',
    },
    {
      key: 'BatchNo',
      name: 'Batch No'
    },
    {
      key: 'PurchaseRateWithTax',
      name: 'PurchaseRateWithTax'
    },
    {
      key: 'PurchaseQuantity',
      name: 'Purchase Quantity'
    },
    {
      key: 'PurchaseAmount',
      name: 'Purchase Amount'
    },
    {
      key: 'ReturnPackQuantity',
      name: 'Return Quantity'
    },
    {
      key: 'ReturnQuantityAmount',
      name: 'Return Quantity Amount'
    },
    {
      key: 'Remarks',
      name: 'Remarks'
    }
  ]


  return (
    <>

      <div className="Main_container_app">
        <h3>Purchase Return List</h3>
        <br />
        <div className="RegisFormcon_1">
          <div className="RegisForm_1">
            <label>Status<span>:</span></label>

            <select
              name='StatusCheck'
              value={SerchOptions.StatusCheck}
              onChange={Handeleonchange}
            >
              <option value=''>Select</option>
              <option value='Pending'>Pending</option>
              <option value='Approved'>Approved</option>
              <option value='cancelled'>cancelled</option>
            </select>
          </div>

          <div className="RegisForm_1">
            <label>Date Type<span>:</span></label>
            <select
              name='DateType'
              value={SerchOptions.DateType}
              onChange={Handeleonchange}
            >
              <option value=''>Select</option>
              <option value='CurrentDate'>Current Date</option>
              <option value='Customize'>Customize</option>
            </select>
          </div>

          {SerchOptions.DateType === 'CurrentDate' ?
            <div className="RegisForm_1">
              <label>Current Date<span>:</span></label>
              <input
                type='date'
                name='CurrentDate'
                value={SerchOptions.CurrentDate}
                onChange={Handeleonchange}
                readOnly
              />

            </div>
            :
            <>
              <div className="RegisForm_1">
                <label>From Date<span>:</span></label>
                <input
                  type='date'
                  name='FromDate'
                  value={SerchOptions.FromDate}
                  onChange={Handeleonchange}
                />

              </div>


              <div className="RegisForm_1">
                <label>To Date<span>:</span></label>
                <input
                  type='date'
                  name='ToDate'
                  value={SerchOptions.ToDate}
                  onChange={Handeleonchange}
                  min={SerchOptions.FromDate}
                />

              </div>
            </>}

          <div className="RegisForm_1">
            <label>Supplier Id<span>:</span></label>
            <input
              type='text'
              name='SupplierId'
              value={SerchOptions.SupplierId}
              onChange={Handeleonchange}
              list='SupplierIdList'
            />
            <datalist id='SupplierIdList'>
              {
                supplierArray.map((ele, ind) => (
                  <option key={ind + 'key'} value={ele.id} ></option>
                ))

              }
            </datalist>

          </div>


          <div className="RegisForm_1">
            <label>Supplier Name<span>:</span></label>
            <input
              type='text'
              name='SupplierName'
              value={SerchOptions.SupplierName}
              onChange={Handeleonchange}
              list='SupplierNameList'
            />
            <datalist id='SupplierNameList'>
              {
                supplierArray.map((ele, ind) => (
                  <option key={ind + 'key'} value={ele.SupplierName} ></option>
                ))
              }
            </datalist>

          </div>



          <div className="RegisForm_1">
            <label>Location<span>:</span></label>
            <select
              id='Location'
              name='Location'
              value={SerchOptions.Location}
              onChange={Handeleonchange}
            >
              <option value=''>Select</option>
              {
                LocationData.map((ele, ind) => (
                  <option key={ind + 'key'} value={ele.id} >{ele.locationName}</option>
                ))

              }
            </select>
          </div>

          <button
            className="search_div_bar_btn_1"
            onClick={handleNewMaster}
            title="New Doctor Register"
          >
            <LoupeIcon />
          </button>
        </div>

        <br />
        <ReactGrid columns={PurchaseOrderColumn} RowData={PurchaseReturnList} />

      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />


      {selectRoom && Itemlist.length !== 0 && (
        <div className="loader" onClick={() => setselectRoom(false)}>
          <div className="loader_register_roomshow" onClick={(e) => e.stopPropagation()}>
            <br />

            <div className="common_center_tag">
              <span>Item Details</span>
            </div>
            <br />
            <br />

            <ReactGrid columns={ItemColumn} RowData={Itemlist} />
          </div>
        </div>
      )}

    </>
  )
}

export default PurchaseReturnList;
