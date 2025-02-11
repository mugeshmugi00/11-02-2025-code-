import React, { useState, useEffect } from "react";
import ToggleOnIcon from "@mui/icons-material/ToggleOn";
import ToggleOffIcon from "@mui/icons-material/ToggleOff";
import NewNavigationMasters from "../../LabMasters/NewMastersNavigations";
import NewMasterList from "../../LabMasters/NewMasterList";
import TestMasterNavigation from "../../LabMasters/TestMasterNavigation";
import ExternalLabList from "../../LabMasters/ExternalLabList";
import ReferDoctorList from "../../LabMasters/ReferDoctorList";
import RatecardLims from "../../LabMasters/RatecardLims";
import GroupMasterList from "../../LabMasters/GroupMasterList";

function LabMasterNavigation() {
    const [activeTab, setActiveTab] = useState("NewMasterList");
    const [isToggled, setIsToggled] = useState(false);
    // const urllink = useSelector(state => state.userRecord?.UrlLink)

    const toggle = () => setIsToggled(!isToggled);

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        closeToggle();
    };

    const closeToggle = () => {
        setIsToggled(false);
    };

    useEffect(() => {
        const handleBodyClick = (event) => {
            if (!event.target.closest(".new-kit")) {
                closeToggle();
            }
        };

        document.body.addEventListener("click", handleBodyClick);

        return () => {
            document.body.removeEventListener("click", handleBodyClick);
        };
    });

    return (
        <>
            <div className="appointment">

                <br />
                <div className="new-patient-registration-form1">
                    <div className="new-navigation">
                        <h2>
                            <button onClick={() => handleTabChange("NewMasterList")}>
                                Test Master
                            </button>
                            |
                            <button onClick={() => handleTabChange("BasicMasters")}>
                                BasicMasters
                            </button>
                            |

                            <button onClick={() => handleTabChange("TestMasterNavigation")}>
                                TestMasterNavigation
                            </button>
                            |

                            <button onClick={() => handleTabChange("ExternalLabList")}>
                                ExternalLab
                            </button>
                            |

                            <button onClick={() => handleTabChange("ReferDoctorList")}>
                                ReferDoctor
                            </button>
                            |

                            <button onClick={() => handleTabChange("RatecardLims")}>
                                Lab Ratecard
                            </button>

                            |

                            <button onClick={() => handleTabChange("GroupMasterList")}>
                                Group Master
                            </button>

                        </h2>
                    </div>

                    <div className="new-kit ">
                        <button className="new-tog" onClick={toggle}>
                            {isToggled ? <ToggleOffIcon /> : <ToggleOnIcon />}
                        </button>

                        <div>
                            {isToggled && (
                                <div className="new-navigation-toggle">
                                    <h2>
                                        <button onClick={() => handleTabChange("BasicMasters")}>
                                            BasicMasters
                                        </button>
                                        |
                                        <button onClick={() => handleTabChange("BasicMasters")}>
                                            BasicMasters
                                        </button>
                                        |

                                        <button onClick={() => handleTabChange("TestMasterNavigation")}>
                                            TestMasterNavigation
                                        </button> |

                                        <button onClick={() => handleTabChange("ExternalLabList")}>
                                            ExternalLab
                                        </button> |

                                        <button onClick={() => handleTabChange("ReferDoctorList")}>
                                            ReferDoctor
                                        </button>
                                        |

                                        <button onClick={() => handleTabChange("RatecardLims")}>
                                            Lab Ratecard
                                        </button>
                                        |

                                        <button onClick={() => handleTabChange("GroupMasterList")}>
                                            Group Master
                                        </button>
                                    </h2>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {activeTab === "BasicMasters" && <NewNavigationMasters />}
            {activeTab === "NewMasterList" && <NewMasterList />}
            {activeTab === "TestMasterNavigation" && <TestMasterNavigation />}
            {activeTab === "ExternalLabList" && <ExternalLabList />}
            {activeTab === "ReferDoctorList" && <ReferDoctorList />}
            {activeTab === "RatecardLims" && <RatecardLims />}
            {activeTab === "GroupMasterList" && <GroupMasterList />}
        </>
    );
}

export default LabMasterNavigation;

