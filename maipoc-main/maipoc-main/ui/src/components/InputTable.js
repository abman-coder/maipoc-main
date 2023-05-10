import { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory from 'react-bootstrap-table2-editor';
import { methods } from '../plugins/http';
import Constant from '../constant';

const InputTable = ({ data, selected, setEvaluate, modelType, dropdownValues, defaultData, noData, addNewRow, deleteARow, originalData }) => {
    const products = data || [
        {
            id: 1,
            name: 'test1',
            price: 20
        },
        {
            id: 2,
            name: 'test2',
            price: 40
        },
        {
            id: 3,
            name: 'test3',
            price: 60
        }
    ]

    let columns = Constant.getColumns(modelType);

    // const [defaultData, setdefaultData] = useState([]);

    // useEffect(() => {
    //     if (selected) {
    //         methods.post('default_values_with_optid', { "type": modelType, "opty_id": selected }).then(res => {
    //             setdefaultData(res.data?.opty_rows);
    //         })
    //     }

    // }, [selected])

    const convertToInt = val => isNaN(val) ? val : +val;

    const [columnsModified, setcolumnsModified] = useState([])
    const [rowsModified, setrowsModified] = useState([])
    const [rowsDeleted, setrowsDeleted] = useState([])

    const saveData = async () => {
        let dataToSave = [...defaultData];

        if (modelType === 'Risk Assessment') {
            dataToSave = dataToSave.slice(1);
        }

        dataToSave = dataToSave.map(dr => {
            for (let ij of columnsModified) {
                dr[ij] = convertToInt(dr[ij]);
            }
            return dr;
        })

        let saveInfo = []
        // rowsDeleted.map(dr => {
        //     return {
        //         ...keyoriginalData[dr],
        //         deleted: true
        //     }
        // })

        // const keyoriginalData = originalData.reduce((acc, cur) => {
        //     acc[cur.id] = cur;
        //     return acc;
        // }, {})

        // const keydefaultData = defaultData.reduce((acc, cur) => {
        //     acc[cur.id] = cur;
        //     if (cur.new) saveInfo.push(cur)
        //     return acc;
        // }, {});

        // [...new Set(rowsModified)].forEach(row => {
        //     let obj = {}
        //     for (let ij in keyoriginalData[row]) {
        //         if (keyoriginalData[row][ij] !== keydefaultData[row][ij]) {
        //             obj['initial_' + ij] = keyoriginalData[row][ij]
        //             obj['modified_' + ij] = keydefaultData[row][ij]
        //         }
        //     }
        //     saveInfo.push(obj)
        // })

        // if (modelType === 'Opportunity Propensity') {
        //     const id = `re_${Date.now()}.json`
        //     localStorage.id = id;
        //     await methods.post('re_score', { "type": modelType, "id": id, "data": dataToSave }).then(res => {
        //         console.log(res.data)
        //     })
        // }
        setEvaluate({ "saveInfo": saveInfo, "data": dataToSave.map(ds => ({ ...ds, "Score": undefined, Label: undefined })) });
    }

    if (dropdownValues) {
        columns = columns.map(col => {
            if (dropdownValues[col.dataField]) {
                col.editor = {
                    type: 'select',
                    options: dropdownValues[col.dataField].map(a => ({ value: a, label: a }))
                }
            }
            return col;
        })
    }

    if (modelType === 'Opportunity Propensity') {
        columns.push({
            dataField: 'actions',
            text: 'Actions',
            isDummyField: true,
            csvExport: false,
            formatter: (cell, row, indx) => (
                <div>
                    <Button color="primary" size="sm" id={row.id} onClick={() => {
                        deleteARow(indx, defaultData);
                        setrowsDeleted([...rowsDeleted, row.id])
                    }}>
                        Delete
                    </Button>
                </div>
            ),
        })
    }

    return (<>
        <div class="f-12" style={{ "fontSize": "12px", "textAlign": "left", "color": "#f30808" }}>
            Double click to edit any value. After editing press enter to save the value</div>
        {modelType === "Opportunity Propensity" && <Button onClick={() => addNewRow(
            // { "opty_id": selected, "id": "", "contract id": "", "pkg_id": "", "Revenue CCUS": 0, "Discount CCUS": 0, "ECIFCommitted": 0, "Risk Reserve CCUS": 0, "FeeType": "", "ResourceTier": "", "Total Resource Hours": 0, "ItemLevel": "Resource" }

            {
                "ACRPotentialRevenue": 0,
                "BIF Amount CCUS": 0,
                "Discount CCUS": 0,
                "ECIFCommitted": null,
                "FeeType": "",
                "ItemLevel": "Resource",
                "ResourceTier": "",
                "Revenue CCUS": 0,
                "Risk Reserve CCUS": 0,
                "Total Resource Hours": 0,
                "contract id": 0,
                "id": +(defaultData[defaultData.length - 1]?.id || 0) + 1,
                "is S500 Flag": "",
                "opportunitycreateddatefiscalyear": "",
                "opportunitystatus": "",
                "opty_id": selected,
                "pkg_id": 0,
                "new": true
            }



        )}>+ Add</Button>}
        <BootstrapTable
            keyField="id"
            data={defaultData}
            columns={columns}
            cellEdit={cellEditFactory({ mode: 'dbclick', afterSaveCell: (oldValue, newValue, row, column) => { setcolumnsModified([...columnsModified, column.dataField]); if (!row.new) { setrowsModified([...rowsModified, row.id]) } } })}
        />
        {defaultData.length !== 0 && <Button onClick={() => saveData()}>Evaluate</Button>}
    </>
    )
}

export default InputTable;