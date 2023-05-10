import './App.css';
// import InputForm from './components/inputForm';
import InputTable from './components/InputTable';
import OutputTable from './components/OutputTable';
import ReactSelect from "react-select";
import { Container, Row, Col, Button, Form } from "react-bootstrap";

import { MsalProvider } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";

import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
  useAccount,
} from "@azure/msal-react";
import { loginRequest, protectedResources } from "./authConfig";
import { useEffect, useState } from 'react';
import { methods } from './plugins/http';
import AsyncTypeAhead from './plugins/AsyncTypeAhead';



function MainPage({ }) {
  const history = useNavigate();
  const { instance } = useMsal();

  // variables
  const [opsListData, setOpsListData] = useState([]);
  const [opsSelected, setOpsSelected] = useState(null);
  const [scoreValue, setScoreValue] = useState(null);
  const [query, setQuery] = useState('');
  const [evaluate, setEvaluate] = useState(false);
  const [evaluateClicked, setEvaluateClicked] = useState(false);
  // const [modelSelected, setmodelSelected] = useState('Risk Assessment');
  const [modelSelected, setmodelSelected] = useState();

  const [defaultData, setdefaultData] = useState({});
  const [timerId, settimerId] = useState(null);
  const [count, setcount] = useState(0);
  const [dropdownValues, setdropdownValues] = useState(null);
  const [originalData, setoriginalData] = useState([]);
  const [defaultDataAllRows, setdefaultDataAllRows] = useState([]);
  const [OptyDefaultScore, setOptyDefaultScore] = useState(null);
  const [noData, setnoData] = useState(false)
  const [modelOPtions, setmodelOPtions] = useState([{ "label": "Risk Assessment", value: "Risk Assessment", key: 'r' }, { label: "Opportunity Propensity", value: "Opportunity Propensity", key: 'o' },]);

  const { accounts, inProgress } = useMsal();
  const account = useAccount(accounts[0] || {});

  useEffect(() => {
    if (!dropdownValues && modelSelected === 'Risk Assessment') {
      methods.get('opportunities?drop_down=1&type=' + modelSelected).then(res => {
        setdropdownValues(res.data?.drop_down);
      })
    }
  }, [modelSelected])

  const getRoleAccess = () => {
    methods.get('get_role_access').then((res, err) => {
      // setdropdownValues(res.data?.drop_down);
      if (res.data.code === 401 || err) {
        const trail = +(localStorage.trail || 0)
        if (!trail || trail < 4) {
          localStorage.trail = trail + 1
          setTimeout(() => {
            getRoleAccess()
          }, 800);
        }
      }
      const access = res.data.access.reduce((a, b) => (a[b] = 1, a), {});
      const filteredModelOPtions = modelOPtions.filter(m => access[m.key]);
      setmodelOPtions(filteredModelOPtions);
      if (filteredModelOPtions?.[0]) {
        setmodelSelected(filteredModelOPtions?.[0].value);
      }
    })
  }


  useEffect(() => {
    SaveToken()
    getRoleAccess()
  }, [])


  const SaveToken = () => {
    // const { accounts, inProgress } = useMsal();
    // const account = useAccount(accounts[0] || {});
    instance
      .acquireTokenSilent({
        scopes: protectedResources.apiHello.scopes,
        account: account,
      })
      .then((response) => {
        localStorage.token = response.accessToken;
        localStorage.userName = response.account.name;
        localStorage.userEmail = response.account.username;
        let path = localStorage.previousPath;
        delete localStorage.previousPath;
        if (path) history.push(path);
      })
      .catch((error) => {
        if (inProgress) return;
        history.push("/");
        console.log(error);
      });
  };


  useEffect(() => {
    let trm = setInterval(() => {
      SaveToken()
    }, 300000);

    return () => {
      clearInterval(trm);
    }
  }, [])


  const login = async () => {
    instance.loginRedirect(loginRequest);
    // if (history.location.pathname != "/")
    //   localStorage.previousPath = history.location.pathname;
  };

  const logOut = () => {
    localStorage.clear();
    window.location.reload()
  }

  // useEffect(() => {
  //   if (localStorage.modelSelected) setmodelSelected(localStorage.modelSelected)
  // }, [modelSelected])

  const reScore = () => {
    setEvaluateClicked(true)
    methods.post('output_values_with_optid', { "id": localStorage.id, "opty_id": opsSelected, "source": "uitool", "type": modelSelected, ...evaluate }).then(res => {
      if (modelSelected === 'Opportunity Propensity') {
        setdefaultData({ opty_rows: res.data?.score_output });
      } else {
        setdefaultData(res.data?.score_output);
      }
      if (res.data.received || count > 20) {
        clearInterval(timerId);
        setEvaluate(false);
      }
      setcount(count + 1);
    })
  }

  useEffect(() => {
    if (evaluate) {
      reScore()
      // const intId = setInterval(() => {
      //   reScore()
      // }, 30000);
      // settimerId(intId);
    }

  }, [evaluate])


  useEffect(() => {
    if (opsSelected) {
      setEvaluateClicked(false)
      setnoData(false)
      methods.post('default_values_with_optid', { "type": modelSelected, "source": "uitool", "opty_id": opsSelected }).then(res => {
        let rows = res.data?.opty_rows
        if (modelSelected === 'Risk Assessment') {
          let copiedRows = JSON.parse(JSON.stringify(rows))
          rows = [...copiedRows.map(r => { r.originalRow = true; r.id = `O${r.id}`; return r }), ...rows]
        }
        setdefaultDataAllRows(rows);
        setoriginalData(JSON.parse(JSON.stringify(rows)));
        setOptyDefaultScore(res.data?.old_input_score);
        if (!rows || !rows?.length) setnoData(true)
      })
    }

  }, [opsSelected])

  const addNewRow = row => {
    let newData = [...defaultDataAllRows];
    newData.push(row);
    setdefaultDataAllRows(newData);
  }

  const deleteARow = indx => {
    setdefaultDataAllRows(dfRows => {
      let newData = [...dfRows];
      newData.splice(indx, 1);
      return newData
    });
  }

  const numberToFixed = (number = 0, precision) => {
    const multiplier = Math.pow(10, precision || 0);
    return Math.round(number * multiplier) / multiplier;
  }

  return (
    <MsalProvider instance={instance}>

      <div className="App">
        <div className='App-header-container'>
          <header className="App-header">
            <div>
              ML as a service
            </div>
            <div>

              <AuthenticatedTemplate>
                <span className='f-12'>{localStorage.userName} </span> |
                <a onClick={logOut}> Log out</a>
              </AuthenticatedTemplate>

              {/* <UnauthenticatedTemplate>
                <a onClick={login}>Login</a>
              </UnauthenticatedTemplate> */}

            </div>
          </header>
        </div>

        <AuthenticatedTemplate>

          <div className='model-selection'>
            Select Model:
            <ReactSelect
              className='me-3 ms-2 mt-2'
              id="model-select"
              isOptionSelected={modelSelected}
              options={modelOPtions}
              value={{
                label: modelSelected,
                value: modelSelected,
              }}
              onChange={(values) => {
                setmodelSelected(null);
                setTimeout(() => {
                  setmodelSelected(values?.value || "");
                }, 500);
                setOpsSelected(null);
                setEvaluateClicked(false);
                setdefaultDataAllRows([])
                setQuery("")
              }}
              hideSelectedOptions={false}
              closeMenuOnSelect={true}
            />
          </div>

          {(!modelOPtions || modelOPtions.length === 0) && <h5 className='f-12'>Please contact admin to get access</h5>}

          {modelSelected &&
            <div>

              <Form.Group className="mb-3 text-left d-f fl-r" controlId="TargetMetric">

                <Form.Label className="me-2 ms-3 mt-2 required_class">{modelSelected === 'Opportunity Propensity' ? "Opportunity" : "Deal ID"}:</Form.Label>

                <Row>
                  <Col>
                    <AsyncTypeAhead
                      query={query}
                      type={modelSelected}
                      setQuery={setQuery}
                      keyWord={"opty_ids"}
                      searchUrl={"opportunities"}
                      placeholder={`Search for ${modelSelected === 'Opportunity Propensity' ? "an Opportunity" : "a Deal ID"}`}
                      onChange={val => { setOpsSelected(val?.[0]); setdefaultDataAllRows([]); setdefaultData({}) }}
                    />
                  </Col>
                </Row>

              </Form.Group>


            </div>}

          {modelSelected && defaultDataAllRows && opsSelected &&
            <Row className='w-100 p-lt-5 ml-5'>
              <Col className='col-lg-10 col-md-10'>
                <div>
                  <InputTable noData={noData} originalData={originalData} defaultData={defaultDataAllRows} selected={opsSelected} dropdownValues={dropdownValues} addNewRow={addNewRow} deleteARow={deleteARow} setEvaluate={val => setEvaluate(val)} modelType={modelSelected || "Opportunity Propensity"} />
                </div>
              </Col>
              {((modelSelected === 'Opportunity Propensity' && (OptyDefaultScore || defaultData?.opty_rows?.[0]?.Won)) || defaultDataAllRows?.[0]?.Label) &&
                <Col className='col-lg-2 col-md-2'>
                  {
                    modelSelected === 'Opportunity Propensity' ?
                      <div>
                        <span>Insights</span>
                        <div>Initial Score: {numberToFixed(OptyDefaultScore?.Score, 4)}</div>
                        <div>Initial Label: {OptyDefaultScore?.Label}</div>
                        {evaluateClicked && <>
                          <div>Score: {numberToFixed(defaultData?.opty_rows?.[0]?.Won, 4)}</div>
                          <div>Label: {defaultData?.opty_rows?.[0]?.Prop_Bucket}</div>
                          <div
                            style={{
                              marginTop: '10px'
                            }}
                          >Actions
                            <ul

                              style={{
                                maxHeight: '200px',
                                overflow: 'auto',
                                marginTop: '10px'
                              }}
                            >
                              {
                                defaultData?.opty_rows?.[0]?.Action?.map((rw, ind) => (
                                  <li key={ind}>{rw}</li>
                                ))
                              }
                            </ul>
                          </div>
                        </>}
                      </div> :
                      <div>
                        <div>
                          <span>Insights</span>
                          <div>Initial Score: {numberToFixed(defaultDataAllRows?.[0]?.Score, 4)}</div>
                          <div>Initial Label: {defaultDataAllRows?.[0]?.Label}</div>
                        </div>
                        {evaluateClicked && <div>
                          {/* <span>Insights</span> */}
                          <div>Score: {numberToFixed(defaultData?.[0]?.Score, 4)}</div>
                          <div>Label: {defaultData?.[0]?.Label}</div>
                        </div>}
                      </div>

                  }
                </Col>}
            </Row>}

          {/* {evaluate &&
          <Row className='w-100 p-lt-5'>
            <Col className='col-lg-10 col-md-10'>
              <div style={{ "height": "200px" }}>
                <OutputTable selected={opsSelected} selectedInputs={evaluate || {}} modelType={modelSelected || "Opportunity Propensity"} />
              </div>
            </Col>
          </Row>} */}
        </AuthenticatedTemplate>

        <UnauthenticatedTemplate>
          {/* <a onClick={login}>Login</a> */}
          <Button className='mt-2' color="primary" size="sm" onClick={login}>
            Login to continue
          </Button>
        </UnauthenticatedTemplate>


      </div>
    </MsalProvider>
  );
}

export default MainPage;
