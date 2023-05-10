import { Container, Row, Col, Button, Form, Table } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import { methods } from "../plugins/http";


const InputForm = () => {

    const [inputJson, setInputJson] = useState({})

    useEffect(() => {
        if (localStorage.inputJson) setInputJson(JSON.parse(localStorage.inputJson))
    }, [])

    return (
        <Container fluid className="createExp mt-4 p-4">
            <Form>
                <Row>
                    <Col>
                        <Form.Group className="mb-3 text-left" controlId="opportunityId">
                            <Form.Label className="required_class">Opportunity Id</Form.Label>
                            <Form.Control type="text" placeholder="Name" onChange={(e) => setInputJson({ ...inputJson, "opportunityId": e.target.value })} value={inputJson.opportunityId} required />
                            {/* {errorIn["opportunityId"]["err"] && <div className="invalid_feedback">{errorIn["opportunityId"]["msg"] || "Experiment Name is required"}</div>} */}
                        </Form.Group>
                    </Col>
                </Row>
            </Form>

            <Table>

            </Table>
        </Container>
    )
}

export default InputForm