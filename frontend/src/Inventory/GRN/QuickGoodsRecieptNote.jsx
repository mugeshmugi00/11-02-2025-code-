import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { addDays, format } from 'date-fns';
import axios from 'axios';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import ModelContainer from '../../OtherComponent/ModelContainer/ModelContainer';
import { BlockInvalidcharecternumber } from '../../OtherComponent/OtherFunctions';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from '@mui/icons-material/Delete';
import ManageSearchIcon from '@mui/icons-material/ManageSearch';


 
const QuickGoodsRecieptNote = () => {



    const dispatchvalue = useDispatch();
    const navigate = useNavigate();
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const toast = useSelector(state => state.userRecord?.toast);
    const GoodsReceiptNoteEdit = useSelector(state => state.Inventorydata?.GoodsReceiptNoteEdit);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const [GrnSupplierDetials, setGrnSupplierDetials] = useState({
        IsOldGRN: false,
        GRNDate: '',
        SupplierCode: '',
        SupplierName: '',
        ContactPerson: "",
        ContactNumber: '',
        EmailAddress: '',
        SupplierBillNumber: '',
        SupplierBillDate: '',
        SupplierBillDueDate: '',
        SupplierBillAmount: '',
        StoreLocation: '',
        ReceivingPersonName: '',
        IsFOCAvailable: false,
        FOCMethod: 'Invoice',
        FileAttachment: null,
        Status: 'Recieved',
        pk: null,

        // 

        TotalTaxableAmount: '',
        TotalTaxAmount: '',
        TotalAmount: '',
        TotalDiscountMethod: '',
        TotalDiscountType: '',
        TotalDiscount: '',
        FinalTotalTaxableAmount: '',
        FinalTotalTaxAmount: '',
        FinalTotalAmount: '',
        RoundOffAmount: '',
        NetAmount: '',
    })
    const [GrnItemDetials, setGrnItemDetials] = useState({
        id: null,
        pk: null,
        ItemCode: '',
        ItemName: '',
        // ----


        IsFOCProduct: false,
        FOCItemCode: '',
        FOCItemName: '',
        PurchaseRateTaxable: '',
        TaxPercentage: '',
        PurchaseRateWithTax: '',
        MRP: '',
        TaxType: '',
        ReceivedQty: '',
        FOCQuantity: '',
        TotalReceivedQty: '',
        TotalPackQuantity: '',
        IsMRPAsSellablePrice: true,
        SellablePrice: '',
        SellableQtyPrice: '',
        TotalPackTaxableAmount: '',
        TotalTaxAmount: '',
        TotalPackAmount: '',
        BatchNo: '',
        IsManufactureDateAvailable: false,
        ManufactureDate: '',
        IsExpiryDateAvailable: false,
        ExpiryDate: '',
        DiscountMethod: '',
        DiscountType: '',
        Discount: '',
        FinalTotalPackTaxableAmount: '',
        FinalTotalTaxAmount: '',
        FinalTotalPackAmount: '',
        Status: 'Recieved'
    })


    const [ProductListFormOne, setProductListFormOne] = useState([]);
    const [ProductListFormTwo, setProductListFormTwo] = useState([]);
    const [SupplierData, setSupplierData] = useState([]);
    const [SupplierProductListData, setSupplierProductListData] = useState([]);
    const [FocSupplierProductListData, setFocSupplierProductListData] = useState([]);
    const [StoreLocationData, setStoreLocationData] = useState([]);
    const [GrnProductListDatas, setGrnProductListDatas] = useState([]);
  const clearGrnItemsList = () => {
        setGrnItemDetials({
            id: null,
            pk: null,
            ItemCode: '',
            ItemName: '',
            // ----
            IsFOCProduct: false,
            FOCItemCode: '',
            FOCItemName: '',
            PurchaseRateTaxable: '',
            TaxPercentage: '',
            PurchaseRateWithTax: '',
            MRP: '',
            TaxType: '',
            ReceivedQty: '',
            FOCQuantity: '',
            TotalReceivedQty: '',
            TotalPackQuantity: '',
            IsMRPAsSellablePrice: true,
            SellablePrice: '',
            SellableQtyPrice: '',
            TotalPackTaxableAmount: '',
            TotalTaxAmount: '',
            TotalPackAmount: '',
            BatchNo: '',
            IsManufactureDateAvailable: false,
            ManufactureDate: '',
            IsExpiryDateAvailable: false,
            ExpiryDate: '',
            DiscountMethod: '',
            DiscountType: '',
            Discount: '',
            FinalTotalPackTaxableAmount: '',
            FinalTotalTaxAmount: '',
            FinalTotalPackAmount: '',
            Status: 'Recieved',
        })
    }


    const currentDate = format(new Date(), 'yyyy-MM-dd');

    useEffect(() => {
        setGrnSupplierDetials((prev) => ({
            ...prev,
            GRNDate: currentDate,
            SupplierBillDate: currentDate
        }))
    }, [GrnSupplierDetials.IsOldGRN, currentDate])

    useEffect(() => {
        if (userRecord?.location) {
            axios.get(`${UrlLink}Masters/Inventory_Master_Detials_link?SearchLocation=${userRecord?.location}&forquickgrn=${false}`)
                .then((res) => {
                    const data = res.data
                    setStoreLocationData(Array.isArray(data) ? data : [])
                })
                .catch((err) => {
                    console.log(err);

                })

        }
    }, [UrlLink, userRecord?.location])
    useEffect(() => {
        axios.get(`${UrlLink}Inventory/Supplier_Data_Get?ForQuickGrn=${true}`, {
            params: {
                SupplierCode: GrnSupplierDetials.SupplierCode,
                SupplierName: GrnSupplierDetials.SupplierName
            }
        })
            .then((res) => {
                const data = res.data
                setSupplierData(Array.isArray(data) ? data : [])
            })
            .catch((err) => {
                console.log(err);
                setSupplierData([])
            })
    }, [UrlLink, GrnSupplierDetials.SupplierCode, GrnSupplierDetials.SupplierName])

    const formatLabel = (label) => {

        if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
            return label
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/^./, (str) => str.toUpperCase());
        } else {
            return label;
        }
    };




    useEffect(() => {
        const findsupdata = SupplierData.find(p => p.id === GrnSupplierDetials.SupplierCode)
        if (findsupdata) {
            axios.get(`${UrlLink}Inventory/Supplier_product_Mapping_link`, {
                params: {
                    SupplierId: findsupdata.id,
                    forquickgrn: true,
                    ItemCode: GrnItemDetials.ItemCode,
                    ItemName: GrnItemDetials.ItemName,
                }
            })
                .then((res) => {
                    const resdata = res.data
                    setSupplierProductListData(Array.isArray(resdata) ? resdata : [])

                })
                .catch((err) => {
                    console.log(err);
                    setSupplierProductListData([])

                })
        } else {
            setSupplierProductListData([])

        }

    }, [UrlLink,
        SupplierData,
        GrnSupplierDetials.SupplierCode,
        GrnItemDetials.ItemCode,
        GrnItemDetials.ItemName
    ])



    useEffect(() => {
        const findsupdata = SupplierData.find(p => p.id === GrnSupplierDetials.SupplierCode)
        if (findsupdata) {
            axios.get(`${UrlLink}Inventory/Supplier_product_Mapping_link`, {
                params: {
                    SupplierId: findsupdata.id,
                    forquickgrn: true,
                    ItemCode: GrnItemDetials.FOCItemCode,
                    ItemName: GrnItemDetials.FOCItemName,
                }
            })
                .then((res) => {
                    const resdata = res.data.filter((f) => "" + f.ItemCode !== "" + GrnItemDetials.ItemCode)

                    setFocSupplierProductListData(Array.isArray(resdata) ? resdata : [])

                })
                .catch((err) => {
                    console.log(err);
                    setFocSupplierProductListData([])

                })
        } else {
            setFocSupplierProductListData([])

        }

    }, [
        SupplierData,
        UrlLink,
        GrnSupplierDetials.SupplierCode,
        GrnItemDetials.FOCItemCode,
        GrnItemDetials.FOCItemName,
        GrnItemDetials.ItemCode,
    ])



    const fetchSupplierData = async (code) => {
        try {

            const response = await axios.get(`${UrlLink}Inventory/Supplier_Data_Get?SupplierCode=${code}`);
            return response.data; // This assumes data is the correct field you want to return
        } catch (error) {
            console.error("Error fetching supplier data:", error);
            // You can throw the error or return a default value
            return {}
        }
    };




    useEffect(() => {

        if (Object.keys(GoodsReceiptNoteEdit).length) {
            setGrnSupplierDetials({
                // IsQuickGRN: GoodsReceiptNoteEdit?.IsQuickGRN,
                IsOldGRN: GoodsReceiptNoteEdit?.IsOldGRN,
                GRNDate: GoodsReceiptNoteEdit?.GrnDate,
                SupplierCode: GoodsReceiptNoteEdit?.SupplierCode,
                SupplierName: GoodsReceiptNoteEdit?.SupplierName,
                ContactPerson: GoodsReceiptNoteEdit?.ContactPerson,
                ContactNumber: GoodsReceiptNoteEdit?.ContactNumber,
                EmailAddress: GoodsReceiptNoteEdit?.EmailAddress,
                SupplierBillNumber: GoodsReceiptNoteEdit?.Supplier_Bill_Number,
                SupplierBillDate: GoodsReceiptNoteEdit?.Supplier_Bill_Date,
                SupplierBillDueDate: GoodsReceiptNoteEdit?.Supplier_Bill_Due_Date,
                SupplierBillAmount: GoodsReceiptNoteEdit?.Supplier_Bill_Amount,
                StoreLocation: GoodsReceiptNoteEdit?.Store_location_pk,
                ReceivingPersonName: GoodsReceiptNoteEdit?.Received_person,
                IsFOCAvailable: GoodsReceiptNoteEdit?.Is_Foc_Available,
                FOCMethod: GoodsReceiptNoteEdit?.Foc_Method,
                FileAttachment: GoodsReceiptNoteEdit?.FileAttachment,
                Status: GoodsReceiptNoteEdit?.Status,
                pk: GoodsReceiptNoteEdit?.pk,
                TotalTaxableAmount: GoodsReceiptNoteEdit?.Taxable_Amount,
                TotalTaxAmount: GoodsReceiptNoteEdit?.Tax_Amount,
                TotalAmount: GoodsReceiptNoteEdit?.Total_Amount,
                TotalDiscountMethod: GoodsReceiptNoteEdit?.Total_Discount_Method,
                TotalDiscountType: GoodsReceiptNoteEdit?.Total_Discount_Type,
                TotalDiscount: GoodsReceiptNoteEdit?.Discount_Amount,
                FinalTotalTaxableAmount: GoodsReceiptNoteEdit?.Final_Taxable_Amount,
                FinalTotalTaxAmount: GoodsReceiptNoteEdit?.Final_Tax_Amount,
                FinalTotalAmount: GoodsReceiptNoteEdit?.Final_Total_Amount,
                RoundOffAmount: GoodsReceiptNoteEdit?.Round_off_Amount,
                NetAmount: GoodsReceiptNoteEdit?.Net_Amount,
            })
            if (GoodsReceiptNoteEdit?.GRN_Items) {
                setGrnProductListDatas(GoodsReceiptNoteEdit?.GRN_Items)
            }
        }

    }, [GoodsReceiptNoteEdit])




    const HandeleOnchange = (e) => {
        const { name, value } = e.target

        if (name === 'IsOldGRN') {
            setGrnSupplierDetials(prev => ({
                ...prev,
                [name]: value === 'Yes',
                GRNDate: '',
                SupplierCode: '',
                SupplierName: '',
                ContactPerson: "",
                ContactNumber: '',
                EmailAddress: '',
                SupplierBillNumber: '',
                SupplierBillDate: '',
                SupplierBillDueDate: '',
                SupplierBillAmount: '',
                StoreLocation: '',
                ReceivingPersonName: '',
                IsFOCAvailable: false,
                FOCMethod: 'Invoice',
                FileAttachment: null,
                Status: 'Recieved',
                pk: null,
                TotalTaxableAmount: '',
                TotalTaxAmount: '',
                TotalAmount: '',
                TotalDiscountMethod: '',
                TotalDiscountType: '',
                TotalDiscount: '',
                FinalTotalTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalAmount: '',
                RoundOffAmount: '',
                NetAmount: '',
            }))
            clearGrnItemsList()
            setGrnProductListDatas([])
        } else if (name === 'SupplierCode') {

            setGrnSupplierDetials((prev) => ({
                IsOldGRN: prev.IsOldGRN,
                GRNDate: prev.GRNDate,
                [name]: value,
                SupplierName: '',
                ContactPerson: "",
                ContactNumber: '',
                EmailAddress: '',
                SupplierBillNumber: '',
                SupplierBillDate: prev.SupplierBillDate,
                SupplierBillDueDate: '',
                SupplierBillAmount: '',
                StoreLocation: '',
                ReceivingPersonName: '',
                IsFOCAvailable: false,
                FOCMethod: 'Invoice',
                FileAttachment: null,
                Status: 'Recieved',
                pk: null,

                TotalTaxableAmount: '',
                TotalTaxAmount: '',
                TotalAmount: '',
                TotalDiscountMethod: '',
                TotalDiscountType: '',
                TotalDiscount: '',
                FinalTotalTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalAmount: '',
                RoundOffAmount: '',
                NetAmount: '',

            }))
            clearGrnItemsList()
            setGrnProductListDatas([])

        } else if (name === 'SupplierName') {

            setGrnSupplierDetials((prev) => ({
                IsOldGRN: prev.IsOldGRN,
                GRNDate: prev.GRNDate,
                SupplierCode: '',
                [name]: value,
                ContactPerson: "",
                ContactNumber: '',
                EmailAddress: '',
                SupplierBillNumber: '',
                SupplierBillDate: prev.SupplierBillDate,
                SupplierBillDueDate: '',
                SupplierBillAmount: '',
                StoreLocation: '',
                ReceivingPersonName: '',
                IsFOCAvailable: false,
                FOCMethod: 'Invoice',
                FileAttachment: null,
                Status: 'Recieved',
                pk: null,

                TotalTaxableAmount: '',
                TotalTaxAmount: '',
                TotalAmount: '',
                TotalDiscountMethod: '',
                TotalDiscountType: '',
                TotalDiscount: '',
                FinalTotalTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalAmount: '',
                RoundOffAmount: '',
                NetAmount: '',

            }))
            clearGrnItemsList()
            setGrnProductListDatas([])
            

        } else if (name === 'IsFOCAvailable') {
            setGrnSupplierDetials((prev) => ({
                ...prev,
                [name]: value === 'Yes',
                FOCMethod: 'Invoice',
            }))
        } else if (name === 'TotalDiscountMethod') {
            setGrnSupplierDetials((prev) => ({
                ...prev,
                [name]: value,
                TotalDiscountType: '',
                TotalDiscount: '',
            }))
        } else if (name === 'TotalDiscountType') {
            setGrnSupplierDetials((prev) => ({
                ...prev,
                [name]: value,
                TotalDiscount: '',
            }))
        } else {
            setGrnSupplierDetials((prev) => ({
                ...prev,
                [name]: value
            }))
        }

    }
    const handlesearchsupplierlist = async (field) => {
        let findsupdata
        if (field === 'SupplierCode') {
            findsupdata = SupplierData.find(p => p.id === GrnSupplierDetials.SupplierCode)
        } else {
            findsupdata = SupplierData.find(p => p.SupplierName === GrnSupplierDetials.SupplierName)
        }
        if (findsupdata) {
            const data = await fetchSupplierData(findsupdata.id)
            const initialDate = new Date(GrnSupplierDetials.SupplierBillDate);
            const newDate = addDays(initialDate, 45);
            const supplierbillduedate = format(newDate, 'yyyy-MM-dd')
            setGrnSupplierDetials((prev) => ({
                IsOldGRN: prev.IsOldGRN,
                GRNDate: prev.GRNDate,
                SupplierCode: findsupdata?.id,
                SupplierName: findsupdata?.SupplierName,
                ContactPerson: data?.ContactPerson,
                ContactNumber: data?.ContactNumber,
                EmailAddress: data?.EmailAddress,
                SupplierBillNumber: '',
                SupplierBillDate: prev.SupplierBillDate,
                SupplierBillDueDate: supplierbillduedate,
                SupplierBillAmount: '',
                StoreLocation: '',
                ReceivingPersonName: '',
                IsFOCAvailable: false,
                FOCMethod: 'Invoice',
                FileAttachment: null,
                Status: 'Recieved',
                pk: null,

                TotalTaxableAmount: '',
                TotalTaxAmount: '',
                TotalAmount: '',
                TotalDiscountMethod: '',
                TotalDiscountType: '',
                TotalDiscount: '',
                FinalTotalTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalAmount: '',
                RoundOffAmount: '',
                NetAmount: '',

            }))
        } else {
            setGrnSupplierDetials((prev) => ({
                IsOldGRN: prev.IsOldGRN,
                GRNDate: prev.GRNDate,
                SupplierCode: '',
                SupplierName: '',
                ContactPerson: "",
                ContactNumber: '',
                EmailAddress: '',
                SupplierBillNumber: '',
                SupplierBillDate: prev.SupplierBillDate,
                SupplierBillDueDate: '',
                SupplierBillAmount: '',
                StoreLocation: '',
                ReceivingPersonName: '',
                IsFOCAvailable: false,
                FOCMethod: 'Invoice',
                FileAttachment: null,
                Status: 'Recieved',
                pk: null,

                TotalTaxableAmount: '',
                TotalTaxAmount: '',
                TotalAmount: '',
                TotalDiscountMethod: '',
                TotalDiscountType: '',
                TotalDiscount: '',
                FinalTotalTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalAmount: '',
                RoundOffAmount: '',
                NetAmount: '',

            }))
            setGrnProductListDatas([])
        }
    }
    const HandeleOnchangeItemDetials = (e) => {
        const { name, value } = e.target

        if (['IsFOCProduct', 'IsMRPAsSellablePrice', 'IsManufactureDateAvailable', 'IsExpiryDateAvailable'].includes(name)) {

            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value === 'Yes'
            }))
        } else if (name === 'ItemCode') {

            setGrnItemDetials((prev) => ({
                id: null,
                pk: null,
                [name]: value,
                ItemName: '',
                IsFOCProduct: false,
                FOCItemCode: '',
                FOCItemName: '',
                PurchaseRateTaxable: '',
                TaxPercentage: '',
                PurchaseRateWithTax: '',
                MRP: '',
                TaxType: '',
                ReceivedQty: '',
                FOCQuantity: '',
                TotalReceivedQty: '',
                TotalPackQuantity: '',
                IsMRPAsSellablePrice: true,
                SellablePrice: '',
                SellableQtyPrice: '',
                TotalPackTaxableAmount: '',
                TotalTaxAmount: '',
                TotalPackAmount: '',
                BatchNo: '',
                IsManufactureDateAvailable: false,
                ManufactureDate: '',
                IsExpiryDateAvailable: false,
                ExpiryDate: '',
                DiscountMethod: '',
                DiscountType: '',
                Discount: '',
                FinalTotalPackTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalPackAmount: '',
                Status: 'Recieved'
            }))

        } else if (name === 'ItemName') {

            setGrnItemDetials((prev) => ({
                id: null,
                pk: null,
                ItemCode: '',
                [name]: value,
                IsFOCProduct: false,
                FOCItemCode: '',
                FOCItemName: '',
                PurchaseRateTaxable: '',
                TaxPercentage: '',
                PurchaseRateWithTax: '',
                MRP: '',
                TaxType: '',
                ReceivedQty: '',
                FOCQuantity: '',
                TotalReceivedQty: '',
                TotalPackQuantity: '',
                IsMRPAsSellablePrice: true,
                SellablePrice: '',
                SellableQtyPrice: '',
                TotalPackTaxableAmount: '',
                TotalTaxAmount: '',
                TotalPackAmount: '',
                BatchNo: '',
                IsManufactureDateAvailable: false,
                ManufactureDate: '',
                IsExpiryDateAvailable: false,
                ExpiryDate: '',
                DiscountMethod: '',
                DiscountType: '',
                Discount: '',
                FinalTotalPackTaxableAmount: '',
                FinalTotalTaxAmount: '',
                FinalTotalPackAmount: '',
                Status: 'Recieved'
            }))

        } else if (name === "FOCItemCode") {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                FOCItemName: ''
            }))
        } else if (name === "MRP") {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                IsMRPAsSellablePrice: true,
                SellablePrice: value,
                SellableQtyPrice: '',
            }))
        } else if (name === "SellablePrice") {
            if (parseFloat(value) <= parseFloat(GrnItemDetials.MRP)) {
                setGrnItemDetials((prev) => ({
                    ...prev,
                    [name]: value,
                }))
            } else {
                setGrnItemDetials((prev) => ({
                    ...prev,
                    [name]: GrnItemDetials.MRP,
                    IsMRPAsSellablePrice: true,
                    SellableQtyPrice: '',
                }))
                const tdata = {
                    message: `The selling Price must be less than or equal to MRP of ${GrnItemDetials.MRP}.`,
                    type: 'warn',
                }
                dispatchvalue({ type: 'toast', value: tdata });
            }

        } else if (name === "FOCItemName") {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                FOCItemCode: ''
            }))
        } else if (name === "IsManufactureDateAvailable") {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                ManufactureDate: ''
            }))
        } else if (name === "IsExpiryDateAvailable") {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                ExpiryDate: ''
            }))
        } else if (name === 'DiscountMethod') {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                DiscountType: '',
                Discount: '',
            }))
        } else if (name === 'DiscountType') {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value,
                Discount: '',
            }))
        } else {
            setGrnItemDetials((prev) => ({
                ...prev,
                [name]: value
            }))
        }

    }


    const handlesearchitemslist = (type = 'normal', fieldtype = 'id') => {
        if (type === 'normal') {
            if (GrnItemDetials.ItemCode || GrnItemDetials.ItemName) {
                let findadata = SupplierProductListData.find(p => "" + p.ItemCode === GrnItemDetials.ItemCode)
                if (fieldtype !== 'id') {
                    findadata = SupplierProductListData.find(p => "" + p.ItemName === GrnItemDetials.ItemName)
                }
                if (findadata) {
                    const { id, SupplierPoductId, ItemCode, ItemName, Status, Is_Manufacture_Date_Available, Is_Expiry_Date_Available, ...rest } = findadata
                    setGrnItemDetials((prev) => ({
                        id: null,
                        pk: null,
                        ItemCode: ItemCode,
                        ItemName: ItemName,

                        ...rest,
                        IsFOCProduct: false,
                        FOCItemCode: '',
                        FOCItemName: '',
                        PurchaseRateTaxable: rest?.PreviousPurchaseRateBeforeGST,
                        TaxPercentage: rest?.PreviousGST,
                        PurchaseRateWithTax: rest?.PreviousPurchaseRateAfterGST,
                        MRP: rest?.PreviousMRP,
                        TaxType: "",
                        ReceivedQty: '',
                        FOCQuantity: '',
                        TotalReceivedQty: '',
                        TotalPackQuantity: '',
                        IsMRPAsSellablePrice: true,
                        SellablePrice: rest?.PreviousMRP,
                        SellableQtyPrice: '',
                        TotalPackTaxableAmount: '',
                        TotalTaxAmount: '',
                        TotalPackAmount: '',
                        BatchNo: '',
                        IsManufactureDateAvailable: Is_Manufacture_Date_Available,
                        ManufactureDate: '',
                        IsExpiryDateAvailable: Is_Expiry_Date_Available,
                        ExpiryDate: '',
                        DiscountMethod: '',
                        DiscountType: '',
                        Discount: '',
                        FinalTotalPackTaxableAmount: '',
                        FinalTotalTaxAmount: '',
                        FinalTotalPackAmount: '',
                        Status: 'Recieved'
                    }))
                } else {
                    const tdata = {
                        message: `Please enter valid Item Code or Item Name to search.`,
                        type: 'warn',
                    }
                    dispatchvalue({ type: 'toast', value: tdata });
                    setGrnItemDetials((prev) => ({
                        id: null,
                        pk: null,
                        ItemCode: fieldtype === 'id' ? prev.ItemCode : '',
                        ItemName: fieldtype !== 'id' ? prev.ItemName : '',

                        IsFOCProduct: false,
                        FOCItemCode: '',
                        FOCItemName: '',
                        PurchaseRateTaxable: '',
                        TaxPercentage: '',
                        PurchaseRateWithTax: '',
                        MRP: '',
                        TaxType: '',
                        ReceivedQty: '',
                        FOCQuantity: '',
                        TotalReceivedQty: '',
                        TotalPackQuantity: '',
                        IsMRPAsSellablePrice: true,
                        SellablePrice: '',
                        SellableQtyPrice: '',
                        TotalPackTaxableAmount: '',
                        TotalTaxAmount: '',
                        TotalPackAmount: '',
                        BatchNo: '',
                        IsManufactureDateAvailable: false,
                        ManufactureDate: '',
                        IsExpiryDateAvailable: false,
                        ExpiryDate: '',
                        DiscountMethod: '',
                        DiscountType: '',
                        Discount: '',
                        FinalTotalPackTaxableAmount: '',
                        FinalTotalTaxAmount: '',
                        FinalTotalPackAmount: '',
                        Status: 'Recieved'
                    }))
                }
            } else {
                const tdata = {
                    message: `Please fill atleast any one of the Item Code or Item Name to search.`,
                    type: 'warn',
                }
                dispatchvalue({ type: 'toast', value: tdata });

            }
        } else {
            if (GrnItemDetials.FOCItemCode || GrnItemDetials.FOCItemName) {
                let findadata = FocSupplierProductListData.find(p => "" + p.ItemCode === GrnItemDetials.FOCItemCode)
                if (fieldtype !== 'id') {
                    findadata = FocSupplierProductListData.find(p => "" + p.ItemName === GrnItemDetials.FOCItemName)
                }
                if (findadata) {
                    const { id, SupplierPoductId, ItemCode, ItemName, Status, ...rest } = findadata
                    setGrnItemDetials((prev) => ({
                        ...prev,
                        FOCItemCode: ItemCode,
                        FOCItemName: ItemName
                    }))
                } else {
                    const tdata = {
                        message: `Please enter valid Item Code or Item Name to search.`,
                        type: 'warn',
                    }
                    dispatchvalue({ type: 'toast', value: tdata });
                    setGrnItemDetials((prev) => ({
                        ...prev,
                        FOCItemCode: fieldtype === 'id' ? prev.FOCItemCode : '',
                        FOCItemName: fieldtype !== 'id' ? prev.FOCItemName : '',
                    }))
                }
            } else {
                const tdata = {
                    message: `Please fill atleast any one of the Item Code or Item Name to search.`,
                    type: 'warn',
                }
                dispatchvalue({ type: 'toast', value: tdata });

            }
        }
    }
  
    useEffect(() => {
        let Filtered_with_out_dis_FinalTotalTaxableAmount = 0
        let Filtered_with_out_dis_FinalTotalTaxAmount = 0
        let Filtered_with_out_dis_FinalTotalAmount = 0
        let Filtered_with_dis_FinalTotalTaxableAmount = 0
        let Filtered_with_dis_FinalTotalTaxAmount = 0
        let Filtered_with_dis_FinalTotalAmount = 0
        let TotalTaxableAmount = 0
        let TotalTaxAmount = 0
        let TotalAmount = 0

        let FinalTotalTaxableAmount = 0
        let FinalTotalTaxAmount = 0
        let FinalTotalAmount = 0
        let RoundOffAmount = 0
        let NetAmount = 0
        if (GrnProductListDatas.length !== 0) {
            GrnProductListDatas.forEach(item => {
                TotalTaxableAmount += +item?.TotalPackTaxableAmount;
                TotalTaxAmount += +item?.TotalTaxAmount;
                TotalAmount += +item?.TotalPackAmount;
            })
            GrnProductListDatas.filter(f => f.DiscountMethod === '').forEach(item => {
                Filtered_with_out_dis_FinalTotalTaxableAmount += +item?.FinalTotalPackTaxableAmount;
                Filtered_with_out_dis_FinalTotalTaxAmount += +item?.FinalTotalTaxAmount;
                Filtered_with_out_dis_FinalTotalAmount += +item?.FinalTotalPackAmount;
            })
            GrnProductListDatas.filter(f => f.DiscountMethod !== '').forEach(item => {
                Filtered_with_dis_FinalTotalTaxableAmount += +item?.FinalTotalPackTaxableAmount;
                Filtered_with_dis_FinalTotalTaxAmount += +item?.FinalTotalTaxAmount;
                Filtered_with_dis_FinalTotalAmount += +item?.FinalTotalPackAmount;
            })
        }

        if (
            Filtered_with_out_dis_FinalTotalTaxableAmount &&
            Filtered_with_out_dis_FinalTotalTaxAmount &&
            Filtered_with_out_dis_FinalTotalAmount &&
            GrnSupplierDetials.TotalDiscountMethod &&
            GrnSupplierDetials.TotalDiscountType &&
            GrnSupplierDetials.TotalDiscount
        ) {
            if (GrnSupplierDetials.TotalDiscountMethod === 'BeforeTax') {
                const fixed_taxable_val = Filtered_with_out_dis_FinalTotalTaxableAmount
                const fixed_taxvale = Filtered_with_out_dis_FinalTotalTaxAmount
                if (GrnSupplierDetials.TotalDiscountType === 'Percentage') {
                    Filtered_with_out_dis_FinalTotalTaxableAmount -= Filtered_with_out_dis_FinalTotalTaxableAmount * (+GrnSupplierDetials.TotalDiscount / 100)
                } else {
                    Filtered_with_out_dis_FinalTotalTaxableAmount -= +GrnSupplierDetials.TotalDiscount
                }
                Filtered_with_out_dis_FinalTotalTaxAmount = (Filtered_with_out_dis_FinalTotalTaxableAmount * +fixed_taxvale) / fixed_taxable_val
                Filtered_with_out_dis_FinalTotalAmount = Filtered_with_out_dis_FinalTotalTaxableAmount + Filtered_with_out_dis_FinalTotalTaxAmount
            } else if (GrnSupplierDetials.TotalDiscountMethod === 'AfterTax') {
                if (GrnSupplierDetials.TotalDiscountType === 'Percentage') {
                    Filtered_with_out_dis_FinalTotalAmount -= Filtered_with_out_dis_FinalTotalAmount * (+GrnSupplierDetials.TotalDiscount / 100)
                } else {
                    Filtered_with_out_dis_FinalTotalAmount -= +GrnSupplierDetials.TotalDiscount
                }
            }

        }
        FinalTotalTaxableAmount = Filtered_with_out_dis_FinalTotalTaxableAmount + Filtered_with_dis_FinalTotalTaxableAmount
        FinalTotalTaxAmount = Filtered_with_out_dis_FinalTotalTaxAmount + Filtered_with_dis_FinalTotalTaxAmount
        FinalTotalAmount = Filtered_with_out_dis_FinalTotalAmount + Filtered_with_dis_FinalTotalAmount

        RoundOffAmount = Math.round(FinalTotalAmount) - FinalTotalAmount;
        NetAmount = Math.round(FinalTotalAmount)



        setGrnSupplierDetials((prev) => ({
            ...prev,

            TotalTaxableAmount: TotalTaxableAmount.toFixed(2),
            TotalTaxAmount: TotalTaxAmount.toFixed(2),
            TotalAmount: TotalAmount.toFixed(2),
            FinalTotalTaxableAmount: FinalTotalTaxableAmount.toFixed(2),
            FinalTotalTaxAmount: FinalTotalTaxAmount.toFixed(2),
            FinalTotalAmount: FinalTotalAmount.toFixed(2),
            RoundOffAmount: RoundOffAmount.toFixed(2),
            NetAmount: NetAmount.toFixed(2),
        }))

    }, [
        GrnProductListDatas,
        GrnSupplierDetials.TotalDiscountMethod,
        GrnSupplierDetials.TotalDiscountType,
        GrnSupplierDetials.TotalDiscount,
    ])






    useEffect(() => {

        let purchaserate = parseFloat(GrnItemDetials.PurchaseRateTaxable, 0) || 0;
        let totalAmount
      
        let GSTValue = +GrnItemDetials.TaxPercentage;
        totalAmount = purchaserate + ((purchaserate * GSTValue) / 100);
    
 

        if (GrnItemDetials.TaxPercentage !== '' && GrnItemDetials.MRP !== '') {
            if (parseFloat(GrnItemDetials.MRP) >= totalAmount) {
                const recieved_qty = parseInt(GrnItemDetials.ReceivedQty || 0, 0)
                const total_recieved_qty = recieved_qty + parseInt(GrnItemDetials.FOCQuantity || 0, 0)
                const discount_amount = parseFloat(GrnItemDetials.Discount) || 0
                let mrp_for_leastsellablequantity = 0
                let total_rate_taxable = purchaserate * recieved_qty
                let total_gst = +GrnItemDetials.TaxPercentage === 0 ? 0 : (total_rate_taxable * parseInt(GrnItemDetials.TaxPercentage)) / 100
                let total_rate_with_gst = total_rate_taxable + total_gst
                let grant_total_rate_taxable = 0
                let grant_gst = 0
                let grant_total_rate_with_gst = 0

                if (GrnItemDetials?.PackQuantity && GrnItemDetials?.LeastSellableUnit) {
                    if (parseInt(GrnItemDetials?.PackQuantity || 1) === 1) {
                        mrp_for_leastsellablequantity = parseFloat(GrnItemDetials.SellablePrice)
                    } else {
                        if (parseInt(GrnItemDetials?.LeastSellableUnit || 1) === 1) {
                            mrp_for_leastsellablequantity = parseFloat(GrnItemDetials.SellablePrice) / parseInt(GrnItemDetials?.PackQuantity || 1)
                        } else if (GrnItemDetials.LeastSellableUnit === 'Not Sellable') {
                            mrp_for_leastsellablequantity = parseFloat(GrnItemDetials.SellablePrice) / parseInt(GrnItemDetials?.PackQuantity || 1)
                        } else {
                            mrp_for_leastsellablequantity = parseFloat(GrnItemDetials.SellablePrice)
                        }
                    }
                }

                if (GrnItemDetials?.DiscountMethod === 'BeforeTax') {
                    if (GrnItemDetials.DiscountType === 'Percentage') {
                        grant_total_rate_taxable = total_rate_taxable - (total_rate_taxable * (discount_amount / 100))

                    } else {
                        grant_total_rate_taxable = total_rate_taxable - discount_amount
                    }
                    grant_gst = +GrnItemDetials.TaxPercentage === 0 ? 0 : (grant_total_rate_taxable * parseInt(GrnItemDetials.TaxPercentage)) / 100
                    grant_total_rate_with_gst = grant_total_rate_taxable + grant_gst

                } else if (GrnItemDetials?.DiscountMethod === 'AfterTax') {
                    if (GrnItemDetials.DiscountType === 'Percentage') {
                        grant_total_rate_with_gst = total_rate_with_gst - (total_rate_with_gst * (discount_amount / 100))
                    } else {
                        grant_total_rate_with_gst = total_rate_with_gst - discount_amount
                    }
                    grant_total_rate_taxable = total_rate_taxable
                    grant_gst = +GrnItemDetials.TaxPercentage === 0 ? 0 : (grant_total_rate_taxable * parseInt(GrnItemDetials.TaxPercentage)) / 100

                } else {
                    grant_total_rate_taxable = total_rate_taxable
                    grant_gst = total_gst
                    grant_total_rate_with_gst = total_rate_taxable + total_gst
                }


                setGrnItemDetials((prev) => ({
                    ...prev,
                    PurchaseRateWithTax: totalAmount.toFixed(3),
                    TotalReceivedQty: total_recieved_qty,
                    TotalPackQuantity: GrnItemDetials?.PackQuantity * total_recieved_qty,
                    SellableQtyPrice: mrp_for_leastsellablequantity.toFixed(3),
                    TotalPackTaxableAmount: total_rate_taxable.toFixed(3),
                    TotalTaxAmount: total_gst.toFixed(3),
                    TotalPackAmount: total_rate_with_gst.toFixed(3),
                    FinalTotalPackTaxableAmount: grant_total_rate_taxable.toFixed(3),
                    FinalTotalTaxAmount: grant_gst.toFixed(3),
                    FinalTotalPackAmount: grant_total_rate_with_gst.toFixed(3),

                }))
            } else {
                const tdata = {
                    message: `The purchase rate after GST must be smaller than the MRP ${GrnItemDetials.MRP}.`,
                    type: 'warn',
                }
                dispatchvalue({ type: 'toast', value: tdata });
                setGrnItemDetials((prev) => ({
                    ...prev,
                    PurchaseRateTaxable: '',
                    PurchaseRateWithTax: ''
                }))
            }
        } else {

            setGrnItemDetials((prev) => ({
                ...prev,
                PurchaseRateTaxable: '',
                PurchaseRateWithTax: ''
            }))
        }




    }, [
        GrnItemDetials.TaxPercentage,
        GrnItemDetials.PurchaseRateTaxable,
        GrnItemDetials.MRP,
        GrnItemDetials.SellablePrice,
        GrnItemDetials.ReceivedQty,
        GrnItemDetials.FOCQuantity,
        GrnItemDetials?.PackQuantity,
        GrnItemDetials?.LeastSellableUnit,
        GrnItemDetials.DiscountMethod,
        GrnItemDetials.DiscountType,
        GrnItemDetials.Discount,
        dispatchvalue
    ])

    useEffect(() => {
        let fdata = Object.keys(GrnItemDetials).filter(f => [
            'ItemCode', 'ItemName', 'ProductCategory',
            'SubCategory', 'ManufacturerName', 'GenericName', 'HSNCode', 'PackType',
            'PackQuantity', 'PreviousMRP', 'PreviousPurchaseRateBeforeGST', 'PreviousGST',
            'PreviousPurchaseRateAfterGST', 'LeastSellableUnit'

        ].includes(f))
        setProductListFormOne(fdata)



        let fdata2 = Object.keys(GrnItemDetials).filter(f => ![
            'ItemCode', 'ItemName', 'ProductCategory',
            'SubCategory', 'ManufacturerName', 'GenericName', 'HSNCode', 'PackType',
            'PackQuantity', 'PreviousMRP', 'PreviousPurchaseRateBeforeGST', 'PreviousGST',
            'PreviousPurchaseRateAfterGST', 'LeastSellableUnit', 'id', 'pk', 'Status'

        ].includes(f))

        if (!GrnSupplierDetials.IsFOCAvailable) {
            fdata2 = fdata2.filter(f => !['IsFOCProduct', 'FOCItemCode', 'FOCItemName', 'FOCQuantity'].includes(f))
        }
        if (GrnItemDetials.IsFOCProduct) {
            fdata2 = fdata2.filter(f => !['FOCQuantity'].includes(f))
        }
        if (!GrnItemDetials.IsManufactureDateAvailable) {
            fdata2 = fdata2.filter(f => !['ManufactureDate'].includes(f))
        }
        if (!GrnItemDetials.IsExpiryDateAvailable) {
            fdata2 = fdata2.filter(f => !['ExpiryDate'].includes(f))
        }
        if (GrnItemDetials?.LeastSellableUnit === 'Not Sellable') {
            fdata2 = fdata2.filter(f => !['IsMRPAsSellablePrice', 'SellablePrice', 'SellableQtyPrice'].includes(f))
        }

        if (GrnSupplierDetials.FOCMethod === 'Invoice') {
            fdata2 = fdata2.filter(f => !['FOCItemCode', 'FOCItemName'].includes(f))
            if (GrnItemDetials.IsFOCProduct) {
                fdata2 = fdata2.filter(f => !['PurchaseRateTaxable', 'TaxPercentage', 'PurchaseRateWithTax', 'MRP'].includes(f))
            }
        } else {
            if (!GrnItemDetials.IsFOCProduct) {
                fdata2 = fdata2.filter(f => !['FOCItemCode', 'FOCItemName'].includes(f))
            } else {
                fdata2 = fdata2.filter(f => !['PurchaseRateTaxable', 'TaxPercentage', 'PurchaseRateWithTax', 'MRP'].includes(f))
            }
        }

        setProductListFormTwo(fdata2)
    }, [GrnItemDetials, GrnSupplierDetials.IsFOCAvailable, GrnSupplierDetials.FOCMethod])

    const handlefileOnchange = (e) => {

        const { files } = e.target


        if (files && files.length > 0) {
            let formattedValue = files[0];

            const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
            const maxSize = 5 * 1024 * 1024; // Example max size of 5MB
            if (!allowedTypes.includes(formattedValue.type) || formattedValue.type === '') {

                const tdata = {
                    message: 'Invalid file type. Please upload a PDF, JPEG, or PNG file.',
                    type: 'warn'
                };
                dispatchvalue({ type: 'toast', value: tdata });

            } else {
                if (formattedValue.size > maxSize) {
                    const tdata = {
                        message: 'File size exceeds the limit of 5MB.',
                        type: 'warn'
                    };
                    dispatchvalue({ type: 'toast', value: tdata });

                } else {
                    const reader = new FileReader();
                    reader.onload = () => {
                        setGrnSupplierDetials((prev) => ({
                            ...prev,
                            FileAttachment: reader.result
                        }))

                    };
                    reader.readAsDataURL(formattedValue);
                }
            }

        } else {
            const tdata = {
                message: 'No file selected. Please choose a file to upload.',
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        }

    }



    const Selectedfileview = (fileval) => {

        if (fileval) {
            let tdata = {
                Isopen: false,
                content: null,
                type: 'image/jpg'
            };
            if (['data:image/jpeg;base64', 'data:image/jpg;base64'].includes(fileval?.split(',')[0])) {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'image/jpeg'
                };
            } else if (fileval?.split(',')[0] === 'data:image/png;base64') {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'image/png'
                };
            } else if (fileval?.split(',')[0] === 'data:application/pdf;base64') {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'application/pdf'
                };
            }

            dispatchvalue({ type: 'modelcon', value: tdata });
        } else {
            const tdata = {
                message: 'There is no file to view.',
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        }
    }
    const handelEditGrnProductList = async (params) => {
        try {
            const findsupdata = SupplierData.find(p => p.id === GrnSupplierDetials.SupplierCode)

            const findadata = await axios.get(`${UrlLink}Inventory/Supplier_product_Mapping_link`, {
                params: {
                    SupplierId: findsupdata.id,
                    forquickgrn: true,
                    ItemCode: params.ItemCode,
                    ItemName: params.ItemName,
                }
            })
            const summadata = findadata.data[0]
            const { id, SupplierPoductId,Is_Manufacture_Date_Available,Is_Expiry_Date_Available,ItemCode, ItemName, Status, ...rest } = summadata
            setGrnItemDetials({
                id: params.id,
                ItemCode: ItemCode,
                ItemName: ItemName,
                ...rest,
                IsFOCProduct: params?.IsFOCProduct,
                FOCItemCode: params?.FOCItemCode,
                FOCItemName: params?.FOCItemName,
                PurchaseRateTaxable: params?.PurchaseRateTaxable,
                TaxPercentage: params?.TaxPercentage,
                PurchaseRateWithTax: params?.PurchaseRateWithTax,
                MRP: params?.MRP,
                TaxType: params?.TaxType,
                ReceivedQty: params?.ReceivedQty,
                FOCQuantity: params?.FOCQuantity,
                TotalReceivedQty: params?.TotalReceivedQty,
                TotalPackQuantity: params?.TotalPackQuantity,
                IsMRPAsSellablePrice: params?.IsMRPAsSellablePrice,
                SellablePrice: params?.SellablePrice,
                SellableQtyPrice: params?.SellableQtyPrice,
                TotalPackTaxableAmount: params?.TotalPackTaxableAmount,
                TotalTaxAmount: params?.TotalTaxAmount,
                TotalPackAmount: params?.TotalPackAmount,
                BatchNo: params?.BatchNo,
                IsManufactureDateAvailable: params?.IsManufactureDateAvailable,
                ManufactureDate: params?.ManufactureDate,
                IsExpiryDateAvailable: params?.IsExpiryDateAvailable,
                ExpiryDate: params?.ExpiryDate,
                DiscountMethod: params?.DiscountMethod,
                DiscountType: params?.DiscountType,
                Discount: params?.Discount,
                FinalTotalPackTaxableAmount: params?.FinalTotalPackTaxableAmount,
                FinalTotalTaxAmount: params?.FinalTotalTaxAmount,
                FinalTotalPackAmount: params?.FinalTotalPackAmount,
                Status: 'Recieved'
            })
        } catch (error) {
            console.error(error);

        }
    }

    
    const handelDeleteGrnProductList = (params) => {

        setGrnProductListDatas((prev) =>
            prev.filter(p => p.id !== params.id)
        )

    }

    const GrnProductColumns = [
        ...[
            'id', 'Action', 'ItemCode', 'ItemName', 'IsFOCProduct', 'FOCItemCode', 'FOCItemName', 'PurchaseRateTaxable',
            'TaxPercentage', 'PurchaseRateWithTax', 'MRP', 'TaxType', 'ReceivedQty', 'FOCQuantity',
            'TotalReceivedQty', 'TotalPackQuantity', 'SellableQtyPrice', 'TotalPackTaxableAmount', 'TotalTaxAmount',
            'TotalPackAmount', 'BatchNo', 'ManufactureDate', 'ExpiryDate', 'DiscountMethod', 'DiscountType',
            'Discount', 'FinalTotalPackTaxableAmount', 'FinalTotalTaxAmount', 'FinalTotalPackAmount',
        ].map((field) => ({

            key: field,
            name: field === 'id' ?
                'S.No' :
                field === "IsFOCProduct" ?
                    "Is FOC Product" :
                    field === "FOCItemCode" ?
                        "FOC Item Code" :
                        field === "FOCItemName" ?
                            "FOC Item Name" :
                            field === 'FOCQuantity' ?
                                "FOC Quantity" :
                                formatLabel(field),
            width: ['PurchaseRateTaxable', 'TaxPercentage',
                'PurchaseRateWithTax', 'TotalPackTaxableAmount',
                'FinalTotalPackTaxableAmount', 'FinalTotalTaxAmount',
                'FinalTotalPackAmount', 'Action'
            ].includes(field) && 200,
            renderCell: (params) => (
                field === "Action" ? (
                    <>
                        <Button className="cell_btn" onClick={() => handelEditGrnProductList(params.row)}>
                            <EditIcon className="check_box_clrr_cancell" />
                        </Button>
                        <Button className="cell_btn" onClick={() => handelDeleteGrnProductList(params.row)}>
                            <DeleteIcon className="check_box_clrr_cancell" />
                        </Button>
                    </>

                ) :
                    field === 'IsFOCProduct' ?
                        params.row[field] ? 'Yes' : 'No'
                        : params.row[field] ?
                            params.row[field] :
                            '-'
            )

        }))
    ]

    const handleAddGrnProductList = () => {
        let requiredFields = Object.keys(GrnItemDetials).filter(p => ![
            'id', 'pk', 'FOCQuantity', 'ProductCategory',
            'SubCategory', 'CompanyName', 'GenericName', 'HSNCode', 'PackType',
            'PackQuantity', 'PreviousMRP', 'PreviousPurchaseRateBeforeGST', 'PreviousGST',
            'PreviousPurchaseRateAfterGST', 'LeastSellableUnit', 'IsFOCProduct', 'DiscountMethod',
            'IsManufactureDateAvailable', 'IsExpiryDateAvailable','TaxType'
        ].includes(p))
        if(+GrnItemDetials.TaxPercentage !==0){
            requiredFields.push('TaxType')
        }
        if (!GrnItemDetials.IsManufactureDateAvailable) {
            requiredFields = requiredFields.filter(f => f !== 'ManufactureDate')
        }
        if (!GrnItemDetials.IsExpiryDateAvailable) {
            requiredFields = requiredFields.filter(f => f !== 'ExpiryDate')
        }
        if (+GrnItemDetials.TaxPercentage === 0) {
            requiredFields = requiredFields.filter(f => !['TotalTaxAmount', 'FinalTotalTaxAmount'].includes(f))
        }
        if (!GrnItemDetials.IsFOCProduct) {
            requiredFields = requiredFields.filter(f => !['FOCItemCode', 'FOCItemName'].includes(f))
        }
        if (!GrnItemDetials.DiscountMethod) {
            requiredFields = requiredFields.filter(f => !['Discount', 'DiscountType'].includes(f))
        }
        const missingFields = requiredFields.filter(f => !GrnItemDetials[f])
        if (missingFields.length !== 0) {
            const tdata = {
                message: `Please fill out all required fields: ${missingFields.join(', ')}`,
                type: 'warn'
            }
            dispatchvalue({ type: 'toast', value: tdata })
        } else {
            const CheckDublicate = GrnProductListDatas.some((ele) => ele.ItemCode === GrnItemDetials.ItemCode && ele.BatchNo === GrnItemDetials.BatchNo && +ele.id !== +GrnItemDetials.id)
            if (CheckDublicate) {

                dispatchvalue({
                    type: 'toast',
                    value: {
                        message: `This item with the same batch number has already been entered.`,
                        type: 'warn',
                    },
                });


            } else {
                if (GrnItemDetials.id) {

                    setGrnProductListDatas((prev) =>
                        prev.map((product) => +product.id === +GrnItemDetials.id ? { ...GrnItemDetials } : product)
                    )
                    clearGrnItemsList()

                } else {
                    setGrnProductListDatas((prev) => ([
                        ...prev,
                        {
                            ...GrnItemDetials,
                            id: prev.length + 1
                        }
                    ]))

                    clearGrnItemsList()
                }
                setGrnSupplierDetials((prev) => ({
                    ...prev,
                    TotalDiscountMethod: '',
                    TotalDiscountType: '',
                    TotalDiscount: '',
                }))

            }

        }
    }
    const handlesaveQuickGrn = () => {
        let requiredFields = Object.keys(GrnSupplierDetials).filter(f => ![
            'IsOldGRN', 'IsFOCAvailable', 'pk', 'TotalDiscountMethod', 'FileAttachment'
        ].includes(f))
        if (!GrnSupplierDetials.TotalDiscountMethod) {
            requiredFields = requiredFields.filter(f => !['TotalDiscountType', 'TotalDiscount'].includes(f))
        }
        const missingFields = requiredFields.filter(f => !GrnSupplierDetials[f])
        if (missingFields.length === 0) {
            if (+GrnSupplierDetials.SupplierBillAmount === +GrnSupplierDetials.NetAmount) {
                const senddata = {
                    IsQuickGRN: true,
                    ...GrnSupplierDetials,
                    Created_by: userRecord?.username,
                    GrnItemList: GrnProductListDatas
                }
                console.log(senddata);

                axios.post(`${UrlLink}Inventory/Goods_Reciept_Note_Details_link`, senddata)
                    .then((res) => {
                        console.log(res);
                        let data = res.data

                        let type = Object.keys(data)[0]
                        let mess = Object.values(data)[0]
                        const tdata = {
                            message: mess,
                            type: type
                        }
                        dispatchvalue({ type: 'toast', value: tdata })
                        navigate('/Home/GoodsReceiptNoteList')
                    })
                    .catch((err) => {
                        console.error(err);
                    })
            } else {
                const tdata = {
                    message: ` Supplier Bill Amount doesnot match with the Net Amount ,cross check the product detials and verify it properly.`,
                    type: 'warn'
                }
                dispatchvalue({ type: 'toast', value: tdata })
            }
        } else {
            const tdata = {
                message: `Please fill out all required fields: ${missingFields.join(', ')}`,
                type: 'warn'
            }
            dispatchvalue({ type: 'toast', value: tdata })
        }
    }
    return (
        <>
            <div className="Main_container_app">
                <h3>Quick Goods Receipt Note</h3>
                <br />
                <div className="RegisFormcon_1">
                    {
                        Object.keys(GrnSupplierDetials).filter(p => ![
                            'Status', 'pk', 'TotalTaxableAmount',
                            'TotalTaxAmount', 'TotalAmount', 'TotalDiscountMethod',
                            'TotalDiscountType', 'TotalDiscount', 'FinalTotalTaxableAmount',
                            'FinalTotalTaxAmount', 'FinalTotalAmount', 'RoundOffAmount', 'NetAmount'
                        ].includes(p)).filter(p => !GrnSupplierDetials.IsFOCAvailable ? p !== 'FOCMethod' : p).map((field, Index) => {
                            return (
                                <div className="RegisForm_1" key={Index + 'key'}>

                                    <label htmlFor={field}>
                                        {
                                            field === 'GRNDate' ?
                                                'GRN Date' :
                                                field === 'IsFOCAvailable' ?
                                                    "Is FOC Available" :
                                                    field === 'FOCMethod' ?
                                                        "FOC Method" : formatLabel(field)
                                        }
                                        <span>:</span>
                                    </label>


                                    {
                                        field === 'StoreLocation' || field === 'FOCMethod' ?

                                            <select
                                                id={field}
                                                name={field}
                                                value={GrnSupplierDetials[field]}
                                                onChange={HandeleOnchange}

                                            >
                                                <option value=''>Select</option>
                                                {field === 'StoreLocation' &&
                                                    StoreLocationData.map((ele, ind) => (
                                                        <option key={ind + 'key'} value={ele.id} >{ele.StoreName}</option>
                                                    ))
                                                }
                                                {field === 'FOCMethod' &&
                                                    ['Invoice', 'Individual Item'].map((ele, ind) => (
                                                        <option key={ind + 'key'} value={ele} >{"For " + ele}</option>
                                                    ))
                                                }
                                            </select>
                                            : field === 'IsOldGRN' || field === 'IsFOCAvailable' ?
                                                (<div style={{ display: 'flex', justifyContent: 'flex-start', gap: '10px', width: '150px' }}>
                                                    <label style={{ width: 'auto' }} htmlFor={`${field}_yes`}>
                                                        <input
                                                            required
                                                            id={`${field}_yes`}
                                                            type="radio"
                                                            name={field}
                                                            value='Yes'
                                                            style={{ width: '15px' }}
                                                            checked={GrnSupplierDetials[field]}
                                                            onChange={HandeleOnchange}

                                                        />
                                                        Yes
                                                    </label>
                                                    <label style={{ width: 'auto' }} htmlFor={`${field}_No`}>
                                                        <input
                                                            required
                                                            id={`${field}_No`}
                                                            type="radio"
                                                            name={field}
                                                            value='No'
                                                            style={{ width: '15px' }}
                                                            checked={!GrnSupplierDetials[field]}
                                                            onChange={HandeleOnchange}
                                                        />
                                                        No
                                                    </label>
                                                </div>
                                                ) : field === 'FileAttachment' ?
                                                    <>
                                                        <input
                                                            type='file'
                                                            name={field}
                                                            accept='image/jpeg,image/png,application/pdf'
                                                            required
                                                            id={`${field}_Grn`}
                                                            autoComplete='off'
                                                            onChange={handlefileOnchange}
                                                            style={{ display: 'none' }}
                                                        />
                                                        <div style={{ width: '150px', display: 'flex', justifyContent: 'space-around' }}>
                                                            <label
                                                                htmlFor={`${field}_Grn`}
                                                                className="RegisterForm_1_btns choose_file_update"
                                                            >
                                                                Choose File
                                                            </label>
                                                            <button className='fileviewbtn'
                                                                onClick={() => Selectedfileview(GrnSupplierDetials.FileAttachment)}
                                                            >view</button>

                                                        </div>
                                                    </>
                                                    :
                                                    <>
                                                        <div className='Search_patient_icons'>


                                                            <input
                                                                type={['GRNDate', 'SupplierBillDate', 'SupplierBillDueDate'].includes(field) ? 'date' : 'text'}
                                                                id={field}
                                                                list={['SupplierCode', 'SupplierName'].includes(field) ? field + 'grn_supplier_list' : null}
                                                                name={field}
                                                                value={GrnSupplierDetials[field]}
                                                                onChange={HandeleOnchange}
                                                                min={field === 'SupplierBillDueDate' ? GrnSupplierDetials.SupplierBillDate : ''}
                                                                max={['SupplierBillDate', 'GRNDate'].includes(field) ? currentDate : ''}
                                                                disabled={
                                                                    ['SupplierBillDueDate', 'GRNDate', 'ContactPerson', 'ContactNumber', 'EmailAddress'].filter(f => GrnSupplierDetials.IsOldGRN ? !['GRNDate', 'SupplierBillDueDate'].includes(f) : f).includes(field)
                                                                }
                                                            />
                                                            {
                                                                ['SupplierCode', 'SupplierName'].includes(field) &&
                                                                (<>
                                                                    <datalist id={field + 'grn_supplier_list'}>
                                                                        {field === 'SupplierCode' &&
                                                                            SupplierData.map((ele, ind) => (
                                                                                <option key={ind + 'key'} value={ele.id} >{`${ele.SupplierName} | ${ele.ContactNo}`}</option>
                                                                            ))
                                                                        }
                                                                        {field === 'SupplierName' &&
                                                                            SupplierData.map((ele, ind) => (
                                                                                <option key={ind + 'key'} value={ele.SupplierName} >{`${ele.id} | ${ele.ContactNo}`}</option>
                                                                            ))
                                                                        }
                                                                    </datalist>
                                                                    <span onClick={(e) => handlesearchsupplierlist(field)}>
                                                                        <ManageSearchIcon />
                                                                    </span>
                                                                </>

                                                                )
                                                            }
                                                        </div>

                                                    </>



                                    }
                                </div>

                            )
                        })
                    }
                </div>
                <br />
                <div className="common_center_tag">
                    <span>Product Details</span>
                </div>
                <br />
                <div className="RegisFormcon_1">
                    {
                        ProductListFormOne.map((field, Index) => (
                            <div className="RegisForm_1" key={Index + 'key'}>
                                <label htmlFor={field}>
                                    {
                                        formatLabel(field)
                                    }
                                    <span>:</span>
                                </label>
                                {
                                    <div className='Search_patient_icons'>

                                        <input
                                            type={'text'}
                                            id={field}
                                            list={['ItemCode', 'ItemName'].includes(field) ? field + 'grn_supplier_Product_list' : null}
                                            name={field}
                                            disabled={!(GrnSupplierDetials.SupplierCode && GrnSupplierDetials.SupplierName) ? true : !['ItemCode', 'ItemName'].includes(field)}
                                            autoComplete='off'
                                            value={GrnItemDetials[field]}
                                            onChange={HandeleOnchangeItemDetials}


                                        />
                                        {
                                            ['ItemCode', 'ItemName'].includes(field) &&
                                            (
                                                <>
                                                    <datalist id={field + 'grn_supplier_Product_list'}>
                                                        {field === 'ItemCode' &&
                                                            SupplierProductListData.map((ele, ind) => (
                                                                <option key={ind + 'key'} value={ele.ItemCode} >{`${ele.ItemName}`}</option>
                                                            ))
                                                        }
                                                        {field === 'ItemName' &&
                                                            SupplierProductListData.map((ele, ind) => (
                                                                <option key={ind + 'key'} value={ele.ItemName} >{`${ele.ItemCode}`}</option>
                                                            ))
                                                        }
                                                    </datalist>
                                                    <span onClick={(e) => handlesearchitemslist('normal', field === 'ItemCode' ? 'id' : 'name')}>
                                                        <ManageSearchIcon />
                                                    </span>
                                                </>
                                            )
                                        }
                                    </div>
                                }
                            </div>
                        ))
                    }
                </div>
                <br />
                {GrnItemDetials.ItemCode && GrnItemDetials.ItemName &&
                    <>
                        <div className="common_center_tag">
                            <span>Product Entry Details</span>
                        </div>
                        <br />
                        <div className="RegisFormcon_1">
                            {
                                ProductListFormTwo.map((field, indx) => (
                                    <div className="RegisForm_1" key={indx + 'key'}>
                                        <label htmlFor={field}>
                                            {
                                                field === "IsFOCProduct" ?
                                                    "Is FOC Product" :
                                                    field === "FOCItemCode" ?
                                                        "FOC Item Code" :
                                                        field === "FOCItemName" ?
                                                            "FOC Item Name" :
                                                            field === 'FOCQuantity' ?
                                                                "FOC Quantity" :
                                                                field === 'IsMRPAsSellablePrice' ?
                                                                    'Is MRP As Sellable Price' :
                                                                    formatLabel(field)
                                            }
                                            <span>:</span>
                                        </label>
                                        {['IsFOCProduct', 'IsMRPAsSellablePrice', 'IsManufactureDateAvailable', 'IsExpiryDateAvailable'].includes(field) ?
                                            (<div style={{ display: 'flex', justifyContent: 'flex-start', gap: '10px', width: '150px' }}>
                                                <label style={{ width: 'auto' }} htmlFor={`${field}_yes`}>
                                                    <input
                                                        required
                                                        id={`${field}_yes`}
                                                        type="radio"
                                                        name={field}
                                                        value='Yes'
                                                        style={{ width: '15px' }}
                                                        checked={GrnItemDetials[field]}
                                                        onChange={HandeleOnchangeItemDetials}
                                                        disabled={['IsManufactureDateAvailable', 'IsExpiryDateAvailable'].includes(field)}

                                                    />
                                                    Yes
                                                </label>
                                                <label style={{ width: 'auto' }} htmlFor={`${field}_No`}>
                                                    <input
                                                        required
                                                        id={`${field}_No`}
                                                        type="radio"
                                                        name={field}
                                                        value='No'
                                                        style={{ width: '15px' }}
                                                        checked={!GrnItemDetials[field]}
                                                        onChange={HandeleOnchangeItemDetials}
                                                        disabled={['IsManufactureDateAvailable', 'IsExpiryDateAvailable'].includes(field)}
                                                    />
                                                    No
                                                </label>
                                            </div>
                                            ) : ['TaxType', 'TaxPercentage', 'DiscountMethod', 'DiscountType'].includes(field) ?
                                                <select
                                                    id={field}
                                                    name={field}
                                                    value={GrnItemDetials[field]}
                                                    disabled={!GrnItemDetials.DiscountMethod && field === 'DiscountType'}
                                                    onChange={HandeleOnchangeItemDetials}

                                                >
                                                    {["DiscountMethod", 'DiscountType'] && <option value=''>Not Applicable</option>}
                                                    {field === 'TaxType' &&
                                                        ['GST', 'IGST'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                    {field === 'TaxPercentage' &&
                                                        ['0', '5', '12', '18', '28'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                    {field === 'DiscountMethod' &&
                                                        ['BeforeTax', 'AfterTax'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                    {field === 'DiscountType' &&
                                                        ['Percentage', 'Cash'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                </select>
                                                :
                                                <div className='Search_patient_icons'>
                                                    <input
                                                        type={['ManufactureDate', 'ExpiryDate'].includes(field) ? "date" : ['PurchaseRateTaxable', 'MRP', 'ReceivedQty', 'FOCQuantity', 'Discount'].includes(field) ? 'number' : 'text'}
                                                        id={field}
                                                        list={['FOCItemCode', 'FOCItemName'].includes(field) ? field + 'grn_supplier_Foc_Product_list' : null}
                                                        name={field}
                                                        autoComplete='off'
                                                        min={field === 'ExpiryDate' ? currentDate : ''}
                                                        max={field === 'ManufactureDate' ? currentDate : ''}
                                                        disabled={['PurchaseRateWithTax', 'TotalReceivedQty', 'TotalPackQuantity', 'SellableQtyPrice',
                                                            'TotalPackTaxableAmount', 'TotalTaxAmount', 'TotalPackAmount', 'Discount',
                                                            'FinalTotalPackTaxableAmount', 'FinalTotalTaxAmount', 'FinalTotalPackAmount'
                                                        ].filter(f => GrnItemDetials.DiscountMethod ? f !== 'Discount' : f).includes(field) ? true : GrnItemDetials.IsMRPAsSellablePrice && field === 'SellablePrice' && true}
                                                        onKeyDown={['MRP', 'ReceivedQty', 'FOCQuantity', 'Discount'].includes(field) ? BlockInvalidcharecternumber : null}
                                                        value={GrnItemDetials[field]}
                                                        onChange={HandeleOnchangeItemDetials}
                                                    />
                                                    {
                                                        ['FOCItemCode', 'FOCItemName'].includes(field) &&
                                                        (<>
                                                            <datalist id={field + 'grn_supplier_Foc_Product_list'}>
                                                                {field === 'FOCItemCode' &&
                                                                    FocSupplierProductListData.map((ele, ind) => (
                                                                        <option key={ind + 'key'} value={ele.ItemCode} >{`${ele.ItemName}`}</option>
                                                                    ))
                                                                }
                                                                {field === 'FOCItemName' &&
                                                                    FocSupplierProductListData.map((ele, ind) => (
                                                                        <option key={ind + 'key'} value={ele.ItemName} >{`${ele.ItemCode}`}</option>
                                                                    ))
                                                                }
                                                            </datalist>
                                                            <span onClick={(e) => handlesearchitemslist('FOC', field === 'FOCItemCode' ? 'id' : 'name')}>
                                                                <ManageSearchIcon />
                                                            </span>
                                                        </>
                                                        )
                                                    }
                                                </div>
                                        }
                                    </div>
                                ))
                            }
                        </div>
                        <br />
                        <div className="Main_container_Btn">
                            <button onClick={handleAddGrnProductList}>
                                {GrnItemDetials.id ? 'Update' : 'Add'}
                            </button>
                        </div>

                    </>
                }
                <br />
                {GrnProductListDatas.length !== 0 &&
                    <>
                        < ReactGrid columns={GrnProductColumns} RowData={GrnProductListDatas} />
                        <br />

                        <div className="RegisFormcon_1">
                            {
                                Object.keys(GrnSupplierDetials).filter(p => ['TotalTaxableAmount',
                                    'TotalTaxAmount', 'TotalAmount', 'TotalDiscountMethod',
                                    'TotalDiscountType', 'TotalDiscount', 'FinalTotalTaxableAmount',
                                    'FinalTotalTaxAmount', 'FinalTotalAmount', 'RoundOffAmount', 'NetAmount'
                                ].includes(p)).map((field, index) => (
                                    <div className="RegisForm_1" key={index + 'key'}>
                                        <label htmlFor={field}>
                                            {
                                                formatLabel(field)
                                            }
                                            <span>:</span>
                                        </label>
                                        {
                                            ['TotalDiscountMethod', 'TotalDiscountType'].includes(field) ?
                                                <select
                                                    name={field}
                                                    id={field}
                                                    value={GrnSupplierDetials[field]}
                                                    onChange={HandeleOnchange}
                                                    disabled={field === 'TotalDiscountMethod' ? !GrnProductListDatas.some(f => f.DiscountMethod === '') : !GrnSupplierDetials['TotalDiscountMethod']}
                                                >
                                                    <option value=''>Not Applicable</option>
                                                    {field === 'TotalDiscountMethod' &&
                                                        ['BeforeTax', 'AfterTax'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                    {field === 'TotalDiscountType' &&
                                                        ['Percentage', 'Cash'].map((ele, ind) => (
                                                            <option key={ind + 'key'} value={ele} >{ele}</option>
                                                        ))
                                                    }
                                                </select>
                                                :
                                                <input
                                                    type={field === 'TotalDiscount' ? 'number' : "text"}
                                                    name={field}
                                                    id={field}
                                                    disabled={field !== 'TotalDiscount' ? true : !GrnSupplierDetials['TotalDiscountType']}
                                                    onKeyDown={['TotalDiscount'].includes(field) ? BlockInvalidcharecternumber : null}
                                                    value={GrnSupplierDetials[field]}
                                                    onChange={HandeleOnchange}
                                                />
                                        }
                                    </div>

                                ))

                            }
                        </div>
                        <br />
                        <div className="Main_container_Btn">
                            <button onClick={handlesaveQuickGrn}>
                                {GrnSupplierDetials.pk ? 'Update GRN' : 'Save GRN'}
                            </button>
                        </div>
                    </>

                }

            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />

            <ModelContainer />
        </>
    )
}

export default QuickGoodsRecieptNote