import axios from 'axios';
import React, { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { Button } from '@mui/material';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import EditIcon from "@mui/icons-material/Edit";

const AssetRelationship = () => {

    const [categories, setCategories] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [parentAssets, setParentAssets] = useState([]);
    const [allAssets, setAllAssets] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [parentAsset, setParentAsset] = useState('');
    const [relationships, setRelationships] = useState([]);
    const [tempRelationships, setTempRelationships] = useState([]);
    const [AssetRelationshipData, setAssetRelationshipData] = useState([]);
    const [AssetRegistered_RelationshipData, setAssetRegistered_RelationshipData] = useState([]);
    const [childAsset, setChildAsset] = useState('');
    const [filteredChildAssets, setFilteredChildAssets] = useState([]); // New state for filtered child assets

    const [relationshipType, setRelationshipType] = useState('CHILD');

    // Fetch categories, assets, and relationships when component mounts
    useEffect(() => {
        axios.get('http://localhost:8000/api/asset-categories/')
            .then(response => setCategories(response.data))
            .catch(error => console.error(error));

        axios.get('http://localhost:8000/api/assets/')
            .then(response => setAllAssets(response.data))
            .catch(error => console.error(error));

        fetchRelationships();
    }, []);

    const fetchRelationships = () => {
        axios.get('http://localhost:8000/api/asset-relationships/')
            .then(response => {
                setRelationships(response.data);
                setAssetRelationshipData(response.data);  
            })
            .catch(error => console.error("Failed to fetch relationships:", error));
    };
    

    // Fetch subcategories based on selected category
    useEffect(() => {
        if (selectedCategory) {
            axios.get(`http://localhost:8000/api/asset-subcategories/?category=${selectedCategory}`)
                .then(response => {
                    setSubcategories(response.data);
                    setSelectedSubcategory('');
                })
                .catch(error => console.error(error));
        } else {
            setSubcategories([]);
        }
    }, [selectedCategory]);

    // Filter parent assets based on selected category, subcategory, and exclude those already registered as a parent
    useEffect(() => {
        if (selectedCategory && selectedSubcategory) {
            axios.get(`http://localhost:8000/api/assets/?category=${selectedCategory}&subcategory=${selectedSubcategory}`)
                .then((response) => {
                    console.log('subbbbb', selectedSubcategory);

                    const data = response.data;
                    const data1 = data?.filter((row) => String(row.asset_subcategory) === String(selectedSubcategory))
                    //console.log('subbbb',data);
                    //console.log('subbbb111',data1);

                    setParentAssets(data1)
                })
                .catch(error => console.error("Error fetching parent assets:", error));
        }
    }, [selectedCategory, selectedSubcategory]);


    // filter child assets based on selected category, subcategory, and exclude those already registered as
    useEffect(() => {
        if (selectedCategory && selectedSubcategory && parentAsset) {
            axios.get(`http://localhost:8000/api/assets/?category=${selectedCategory}&subcategory=${selectedSubcategory}`)
                .then(response => {
                    // Exclude the selected parent asset by comparing the IDs
                    const filteredChildren = response.data.filter(asset => asset.id !== parseInt(parentAsset, 10));
                    setFilteredChildAssets(filteredChildren);
                })
                .catch(error => console.error("Error fetching child assets:", error));
        }
    }, [selectedCategory, selectedSubcategory, parentAsset]);


    /*// filter child assets based on selected category, subcategory, and exclude those already registered as
      useEffect(() => {
        if (selectedCategory && selectedSubcategory && parentAsset) {
          axios.get(`http://localhost:8000/api/assets/?category=${selectedCategory}&subcategory=${selectedSubcategory}`)
            .then(response => {
              // Filter child assets to exclude the selected parent asset
              setFilteredChildAssets(response.data.filter(asset => asset.id !== parentAsset));
            })
            .catch(error => console.error("Error fetching child assets:", error));
        }
      }, [selectedCategory, selectedSubcategory, parentAsset]);*/



    // Handle adding temporary relationships
    const handleAddTempRelationship = () => {
        if (!parentAsset || !childAsset) {
            alert('Please select both parent and child assets');
            return;
        }

        const newRelationship = {
            id: Date.now(),
            parent_asset: parentAsset,
            child_asset: childAsset,
            relationship_type: relationshipType
        };

        setTempRelationships([...tempRelationships, newRelationship]);

        // Reset child asset and relationship type
        setChildAsset('');
        setRelationshipType('CHILD');
    };



    // Remove a temporary relationship
    const handleRemoveTempRelationship = (id) => {
        setTempRelationships(tempRelationships.filter(rel => rel.id !== id));
    };

    // Edit a relationship
    const handleEditTempRelationship = (relationship) => {
        setParentAsset(relationship.parent_asset.id);
        setChildAsset(relationship.child_asset.id);
        setRelationshipType(relationship.relationship_type);
        setTempRelationships(tempRelationships.filter(rel => rel.id !== relationship.id));
    };

    // Save all relationships
    const handleSaveRelationships = () => {
        const relationshipData = tempRelationships.map(rel => ({
            parent_asset: rel.parent_asset,
            child_assets: [rel.child_asset],
            relationship_type: rel.relationship_type
        }));
    
        axios.post('http://localhost:8000/api/asset-relationships/bulk_create/', relationshipData)
            .then(response => {
                setRelationships([...relationships, ...response.data.relationships]);
                setAssetRelationshipData([...AssetRelationshipData, ...response.data.relationships]);  // Add this line to update the data
                setTempRelationships([]);
                setParentAsset('');
                alert(response.data.message);
            })
            .catch(error => {
                console.error("Failed to create relationships:", error);
                alert(error.response?.data?.error || "An error occurred while creating the relationships");
            });
    };
    

    // Handle deleting a relationship
    const handleDeleteRelationship = (id) => {
        axios.delete(`http://localhost:8000/api/asset-relationships/${id}/`)
            .then(() => {
                setRelationships(relationships.filter(rel => rel.id !== id));
                alert("Relationship deleted successfully");
            })
            .catch(error => {
                console.error("Failed to delete relationship:", error);
                alert("Failed to delete relationship");
            });
    };
    const toggleStatus = async (relationship) => {
        const updatedRelationship = { 
            ...relationship, 
            status: relationship.status === 'active' ? 'inactive' : 'active' 
        };
    
        try {
            await axios.put(`http://localhost:8000/api/asset-relationships/${relationship.rel_id}/`, updatedRelationship);
            setRelationships(relationships.map(rel => 
                rel.rel_id === relationship.rel_id ? updatedRelationship : rel
            ));
        } catch (error) {
            console.error("Failed to toggle status:", error);
        }
    };
    
    const handleEditAssetCategory = (relationship) => {
        setParentAsset(relationship.parentAssets.id);
        setChildAsset(relationship.child_asset.id);
        setRelationshipType(relationship.relationship_type);
        setTempRelationships(tempRelationships.filter(rel => rel.rel_id !== relationship.rel_id));
    };
    
    const Asset_toggleStatus = async (registeredRelationship) => {
        const updatedRegisteredRelationship = { 
            ...registeredRelationship, 
            status: registeredRelationship.status === 'active' ? 'inactive' : 'active' 
        };
    
        try {
            await axios.put(`http://localhost:8000/api/asset-registered-relationships/${registeredRelationship.rel_id}/`, updatedRegisteredRelationship);
            setAssetRegistered_RelationshipData(AssetRegistered_RelationshipData.map(rel => 
                rel.rel_id === registeredRelationship.rel_id ? updatedRegisteredRelationship : rel
            ));
        } catch (error) {
            console.error("Failed to toggle registered relationship status:", error);
        }
    };
    
    const Asset_handleEditAssetCategory = (registeredRelationship) => {
        setParentAsset(registeredRelationship.parentAssets.id);
        setChildAsset(registeredRelationship.related_asset.id);
        setRelationshipType(registeredRelationship.relationship_type);
        setTempRelationships(tempRelationships.filter(rel => rel.rel_id !== registeredRelationship.rel_id));
    };
    

    const AssetRelationshipColumn = [
        {
            key: 'rel_id',
            name: 'rel Id',
        },
        {
            key: 'parentAssets',
            name: 'parent Assets',
        }, {
            key: 'child_asset',
            name: 'child Asset',
        }, {
            key: 'relationship_type',
            name: 'relationship Type',
        },
        {
            key: 'status',
            name: 'Status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatus(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        {
            key: 'Action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEditAssetCategory(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        }
    ];
    const AssetRegistered_RelationshipColumn = [
        {
            key: 'rel_id',
            name: 'rel Id',
        },
        {
            key: 'parentAssets',
            name: 'parent Assets',
        }, {
            key: 'related_asset',
            name: 'related Asset',
        }, {
            key: 'relationship_type',
            name: 'relationship Type',
        },
        {
            key: 'status',
            name: 'Status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => Asset_toggleStatus(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        {
            key: 'Action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => Asset_handleEditAssetCategory(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        }
    ]

    return (
        <div className="Main_container_app">
            <h3>Asset Relationship Management</h3>

            <div className="RegisFormcon_1">
                <div className="RegisForm_1">
                    <label>
                        Parent Category <span>:</span>
                    </label>
                    <select value={selectedCategory} onChange={(e) => setSelectedCategory(e.target.value)}>
                        <option value="">Select Category</option>
                        {categories.map(category => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>
                        Parent Subcategory <span>:</span>
                    </label>
                    <select value={selectedSubcategory} onChange={(e) => setSelectedSubcategory(e.target.value)} disabled={!selectedCategory}>
                        <option value="">Select Subcategory</option>
                        {subcategories.map(subcategory => (
                            <option key={subcategory.id} value={subcategory.id}>{subcategory.name}</option>
                        ))}
                    </select>
                </div>


                <div className="RegisForm_1">
                    <label>
                        Parent Asset <span>:</span>
                    </label>
                    <select value={parentAsset} onChange={(e) => setParentAsset(e.target.value)} disabled={!selectedSubcategory}>
                        <option value="">Select Parent Asset</option>
                        {parentAssets.map(asset => (
                            <option key={asset.id} value={asset.id}>{asset.name}</option>
                        ))}
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>
                        Child Asset <span>:</span>
                    </label>
                    <select value={childAsset} onChange={(e) => setChildAsset(e.target.value)} disabled={!parentAsset}>
                        <option value="">Select Child Asset</option>
                        {filteredChildAssets.map(asset => (
                            <option key={asset.id} value={asset.id}>{asset.name} ({asset.category_name} - {asset.subcategory_name})</option>
                        ))}
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>
                        Relationship Type <span>:</span>
                    </label>
                    <select value={relationshipType} onChange={(e) => setRelationshipType(e.target.value)}>
                        <option value="CHILD">Child</option>
                        <option value="COMPONENT">Component</option>
                        <option value="ACCESSORY">Accessory</option>
                    </select>
                </div>
            </div>


            <div className="Main_container_Btn">
                <button onClick={handleAddTempRelationship} style={{ width: "120px" }}>
                    Add Relationship
                </button>
            </div>

            <div className="RegisFormcon_1">
                <h3>Temporary Relationships</h3>
                <div className="Main_container_Btn">
                    <button onClick={handleSaveRelationships} disabled={tempRelationships.length === 0} style={{ width: "150px" }}>
                        Save Relationships
                    </button>
                </div>

                <ReactGrid columns={AssetRelationshipColumn} RowData={AssetRelationshipData} />

                <h3>Registered Relationships</h3>
                <ReactGrid columns={AssetRegistered_RelationshipColumn} RowData={AssetRegistered_RelationshipData} />
            </div>
        </div >

    )
}
export default AssetRelationship;