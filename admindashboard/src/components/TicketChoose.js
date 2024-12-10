import React, { useState } from "react";
import "./Styles/TicketChoose.css"
import { useNavigate } from "react-router-dom";
import ServiceNowTicket from "./Ticketing System/ServiceNow";
import ZendeskTicket from "./Ticketing System/ZenDesk"
import JiraTicket from "./Ticketing System/Jira"

const TicketChoose = ({ onNext }) => {
    const [system, setSystem] = useState("");

    return (
        <div className="MainTicketChooseContainer">
            <div className="TicketChoose-main-container">
                <div className="TicketChoose-container">
                    <h1>Choose One Ticketing System Below</h1>
                    <label>
                        System:
                        <select value={system} onChange={(e) => setSystem(e.target.value)}>
                            <option value="">Select</option>
                            <option value="ServiceNow">Service Now</option>
                            <option value="Zendesk">Zendesk</option>
                            <option value="Jira">Jira</option>
                        </select>
                    </label>
                    {system === 'ServiceNow' && <ServiceNowTicket />}
                    {system === 'Zendesk' && <ZendeskTicket />}
                    {system === 'Jira' && <JiraTicket />}

                </div>

            </div>
        </div>
    );
};

export default TicketChoose;
