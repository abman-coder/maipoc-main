
const Constant = {
    "Opportunity Propensity": {
        "url": "default_values_with_optid",
        "columns": [{
            dataField: 'id',
            text: 'ID',
            editable: false,
            sort: true
        }, {
            dataField: 'contract id',
            text: 'Contract_Id',
            "editable": (cell, row) => row.new === true,
            "ifNew": true,
            // editable: false
        }, {
            dataField: 'pkg_id',
            text: 'Package_Id',
            // editable: false,
            "editable": (cell, row) => row.new === true,
            "ifNew": true,

            // sort: true
        }, {
            dataField: 'ResourceTier',
            text: 'Resource Tier',
            editor: {
                type: 'select',
                options: [
                    { value: 'Tier 4: PjM/Cons/ADE', label: 'Tier 4: PjM/Cons/ADE' },
                    { value: 'Tier 3: Sr PjM/Cons/ADE', label: 'Tier 3: Sr PjM/Cons/ADE' },
                    { value: 'Tier 2: Architect', label: 'Tier 2: Architect' },
                    { value: 'Tier 5: GD/Subcon', label: 'Tier 5: GD/Subcon' },
                    { value: 'Tier 1: Sr Architect', label: 'Tier 1: Sr Architect' },
                    { value: 'Other', label: 'Other' },
                ]
            },
            // "editable": (cell, row) => row.new === true
        }, {
            dataField: 'Revenue CCUS',
            text: 'Revenue CCUS'
        }, {
            dataField: 'Discount CCUS',
            text: 'Discount CCUS'
        }, {
            dataField: 'ECIFCommitted',
            text: 'ECIF CCUS'
        }, {
            dataField: 'Risk Reserve CCUS',
            text: 'Risk Reserve CCUS'
        }, {
            dataField: 'FeeType',
            text: 'Fee Type',
            editor: {
                type: 'select',
                options: [
                    { value: 'Fixed Fee', label: 'Fixed Fee' },
                    { value: 'Time & Materials', label: 'Time & Materials' },
                    // { value: 'T & M Cap', label: 'T & M Cap' }
                ]
            },
            // sort: true
        }, {
            dataField: 'Total Resource Hours',
            text: 'Total Resource Hours'
        }],
        "others": {
            "type": "Opportunity Propensity"
        },
    },
    "Risk Assessment": {
        "url": "default_values_with_optid",
        "columns": [
            { "dataField": "Deal ID", "text": "Deal_ID", "editable": false }, { "dataField": "Contract Id", "text": "Contract Id", "editable": false }, { "dataField": "ProjectId", "text": "ProjectId", "editable": false },
            { "dataField": "Fee Arrangement", "text": "Fee Arrangement" }, { "dataField": "NST Category", "text": "NST Category" }, { "dataField": "Total Resource Hours", "text": "Total Resource Hours" }, { "dataField": "Project Manager Mix", "text": "Project Manager Mix" }, { "dataField": "Standard Offering Type", "text": "Standard Offering Type" }, { "dataField": "Deal Velocity", "text": "Deal Velocity" }, { "dataField": "Is ECIF", "text": "Is ECIF" }, { "dataField": "Payment Terms", "text": "Payment Terms" }, { "dataField": "Delivery Margin Target", "text": "Delivery Margin Target" }, { "dataField": "Derived Primary Domain", "text": "Derived Primary Domain" }, { "dataField": "Domain Count", "text": "Domain Count" }, { "dataField": "Is Subcon Identified", "text": "Is Subcon Identified" }, { "dataField": "Planned Contract Microsoft IGD Hours", "text": "Planned Contract Microsoft IGD Hours" }, { "dataField": "IndustrySector", "text": "IndustrySector" }, { "dataField": "DeliveryCostServicesUSD", "text": "DeliveryCostServicesUSD" },
            { "dataField": "opportunitysalesstage", "text": "opportunitysalesstage", "editable": false }, { "dataField": "Label", "text": "Label", "editable": false }, { "dataField": "DateTimeStamp", "text": "DateTimeStamp", "editable": false }, { "dataField": "Is Public Sector", "text": "Is Public Sector", "editable": false }, { "dataField": "HAS SOW", "text": "HAS SOW", "editable": false }, { "dataField": "CloudFlag", "text": "CloudFlag", "editable": false }, { "dataField": "OSEDealsFlag", "text": "OSEDealsFlag", "editable": false }, { "dataField": "Outlier Type", "text": "Outlier Type", "editable": false }, { "dataField": "Pricing Cut Off", "text": "Pricing Cut Off", "editable": false }, { "dataField": "Is Misstated", "text": "Is Misstated", "editable": false }, { "dataField": "Is IP Exchange", "text": "Is IP Exchange", "editable": false }, { "dataField": "PL Requested Type", "text": "PL Requested Type", "editable": false }, { "dataField": "Total SubCon Hours", "text": "Total SubCon Hours", "editable": false }, { "dataField": "PPGCategory", "text": "PPGCategory", "editable": false }, { "dataField": "ORBApproved", "text": "ORBApproved", "editable": false }, { "dataField": "opportunityaginggroup", "text": "opportunityaginggroup", "editable": false }, { "dataField": "Is Amendment", "text": "Is Amendment", "editable": false }, { "dataField": "Area", "text": "Area", "editable": false }, { "dataField": "IsGlobal", "text": "IsGlobal", "editable": false }, { "dataField": "CompassOneIndustryName", "text": "CompassOneIndustryName", "editable": false }, { "dataField": "Contract Created Date Fiscal Year", "text": "Contract Created Date Fiscal Year", "editable": false }, { "dataField": "Is Vaguely Described", "text": "Is Vaguely Described", "editable": false }, { "dataField": "QA_TQA_Critical", "text": "QA_TQA_Critical", "editable": false }, { "dataField": "QA_TQA_High", "text": "QA_TQA_High", "editable": false }, { "dataField": "QA_TQA_Medium", "text": "QA_TQA_Medium", "editable": false }, { "dataField": "QA_TQA_Low", "text": "QA_TQA_Low", "editable": false }, { "dataField": "Output", "text": "Output", "editable": false }, { "dataField": "Custom_perc", "text": "Custom_perc", "editable": false }, { "dataField": "CSAT", "text": "CSAT", "editable": false }, { "dataField": "Delivery Type", "text": "Delivery Type", "editable": false }, { "dataField": "Red_Projects_SubRegion", "text": "Red_Projects_SubRegion", "editable": false }, { "dataField": "Red_Count_PPG", "text": "Red_Count_PPG", "editable": false }, { "dataField": "Red_Cost_PPG", "text": "Red_Cost_PPG", "editable": false }
        ],
        "others": {
            "type": "Risk Assessment"
        }
    },
    "getColumns": function (modelType) {
        return this[modelType].columns.map(col => {
            if (modelType === "Risk Assessment" && col.editable !== false) {
                col.editable = (cell, row) => (!row.originalRow && col.editable)
            }
            // if (col.editable === false) {
            if (1) {
                return {
                    ...col, style: function (cell, row, rowIndex, colIndex) {
                        if ((col.editable === false || row.originalRow) || (col.ifNew === true && !row.new)) {
                            return {
                                "backgroundColor": "rgba(148, 146, 146, 0.3)"
                            }
                        }
                        return {}
                    }, attrs: {
                        // style: {
                        //     "backgroundColor": "rgba(148, 146, 146, 0.3)",
                        //     // "color": "white"
                        // }
                    }
                };
            }
            return col;
        })
    },
}

export default Constant;