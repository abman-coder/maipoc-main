import { useEffect, useState } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory from 'react-bootstrap-table2-editor';
import { methods } from '../plugins/http';

const OutputTable = ({ data, selected, modelType, selectedInputs = {} }) => {
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

    const columns = [{
        dataField: 'id',
        text: 'ID'
    }, {
        dataField: 'Prop_Score',
        text: 'Prop_Score'
    }, {
        dataField: 'Prop_Bucket',
        text: 'Prop_Bucket'
    }, {
        dataField: 'Business_Feature_Name',
        text: 'Business_Feature_Name'
    }, {
        dataField: 'Feature_Direction',
        text: 'Feature_Direction'
    }, {
        dataField: 'Level_Name',
        text: 'Level_Name'
    }, {
        dataField: 'Risk Reserve CCUS',
        text: 'Feature Importance'
    }, {
        dataField: 'Action',
        text: 'Action_Taken'
    }, {
        dataField: 'Actionable_Flag',
        text: 'Actionable_Flag'
    }, {
        dataField: 'Seller_Narratives_Other',
        text: 'Seller_Narratives'
    }];

    const [defaultData, setdefaultData] = useState([]);
    const [timerId, settimerId] = useState(null);
    const [count, setcount] = useState(0);

    const reScore = () => {
        methods.post('output_values_with_optid', { "id": localStorage.id, "opty_id": selected, "type": modelType, ...selectedInputs }).then(res => {
            setdefaultData(res.data?.opty_rows);
            if (res.data.received || count > 20) {
                clearInterval(timerId);
            }
            setcount(count + 1);
        })
    }

    useEffect(() => {
        if (selected) {
            reScore()
            const intId = setInterval(() => {
                reScore()
            }, 30000);
            settimerId(intId);
        }

    }, [selected])


    return (<>
        <div>
            <h3>Output Table:</h3>
        </div>
        <BootstrapTable
            keyField="id"
            data={defaultData}
            columns={columns}
        // cellEdit={cellEditFactory({ mode: 'click' })}
        />
    </>
    )
}

export default OutputTable;