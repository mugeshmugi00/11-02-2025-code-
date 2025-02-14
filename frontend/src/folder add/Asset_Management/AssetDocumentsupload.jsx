import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Button } from '@mui/material';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from 'react-router-dom'; // Updated to useNavigate
import axios from 'axios';


const AssetDocumentsupload = () => {

    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const [RackMasterPage, setRackMasterPage] = useState('AssetDocumentsupload')

    // const [categories, setCategories] = useState([]);
    // const [subcategories, setSubcategories] = useState([]);
    // const [assets, setAssets] = useState([]);
    // const [selectedCategory, setSelectedCategory] = useState('');
    // const [selectedSubcategory, setSelectedSubcategory] = useState('');
    // const [selectedAsset, setSelectedAsset] = useState('');
    // const [documentType, setDocumentType] = useState('');
    // const [documents, setDocuments] = useState([]);
    // const [file, setFile] = useState(null);
    // const [description, setDescription] = useState('');
    // const [message, setMessage] = useState('');
    // const [isLoading, setIsLoading] = useState(false);
    // const [showDocuments, setShowDocuments] = useState(false);
    // const [showAlert, setShowAlert] = useState(false);
    // // Fetch categories on component mount
    // useEffect(() => {
    //     fetchCategories();
    // }, []);

    // // Fetch categories
    // const fetchCategories = async () => {
    //     try {
    //         const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
    //         setCategories(response.data);
    //     } catch (error) {
    //         console.error('Error fetching categories:', error);
    //         setMessage('Failed to fetch categories.');
    //     }
    // };

    // // Handle category change and fetch subcategories
    // const handleCategoryChange = async (categoryId) => {
    //     setSelectedCategory(categoryId);
    //     setSelectedSubcategory('');
    //     setAssets([]);
    //     setShowDocuments(false);

    //     try {
    //         const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/?category_id=${categoryId}`);
    //         setSubcategories(response.data);
    //     } catch (error) {
    //         console.error('Error fetching subcategories:', error);
    //         setMessage('Failed to fetch subcategories.');
    //     }
    // };

    // const handleSubcategoryChange = async (subcategoryId) => {
    //     setSelectedSubcategory(subcategoryId);
    //     setShowDocuments(false);
    //     try {
    //         const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories?category=${selectedCategory}&subcategory=${subcategoryId}`);
    //         setAssets(response.data);
    //     } catch (error) {
    //         console.error('Error fetching assets:', error);
    //     }
    // };
    // const handleSelectedAsset = async (assetId) => {
    //     try {
    //         const response = await axios.get(`${UrlLink}AccetCategory/Asset_Reg_Get?id=${assetId}`);
    //         if (response.data && response.data.length > 0) {
    //             const asset = response.data[0];
    //             setSelectedAsset(assetId);
    //             setAssets(response.data)
    //             setShowDocuments(false);

    //         }
    //     } catch (error) {
    //         console.error('Error fetching assets:', error);
    //     }
    // };

    // useEffect(() => {
    //     if (selectedAsset) {
    //         fetchDocuments();
    //     }
    // }, [selectedAsset]);


    // const handleFileChange = (e) => {
    //     const selectedFile = e.target.files[0];
    //     if (selectedFile) {
    //         // Check file size (e.g., 5MB limit)
    //         if (selectedFile.size > 5 * 1024 * 1024) {
    //             setMessage('File size should be less than 5MB');
    //             e.target.value = '';
    //             return;
    //         }
    //         setFile(selectedFile);
    //         setMessage('');
    //     }
    // };

    // const fetchDocuments = async () => {
    //     if (!selectedAsset) {
    //         setMessage('Please select an asset to fetch documents.');
    //         return;
    //     }

    //     try {
    //         setIsLoading(true);
    //         const response = await axios.get(`${UrlLink}AccetCategory/assetdocumentsuploadget`, {
    //             params: { asset_code: selectedAsset }
    //         });

    //         if (Array.isArray(response.data)) {
    //             setDocuments(response.data);
    //             setShowDocuments(true);
    //             if (response.data.length === 0) {
    //                 setMessage('No documents found for the selected asset.');
    //             }
    //         } else {
    //             setMessage('Invalid response format from server.');
    //         }
    //     } catch (error) {
    //         console.error('Error fetching documents:', error);
    //         setMessage(error.response?.data?.error || 'Failed to fetch documents.');
    //     } finally {
    //         setIsLoading(false);
    //     }
    // };

    // // -----------
    // const handleSubmit = async (e) => {
    //     e.preventDefault();
    //     setIsLoading(true);
    //     setMessage('');

    //     if (!selectedAsset || !documentType || !file || !selectedCategory || !selectedSubcategory) {
    //         setMessage('Please fill all required fields.');
    //         setIsLoading(false);
    //         return;
    //     }

    //     const formData = new FormData();
    //     formData.append('file', file);
    //     formData.append('asset', selectedAsset); // This should be the asset ID
    //     formData.append('document_type', documentType);
    //     formData.append('description', description || '');
    //     formData.append('category', selectedCategory);
    //     formData.append('subcategory', selectedSubcategory);

    //     try {
    //         const response = await axios.post(
    //             `${UrlLink}AccetCategory/assetdocumentsuploadpost`,
    //             formData,
    //             {
    //                 headers: {
    //                     'Content-Type': 'multipart/form-data',
    //                 },
    //             }
    //         );

    //         if (response.data.message) {
    //             setShowAlert(true);
    //             setMessage('Document uploaded successfully!');
    //             setDocumentType('');
    //             setFile(null);
    //             setDescription('');
    //             const fileInput = document.querySelector('input[type="file"]');
    //             if (fileInput) fileInput.value = '';

    //             await fetchDocuments();
    //         }
    //     } catch (error) {
    //         console.error('Error uploading document:', error);
    //         setMessage(error.response?.data?.error || 'Failed to upload document.');
    //     } finally {
    //         setIsLoading(false);
    //     }
    // };
    const [categories, setCategories] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [assets, setAssets] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [selectedAsset, setSelectedAsset] = useState('');
    const [documentType, setDocumentType] = useState('');
    const [documents, setDocuments] = useState([]);
    const [file, setFile] = useState(null);
    const [description, setDescription] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [showDocuments, setShowDocuments] = useState(false);
    const [showAlert, setShowAlert] = useState(false);

    useEffect(() => {
        fetchCategories();
    }, []);

    const fetchCategories = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
            setCategories(response.data);
        } catch (error) {
            console.error('Error fetching categories:', error);
            setMessage('Failed to fetch categories.');
        }
    };

    const handleCategoryChange = async (categoryId) => {
        setSelectedCategory(categoryId);
        setSelectedSubcategory('');
        setSelectedAsset('');
        setAssets([]);
        setShowDocuments(false);
        setDocuments([]);
    
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/?category_id=${categoryId}`);
            setSubcategories(response.data); // No need to filter; backend handles it
        } catch (error) {
            console.error('Error fetching subcategories:', error);
            setMessage('Failed to fetch subcategories.');
        }
    };

    const handleSubcategoryChange = async (subcategoryId) => {
        setSelectedSubcategory(subcategoryId);
        setSelectedAsset('');
        setShowDocuments(false);
        setDocuments([]);
    
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_assets/?subcategory_id=${subcategoryId}`);
            setAssets(response.data); 
            console.log("response:",response)
        } catch (error) {
            console.error('Error fetching assets:', error);
            setMessage('Failed to fetch assets.');
        }
    };

    const handleSelectedAsset = (assetId) => {
        setSelectedAsset(assetId);
        setShowDocuments(false);
        setDocuments([]);
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            if (selectedFile.size > 5 * 1024 * 1024) {
                setMessage('File size should be less than 5MB');
                e.target.value = '';
                return;
            }
            setFile(selectedFile);
            setMessage('');
        }
    };

    const fetchDocuments = async () => {
        if (!selectedAsset) {
            setMessage('Please select an asset to fetch documents.');
            return;
        }

        try {
            setIsLoading(true);
            const response = await axios.get(`${UrlLink}AccetCategory/assetdocumentsuploadget`, {
                params: { asset_code: selectedAsset }
            });

            if (Array.isArray(response.data)) {
                setDocuments(response.data);
                setShowDocuments(true);
                if (response.data.length === 0) {
                    setMessage('No documents found for the selected asset.');
                }
            } else {
                setMessage('Invalid response format from server.');
            }
        } catch (error) {
            console.error('Error fetching documents:', error);
            setMessage(error.response?.data?.error || 'Failed to fetch documents.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        setMessage('');

        if (!selectedAsset || !documentType || !file || !selectedCategory || !selectedSubcategory) {
            setMessage('Please fill all required fields.');
            setIsLoading(false);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('asset', selectedAsset);
        formData.append('document_type', documentType);
        formData.append('description', description || '');
        formData.append('category', selectedCategory);
        formData.append('subcategory', selectedSubcategory);

        try {
            const response = await axios.post(
                `${UrlLink}AccetCategory/assetdocumentsuploadpost`,
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );

            if (response.data.message) {
                setShowAlert(true);
                setMessage('Document uploaded successfully!');
                setTimeout(() => setShowAlert(false), 3000);
                setDocumentType('');
                setFile(null);
                setDescription('');
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) fileInput.value = '';
                setShowDocuments(false);
                setDocuments([]);
            }
        } catch (error) {
            console.error('Error uploading document:', error);
            setMessage(error.response?.data?.error || 'Failed to upload document.');
        } finally {
            setIsLoading(false);
        }
    };
    // ----------------------------------------------------------------------------
    // ------------------------------Asset document List--------------------------------
    // const [availableAssets, setAvailableAssets] = useState([]);
    // const [currentAssetCode, setCurrentAssetCode] = useState('');
    // const [selectedDocCategory, setSelectedDocCategory] = useState('');
    // const [assetDocuments, setAssetDocuments] = useState([]);
    // const [activeDocumentPreview, setActiveDocumentPreview] = useState(null); // Track selected document

    // const navigate = useNavigate(); // Updated to use useNavigate

    // useEffect(() => {
    //     const fetchAssets = async () => {
    //         try {
    //             const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
    //             setAvailableAssets(response.data);
    //         } catch (error) {
    //             console.error('Error fetching assets:', error);
    //         }
    //     };
    //     fetchAssets();
    // }, []);

    // const fetchDocumentsAsset = async () => {
    //     try {
    //         const response = await axios.get(`http://localhost:8000/api/asset-documents/by-asset/`, {
    //             params: {
    //                 asset_code: currentAssetCode,
    //                 document_type: selectedDocCategory,
    //             }
    //         });
    //         setAssetDocuments(response.data);
    //     } catch (error) {
    //         console.error('Error fetching documents:', error);
    //     }
    // };

    // const handleSearch = (e) => {
    //     e.preventDefault();
    //     fetchDocumentsAsset();
    // };

    // const viewDocument = (document) => {
    //     // Instead of embedding, open the document in a new tab
    //     window.open(document.file, '_blank');
    // };

    // const closeDocumentView = () => {
    //     setActiveDocumentPreview(null); // Close document view by setting it to null
    //     navigate('/dashboard'); // Navigate back to dashboard using useNavigate
    // };

    // ------------------------------------------------------------------------------------
    return (
        <>
            <div className="Main_container_app">
                <h3>Asset Documents</h3>

                <br />
                <div className="RegisterTypecon">
                    <div className="RegisterType">

                        {["AssetDocumentsupload", "AssetDocumentList"].map((p, ind) => (

                            <div className="registertypeval" key={ind}>
                                <input
                                    type="radio"
                                    id={p}
                                    name="appointment_type"
                                    checked={RackMasterPage === p}
                                    onChange={(e) => {
                                        setRackMasterPage(e.target.value)
                                    }}
                                    value={p}
                                />
                                <label htmlFor={p}>
                                    {p}
                                </label>
                            </div>
                        ))}

                    </div>
                </div>
                {/* ----------------------Asset Document Uplode---------------------- */}
                {RackMasterPage === 'AssetDocumentsupload' && <>
                    <br />
                    <div>
                        <div className="Main_container_app">

                            <div className="RegisFormcon_1">
                                <div className="RegisForm_1">
                                    <label>Select Category:</label>
                                    <select
                                        value={selectedCategory}
                                        onChange={(e) => handleCategoryChange(e.target.value)}
                                        required
                                    >
                                        <option value="">Select a Category</option>
                                        {categories.map((category) => (
                                            <option key={category.id} value={category.id}>
                                                {category.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="RegisForm_1">
                                    <label>Select Subcategory:</label>
                                    <select
                                        value={selectedSubcategory}
                                        onChange={(e) => handleSubcategoryChange(e.target.value)}
                                        disabled={!selectedCategory}
                                        required
                                    >
                                        <option value="">Select a Subcategory</option>
                                        {subcategories.map((subcategory) => (
                                            <option key={subcategory.id} value={subcategory.id}>
                                                {subcategory.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>

                                <div className="RegisForm_1">
                                    <label>Select Asset:</label>
                                    <select
                                        value={selectedAsset}
                                        onChange={(e) => handleSelectedAsset(e.target.value)}
                                        disabled={!selectedSubcategory}
                                        required
                                    >
                                        <option value="">Select an Asset</option>
                                        {assets.map((asset) => (
                                            <option key={asset.id} value={asset.id}>
                                                {asset.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            {/* Document Upload Section */}
                            <div className="RegisFormcon_1">
                                <div className="RegisForm_1">
                                    <label>Document Type:</label>
                                    <select
                                        value={documentType}
                                        onChange={(e) => setDocumentType(e.target.value)}
                                        required
                                    >
                                        <option value="">Select Document Type</option>
                                        <option value="INVOICE">Invoice</option>
                                        <option value="WARRANTY">Warranty Card</option>
                                        <option value="MANUAL">User Manual</option>
                                        <option value="CERTIFICATE">Certificate</option>
                                        <option value="CONTRACT">Contract</option>
                                        <option value="REPORT">Inspection Report</option>
                                        <option value="OTHER">Other</option>
                                    </select>
                                </div>

                                <div className="RegisForm_1">
                                    <label>File:</label>
                                    <input
                                        type="file"
                                        onChange={handleFileChange}
                                        required
                                    />
                                </div>

                                <div className="RegisForm_1">
                                    <label>Description:</label>
                                    <textarea
                                        value={description}
                                        onChange={(e) => setDescription(e.target.value)}
                                    ></textarea>
                                </div>

                            </div>

                            <form onSubmit={handleSubmit}>
                                <div className="Main_container_Btn">
                                    <button type="submit" disabled={isLoading} style={{ width: '70px' }}>
                                        {isLoading ? 'Uploading...' : 'Upload'}
                                    </button>
                                    <button type="button" onClick={fetchDocuments} disabled={isLoading} style={{ width: '70px' }}>
                                        {isLoading ? 'Fetching...' : 'Fetch'}
                                    </button>
                                </div>
                            </form>

                            {/* {documents.length > 0 && (
                                <div style={{ display: 'flex' }}>
                                    {documents.map((doc, index) => (
                                        <div >
                                            <h3 >
                                                {doc.asset_name}
                                            </h3>
                                            <p >Type: {doc.document_type}</p>
                                            <button
                                                onClick={() => window.open(`${UrlLink}AccetCategory${doc.file_url}`, '_blank')}
                                            >
                                                View
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )} */}
                            {showDocuments && documents.length > 0 && (
                                <div style={{ display: 'flex' }}>
                                    {documents.map((doc, index) => (
                                        <div key={index}>
                                            <h3>{doc.asset_name}</h3>
                                            <p>Type: {doc.document_type}</p>
                                            <button
                                                onClick={() => window.open(`${UrlLink}AccetCategory${doc.file_url}`, '_blank')}
                                            >
                                                View
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </>}
                {/* -------------------------Asset Document List------------------ */}
                {RackMasterPage === 'AssetDocumentList' && <>
                    <br />
                    {/* <div className="Main_container_app">

                        <div className="RegisFormcon_1">
                            <div className="RegisForm_1">
                                <label>
                                    Select Asset <span>:</span>
                                </label>
                                <select
                                    value={currentAssetCode}
                                    onChange={(e) => setCurrentAssetCode(e.target.value)}
                                    required
                                >
                                    <option value="">Select an Asset</option>
                                    {availableAssets.map((asset) => (
                                        <option key={asset.id} value={asset.asset_code}>
                                            {asset.name} ({asset.asset_code})
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {currentAssetCode && (
                                <div className="RegisForm_1">
                                    <label>
                                        Select Document Category <span>:</span>
                                    </label>
                                    <select
                                        value={selectedDocCategory}
                                        onChange={(e) => setSelectedDocCategory(e.target.value)}
                                        required
                                    >
                                        <option value="">Select Document Type</option>
                                        <option value="INVOICE">Invoice</option>
                                        <option value="WARRANTY">Warranty Card</option>
                                        <option value="MANUAL">User Manual</option>
                                        <option value="CERTIFICATE">Certificate</option>
                                        <option value="CONTRACT">Contract</option>
                                        <option value="REPORT">Inspection Report</option>
                                        <option value="OTHER">Other</option>
                                    </select>
                                </div>
                            )}
                        </div>

                        <div className="Main_container_Btn">
                            {currentAssetCode && selectedDocCategory && (
                                <button onClick={handleSearch} style={{ width: "110px" }}>
                                    Fetch Documents
                                </button>
                            )}
                        </div>

                        {!activeDocumentPreview ? (
                            <div className="Main_container_Btn">
                                <ul className="document-list">
                                    {assetDocuments.map((doc) => (
                                        <li key={doc.id}>
                                            <strong>{doc.asset_name} ({doc.asset_code}):</strong>
                                            <span> - {doc.document_type}</span>
                                            <button  onClick={() => viewDocument(doc)}>View</button>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ) : (
                            // Document view with Close button
                            <div className="Main_container_Btn">
                                <button onClick={closeDocumentView} className="btn btn-secondary">
                                    Close and Go to Dashboard
                                </button>
                            </div>
                        )}
                    </div> */}

                </>
                }
            </div>
        </>

    )
}
export default AssetDocumentsupload;